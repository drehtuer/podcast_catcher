#!/usr/bin/env python3
"""
Main script for podcast_catcher application.

This script is a podcast catcher, which reads
a list of URLs to RSS/ATOM feeds and downloads
all new attachments (aka podcasts) to local
storage.
It offers renaming the downloaded files based
on the RSS/ATOM metadata and sets ID3 tags
accordingly. Too many feeds don't set their
tags or use undecipherable filenames.
"""

from argparse import ArgumentParser
from pathlib import Path
from sys import exit

from config_file import ConfigFile
from config_json_factory import ConfigJsonFactory
from episode_tracker import EpisodeTracker
from exception import PodcastCatcherError
from feed import Feed
from http_loader import HttpLoader
from id3tagger import ID3Tagger
from replacer import Replacer
from version import VERSION

# Subparsers
CMD_DOWNLOAD = 'download'
CMD_LIST_FEEDS = 'list_feeds'
CMD_LIST_EPISODES = 'list_episodes'
CMD_RAW_FEED = 'raw_feed'
CMD_VERSION = 'version'

SUB_CMDS = [
  CMD_DOWNLOAD,
  CMD_LIST_FEEDS,
  CMD_LIST_EPISODES,
  CMD_RAW_FEED,
  CMD_VERSION,
]

DEFAULT_CONFIG = str(Path.home().joinpath('.config', 'podcast_catcher', 'config.json'))

MAPPING_FILENAME = 'filename'

EXIT_SUCCESS = 0
EXIT_ERROR = 2


def build_argument_parser() -> ArgumentParser:
  """
  Create argument parser.
  """
  parser = ArgumentParser(
    description='podcast_catcher is an application to download podcasts.'
  )

  parser.add_argument(
    '--config',
    type=str,
    default=DEFAULT_CONFIG,
    help=f'Configuration file (default {DEFAULT_CONFIG})',
  )

  sub_parsers = parser.add_subparsers(
    required=True,
    dest='cmd',
    metavar=f'{{{','.join(SUB_CMDS)}}}',
  )

  sub_parsers.add_parser(
    CMD_DOWNLOAD,
  )

  sub_parsers.add_parser(
    CMD_LIST_FEEDS,
  )

  parser_list_episodes = sub_parsers.add_parser(
    CMD_LIST_EPISODES,
  )
  parser_list_episodes.add_argument(
    'feed_name',
    type=str,
    help='Name of the feed',
  )

  parser_raw_feed = sub_parsers.add_parser(
    CMD_RAW_FEED,
  )
  parser_raw_feed.add_argument(
    'feed_name',
    type=str,
    help='Name of the feed',
  )

  sub_parsers.add_parser(
    CMD_VERSION,
  )

  return parser


def download(config: ConfigFile) -> None:
  """
  Download feed enclosures not
  downloaded, yet.
  """
  loader = HttpLoader()
  replacer = Replacer()
  # Ensure base download folder exists
  download_dir = Path(config.settings().download_dir())
  if not download_dir.exists():
    download_dir.mkdir(parents=True)
  # For each feed:
  for config_feed in config.feeds():
    # Skip feeds not enabled
    if not config_feed.is_enabled:
      continue

    # Download feed
    feed_text = loader.get_feed(
      url=config_feed.url(),
      verify_https=config_feed.is_strict_https(),
    )

    # Parse feed
    parsed_feed = Feed(feed_text=feed_text)

    # Update replacer settings
    replacer.update_name(config_feed.name())
    replacer.update_feed(parsed_feed)

    # Filter out already downloaded episodes
    episode_tracker = EpisodeTracker(config, config_feed.name())
    already_downloaded = episode_tracker.already_downloaded_links()
    entries = [
      entry
      for entry in parsed_feed.entries()
      if entry.enclosure() not in already_downloaded
    ]
    # Filter out episodes older than X
    if config_feed.skip_older_than() is not None:
      entries = [
        entry for entry in entries if entry.published() >= config_feed.skip_older_than()
      ]
    # Sort entries from oldest to newest
    entries.sort(key=lambda e: e.published())
    print(f'{config_feed.name()} ({len(entries)} new entries)')

    # Ensure target download folder exists,
    # but only if at least one episode is
    # available for download
    target_dir = download_dir.joinpath(
      Path(config_feed.download_subdir()),
    )
    if len(entries) > 0 and not target_dir.exists():
      target_dir.mkdir(parents=True)

    index = 1
    tags = config.get_tags(config_feed)
    # Handle CRTL-C interrupts
    try:
      # For all episodes in feed:
      for entry in entries:
        # Update replacer
        replacer.update_entry(entry)

        filename = replacer.replace(config.get_filename(feed=config_feed))
        print(
          f'\t{index}/{len(entries)}: {entry.title()} ({entry.published()})... ',
          end='',
          flush=True,
        )
        target_file = target_dir.joinpath(Path(f'{filename}'))

        # Download enclosure
        loader.download(
          source=entry.enclosure(),
          target=target_file,
          verify_https=config_feed.is_strict_https(),
        )

        # Tag downloaded enclosure
        tagger = ID3Tagger(target_file)
        for key, value in tags.items():
          tagger.set(key, replacer.replace(value))
        tagger.set('genre', ', '.join(entry.tags()))
        tagger.save()

        # Update episode tracker
        episode_tracker.complete(entry)
        print('Done')
        index += 1
    except InterruptedError:
      # Silently abort via CRTL-C
      # (no stack trace).
      # Ensure the tracker is saved at the end
      episode_tracker.save()


