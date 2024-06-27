"""
Read configuration from a JSON file.
"""

from datetime import datetime


class Config:
  """
  Providing configuration for the application.
  """

  class Settings:
    """
    Global configration settings.
    """

    def __init__(self, download_dir: str, data_dir: str, mappings: dict[str, str]):
      """
      CTOR for Settings class.
      """
      self.__download_dir = download_dir
      self.__data_dir = data_dir
      self.__mappings = mappings

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

    def mappings(self) -> dict[str, str]:
      """
      Access to mappings dict.
      """
      return self.__mappings

    def __repr__(self) -> str:
      """
      Return string representation.
      """
      items = [
        f"'download_dir': '{self.download_dir()}'",
        f"'data_dir': '{self.data_dir()}'",
        f"'mappings': {self.mappings()}",
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
      download_subdir: str | None,
      skip_older_than: datetime,
      mappings: dict[str, str],
    ):
      """
      CTOR for Feed class.
      """
      self.__name = name
      self.__url = url
      self.__strict_https = strict_https
      if download_subdir is not None:
        self.__download_subdir = download_subdir
      else:
        self.__download_subdir = name
      self.__download_subdir = download_subdir
      self.__skip_older_than = skip_older_than
      self.__mappings = mappings

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

    def skip_older_than(self) -> datetime:
      """
      Return reference to skip_older_than.
      """
      return self.__skip_older_than

    def mappings(self) -> dict[str, str]:
      """
      Return reference to mappings.
      """
      return self.__mappings

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
        f"'skip_older_than': '{self.skip_older_than()}'",
        f"'download_subdir': '{self.download_subdir()}'",
        f"'mappings': {self.mappings()}",
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

  def get_mapping(self, feed: Feed, mapping_key: str) -> str:
    """
    Get mapping value for key. Check if feed overrides
    global mappings.
    Throws KeyError is mapping_key is in neither dict.
    """
    if mapping_key in feed.mappings:
      return feed.mappings[mapping_key]
    return self.settings().mappings()[mapping_key]

  def __repr__(self) -> str:
    """
    Return string representation.
    """
    items = [
      f"'settings': {self.settings()}",
      f"'feeds': {self.feeds()}",
    ]
    return ', '.join(items)
