"""
Read configuration from a JSON file.
"""

from datetime import datetime


class ConfigFile:
  """
  Providing configuration for the application.
  """

  class Settings:
    """
    Global configration settings.
    """

    def __init__(
      self, download_dir: str, data_dir: str, filename: str, tags: dict[str, str]
    ):
      """
      CTOR for Settings class.
      """
      self.__download_dir = download_dir
      self.__data_dir = data_dir
      self.__filename = filename
      self.__tags = tags

    def download_dir(self) -> str:
      """
      Access to download_dir value.
      """
      return self.__download_dir

    def data_dir(self) -> str:
      """
      Access to data_dir value.
      """
      return self.__data_dir

    def filename(self) -> str:
      """
      Access to filename.
      """
      return self.__filename

    def tags(self) -> dict[str, str]:
      """
      Access to tag dict.
      """
      return self.__tags

    def __repr__(self) -> str:
      """
      Return string representation.
      """
      items = [
        f"'download_dir': '{self.download_dir()}'",
        f"'data_dir': '{self.data_dir()}'",
        f"'filename': '{self.filename()}'",
        f"'tags': {self.tags()}",
      ]
      return f'{{{', '.join(items)}}}'

  class Feed:
    """
    Feed configuration.
    """

    def __init__(
      self,
      name: str,
      url: str,
      strict_https: bool,
      enabled: bool,
      download_subdir: str | None,
      skip_older_than: datetime,
      filename: str | None,
      tags: dict[str, str],
    ):
      """
      CTOR for Feed class.
      """
      self.__name = name
      self.__url = url
      self.__strict_https = strict_https
      self.__enabled = enabled
      if download_subdir is not None:
        self.__download_subdir = download_subdir
      else:
        self.__download_subdir = name
      self.__skip_older_than = skip_older_than
      self.__filename = filename
      self.__tags = tags

    def name(self) -> str:
      """
      Return reference to name.
      """
      return self.__name

    def url(self) -> str:
      """
      Return reference to URL.
      """
      return self.__url

    def is_strict_https(self) -> bool:
      """
      Return if feed should use strict HTTPS checks.
      """
      return self.__strict_https

    def is_enabled(self) -> bool:
      """
      Return if the feed is enabled or not.
      """
      return self.__enabled

    def skip_older_than(self) -> datetime:
      """
      Return reference to skip_older_than.
      """
      return self.__skip_older_than

    def tags(self) -> dict[str, str]:
      """
      Return reference to tags.
      """
      return self.__tags

    def filename(self) -> str:
      """
      Return filename for the feed.
      """
      return self.__filename

    def download_subdir(self) -> str:
      """
      Return reference to download_subdir.
      If download_subdir is not set in feed config,
      it uses the name instead.
      """
      return self.__download_subdir

    def __repr__(self) -> str:
      """
      Return string representation.
      """
      items = [
        f"'name': '{self.name()}'",
        f"'url': '{self.url()}'",
        f"'strict_https': '{self.is_strict_https()}'",
        f"'enabled': '{self.is_enabled()}'",
        f"'skip_older_than': '{self.skip_older_than()}'",
        f"'download_subdir': '{self.download_subdir()}'",
        f"'filename': '{self.filename()}'",
        f"'tags': {self.tags()}",
      ]
      return f'{{{', '.join(items)}}}'

  def __init__(self, settings: Settings, feeds: list[Feed]) -> None:
    """
    CTOR for Config class.
    """
    self.__settings = settings
    self.__feeds = feeds

  def settings(self) -> Settings:
    """
    Return reference to global settings.
    """
    return self.__settings

  def feeds(self) -> list[Feed]:
    """
    Return reference to list of feeds.
    """
    return self.__feeds

  def get_filename(self, feed: Feed) -> str:
    """
    Get filename for feed. If a filename
    entry exists for the feed, use it.
    Otherwise fall back to settings filename.
    """
    if feed.filename() is not None:
      return feed.filename()
    return self.settings().filename()

  def get_tags(self, feed: Feed) -> dict[str, str]:
    """
    Get joined dict of all tags.
    """
    tags = {}
    for key, value in self.settings().tags().items():
      tags[key] = value
    for key, value in feed.tags().items():
      tags[key] = value
    return tags

  def __repr__(self) -> str:
    """
    Return string representation.
    """
    items = [
      f"'settings': {self.settings()}",
      f"'feeds': {self.feeds()}",
    ]
    return ', '.join(items)