def list_feeds(config: ConfigFile) -> None:
  """
  Show a list of feeds in config.
  """
  for feed in config.feeds():
    print(f'{feed.name()} ({feed.url()}) (enabled: {feed.is_enabled()})')
    episode_tracker = EpisodeTracker(config, feed.name())
    last_entry = episode_tracker.latest_entry()
    if last_entry is None:
      last_entry = '-'
    print(f'\tLast download: {last_entry}')


def list_episodes(config: ConfigFile, feed_name: str) -> None:
  """
  Name of the feed to show
  (available) episodes for.
  """
  loader = HttpLoader()
  for config_feed in config.feeds():
    if config_feed.name() == feed_name:
      episode_tracker = EpisodeTracker(config, config_feed.name())
      print(f'{config_feed.name()}')
      feed_text = loader.get_feed(
        url=config_feed.url(),
        verify_https=config_feed.is_strict_https(),
      )
      parsed_feed = Feed(feed_text=feed_text)
      # Sort entries from oldest to newest
      already_downloaded = episode_tracker.already_downloaded_links()
      entries = [
        entry
        for entry in parsed_feed.entries()
        if entry.enclosure() not in already_downloaded
      ]
      if config_feed.skip_older_than() is not None:
        entries = [
          entry
          for entry in entries
          if entry.published() >= config_feed.skip_older_than()
        ]
      entries.sort(key=lambda e: e.published())
      for entry in entries:
        print(f"\t'{entry.title()}' ({entry.link()}) from {entry.published()}")


def raw_feed(config: ConfigFile, feed_name: str) -> None:
  """
  Show raw RSS/ATOM feed
  fetched via HTTP(S).
  """
  loader = HttpLoader()
  for feed in config.feeds():
    if feed.name() == feed_name:
      feed_text = loader.get_feed(feed.url())
      print(feed_text)


def version() -> None:
  """
  Show applicaton version.
  """
  print('.'.join([str(v) for v in VERSION]))


def main_cli() -> None:
  """
  Structure of the application.

  Integrates the libraries and forwards
  the provided arguments.
  """
  parser: ArgumentParser = build_argument_parser()
  args = parser.parse_args()

  if args.cmd == CMD_VERSION:
    version()
    exit(EXIT_SUCCESS)

  try:
    config_json_factory = ConfigJsonFactory(args.config)
    config_json_factory.validate()
    config = config_json_factory.create_config()

    if args.cmd == CMD_DOWNLOAD:
      download(
        config,
      )
    elif args.cmd == CMD_LIST_FEEDS:
      list_feeds(config)
    elif args.cmd == CMD_LIST_EPISODES:
      list_episodes(
        config,
        args.feed_name,
      )
    elif args.cmd == CMD_RAW_FEED:
      raw_feed(
        config,
        args.feed_name,
      )
    else:
      print(f"Unknown argument '{args.cmd}'")
      exit(EXIT_ERROR)
  except PodcastCatcherError as e:
    print(e)
    exit(EXIT_ERROR)
  except KeyboardInterrupt:
    # Graceful CTRL-C interrupt
    exit(EXIT_SUCCESS)

  exit(EXIT_SUCCESS)


if __name__ == '__main__':
  main_cli()
