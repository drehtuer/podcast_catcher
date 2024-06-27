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

from config_factory import ConfigFactory
from exception import PodcastCatcherError

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

DEFAULT_CONFIG = str(
  Path.joinpath(Path.home(), '.config', 'podcast_catcher', 'config.json')
)

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
  parser.add_argument(
    '--verbose',
    action='store_true',
    help='Enable verbose output',
  )

  sub_parsers = parser.add_subparsers(
    required=True,
    dest='cmd',
    metavar=f'{{{','.join(SUB_CMDS)}}}',
  )

  parser_download = sub_parsers.add_parser(
    CMD_DOWNLOAD,
  )
  parser_download.add_argument(
    '--dry-run',
    action='store_true',
    help="Check for updates, but don't download any files",
  )

  sub_parsers.add_parser(
    CMD_LIST_FEEDS,
  )

  sub_parsers.add_parser(
    CMD_LIST_EPISODES,
  )

  sub_parsers.add_parser(
    CMD_RAW_FEED,
  )

  sub_parsers.add_parser(
    CMD_VERSION,
  )

  return parser


def download(dry_run: bool) -> None:
  pass


def list_feeds() -> None:
  pass


def list_episodes() -> None:
  pass


def raw_feed() -> None:
  pass


def version() -> None:
  pass


def main_cli() -> None:
  """
  Structure of the application.

  Integrates the libraries and forwards
  the provided arguments.
  """
  parser: ArgumentParser = build_argument_parser()
  args = parser.parse_args()

  try:
    config_factory = ConfigFactory(args.config)
    config_factory.validate()
    config = config_factory.create_config()
    print(config)

    if args.cmd == CMD_DOWNLOAD:
      download(args.dry_run)
    elif args.cmd == CMD_LIST_FEEDS:
      list_feeds()
    elif args.cmd == CMD_LIST_EPISODES:
      list_episodes()
    elif args.cmd == CMD_RAW_FEED:
      raw_feed()
    elif args.cmd == CMD_VERSION:
      version()
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
