"""
Flexible string replacer class.
"""

from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlparse

from exception import PodcastCatcherError
from feed import Entry, Feed


class Replacer:
  """
  Replace strings based on feed/entry
  properties.
  """

  PLACEHOLDER_TOKEN = '%'
  PLACEHOLDER_ITEMS: dict[str, Callable[[str, Feed, Entry], str]] = {
    # Config properties
    f'{PLACEHOLDER_TOKEN}config_name{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: name,
    # Feed properties
    f'{PLACEHOLDER_TOKEN}feed_title{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: feed.title(),
    f'{PLACEHOLDER_TOKEN}feed_subtitle{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: feed.subtitle(),
    f'{PLACEHOLDER_TOKEN}feed_description{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: feed.description(),
    f'{PLACEHOLDER_TOKEN}feed_link{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: feed.link(),
    f'{PLACEHOLDER_TOKEN}feed_date{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: feed.updated().strftime('%Y%m%d'),
    f'{PLACEHOLDER_TOKEN}feed_datetime{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: feed.updated().strftime('%Y%m%d-%H%M%S'),
    # Entry properties
    f'{PLACEHOLDER_TOKEN}episode_date{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: entry.published().strftime('%Y%m%d'),
    f'{PLACEHOLDER_TOKEN}episode_datetime{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: entry.published().strftime('%Y%m%d-%H%M%S'),
    f'{PLACEHOLDER_TOKEN}episode_url_basename{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: Path(urlparse(entry.enclosure()).path).stem,
    f'{PLACEHOLDER_TOKEN}episode_url_extension{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: Path(urlparse(entry.enclosure()).path).suffix,
    f'{PLACEHOLDER_TOKEN}episode_title{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: entry.title(),
    f'{PLACEHOLDER_TOKEN}episode_author{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: entry.author(),
    f'{PLACEHOLDER_TOKEN}episode_summary{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: entry.summary(),
    f'{PLACEHOLDER_TOKEN}episode_link{PLACEHOLDER_TOKEN}': lambda name,
    feed,
    entry: entry.link(),
  }

  def __init__(self):
    """
    CTOR for replacer class.
    Sets base config.
    """
    self.__name = None
    self.__feed = None
    self.__entry = None

  def update_name(self, name: str) -> None:
    """
    Update feed name.
    """
    self.__name = name
    self.__feed = None
    self.__entry = None

  def update_feed(self, feed: Feed) -> None:
    """
    Update feed properties.
    """
    self.__feed = feed
    self.__entry = None

  def update_entry(self, entry: Entry) -> None:
    """
    Update entry properties.
    """
    self.__entry = entry

  def replace(self, input: str) -> str:
    """
    Replace %-enclosed parts in
    string with properties of the
    feed entry.
    """
    if self.__name is None or self.__feed is None or self.__entry is None:
      raise PodcastCatcherError(
        f'Replacer sources not all set: Name: {self.__name}, feed: {self.__feed},'
        f'entry: {self.__entry}'
      )
    for key, value in self.PLACEHOLDER_ITEMS.items():
      input = input.replace(
        key, value(name=self.__name, feed=self.__feed, entry=self.__entry)
      )
    return input
