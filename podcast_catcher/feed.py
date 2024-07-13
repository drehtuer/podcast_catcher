"""
Abstraction of a feed.
"""

from datetime import UTC, datetime
from sys import stderr
from time import mktime

import feedparser


class Entry:
  """
  Entry within a feed.
  """

  def __init__(
    self,
    author: str,
    enclosure: str,
    link: str | None,
    published: datetime,
    summary: str,
    title: str,
    tags: list[str],
  ):
    """
    CTOR for entry element.
    """
    self.__author = author
    self.__enclosure = enclosure
    self.__link = link if link is not None else ''
    self.__published = published
    self.__summary = summary
    self.__title = title
    self.__tags = tags

  def author(self) -> str:
    """
    Return author of the entry.
    """
    return self.__author

  def enclosure(self) -> str:
    """
    Enclosure of the entry.
    (The link to the downloadable
    audio/video file).
    """
    return self.__enclosure

  def published(self) -> datetime:
    """
    Time the entry was published.
    """
    return self.__published

  def summary(self) -> str:
    """
    Summary of the entry.
    """
    return self.__summary

  def title(self) -> str:
    """
    Title of the entry.
    """
    return self.__title

  def tags(self) -> list[str]:
    """
    Return list of tags.
    """
    return self.__tags

  def link(self) -> str:
    """
    URL linking to the episode.
    """
    return self.__link

  def __repr__(self) -> str:
    """
    Show string representation
    of the entry instance.
    """
    items = [
      f"author: '{self.author()}'",
      f"title: '{self.title()}'",
      f"published: '{self.published()}'",
      f"enclosure: '{self.enclosure()}'",
      f"link: '{self.link()}'",
      f"summary: '{self.summary()}'",
      f"tags: '{self.tags()}'",
    ]
    return f'{{{', '.join(items)}}}'


class Feed:
  """
  Actions on a feed.
  """

  TAG_AUTHOR = 'author'
  TAG_TERM_KEY = 'term'
  TAG_TAGS = 'tags'
  TAG_LINK = 'link'
  TAG_UPDATED_PARSED = 'updated_parsed'
  TAG_PUBLISHED_PARSED = 'published_parsed'

  def __init__(self, feed_text: str):
    """
    COTR: Parse feed from string.
    """
    parsed: feedparser.FeedParserDict = feedparser.parse(feed_text)
    self.__title = parsed.feed.title
    self.__subtitle = parsed.feed.subtitle
    self.__description = parsed.feed.description
    if self.TAG_LINK in parsed.feed:
      self.__link = parsed.feed.link
    else:
      self.__link = None
    # feedparser uses the fallback to 'published_parsed' if
    # 'updated_parsed' doesn't exist, but this mapping is
    # temporarily and may be removed in the future. Mapping
    # is added here as well to be future-proof.
    if self.TAG_UPDATED_PARSED in parsed.feed:
      self.__updated = datetime.fromtimestamp(
        timestamp=mktime(parsed.feed.updated_parsed),
        tz=UTC,
      )
    elif self.TAG_PUBLISHED_PARSED in parsed.feed:
      self.__updated = datetime.fromtimestamp(
        timestamp=mktime(parsed.feed.published_parsed),
        tz=UTC,
      )
    else:
      # TODO: Better solution?
      self.__updated = datetime.now(tz=UTC)

    self.__entries: list[Entry] = []
    for entry in parsed.entries:
      if len(entry.enclosures) < 1:
        print(
          f"Feed '{self.title()}' episode '{entry.title}' has no enclosures"
          ' -> skipping episode.',
          file=stderr,
        )
        continue
      author = entry.author if self.TAG_AUTHOR in entry else entry.title
      enclosure = entry.enclosures[0].href
      if len(entry.enclosures) > 1:
        # TODO: Support preferred enclosure format
        print(f"Feed '{self.title()}' supports multiple encosure options", file=stderr)
      tags = []
      if self.TAG_TAGS in entry:
        tags = [term[self.TAG_TERM_KEY] for term in entry.tags]
      link = entry.link if self.TAG_LINK in entry else None
      self.__entries.append(
        Entry(
          author=author,
          enclosure=enclosure,
          published=datetime.fromtimestamp(
            timestamp=mktime(entry.published_parsed),
            tz=UTC,
          ),
          summary=entry.summary,
          # tag scheme and label are ignored
          tags=tags,
          title=entry.title,
          link=link,
        )
      )

  def title(self) -> str:
    """
    Return title of feed.
    """
    return self.__title

  def subtitle(self) -> str:
    """
    Return subtitle of feed.
    """
    return self.__subtitle

  def description(self) -> str:
    """
    Return description of feed.
    """
    return self.__description

  def link(self) -> str | None:
    """
    Return link to the feed source.
    """
    return self.__link

  def updated(self) -> datetime:
    """
    Last time the feed was updated.
    """
    return self.__updated

  def entries(self, newer_than: datetime | None = None) -> list[Entry]:
    """
    Return a list of entries in this feed.
    Optional: filter result to show only
    feeds newer than given date.
    """
    if newer_than is not None:
      return [entry for entry in self.__entries if entry.published() >= newer_than]
    else:
      return self.__entries

  def __repr__(self) -> str:
    """
    Return string representation
    of a feed.
    """
    items = [
      f"title: '{self.title()}'",
      f"subtitle: '{self.subtitle()}'",
      f"description: '{self.description()}'",
      f"link: '{self.link()}'",
      f"updated: '{self.updated()}'",
      f"episodes: '{self.entries()}'",
    ]
    return f'{{{', '.join(items)}}}'
