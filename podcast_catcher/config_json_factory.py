"""
Create a config instance
by loading a JSON file.
"""

from datetime import datetime
from json import JSONDecodeError, loads
from pathlib import Path

from config_file import ConfigFile
from exception import PodcastCatcherError
from jsonschema import Draft202012Validator, SchemaError, ValidationError, validate


class ConfigJsonFactory:
  """
  Loader and validator
  for JSON config files.
  """

  CONFIG_SCHEMA = Path.joinpath(Path(__file__).parent.absolute(), 'config.schema.json')

  KEY_SETTINGS = 'settings'
  KEY_DOWNLOAD_DIR = 'download_dir'
  KEY_DATA_DIR = 'data_dir'
  KEY_FILENAME = 'filename'
  KEY_TAGS = 'tags'

  KEY_REPLACE = 'replace'
  KEY_WITH = 'with'

  KEY_FEEDS = 'feeds'
  KEY_NAME = 'name'
  KEY_URL = 'url'
  KEY_STRICT_HTTPS = 'strict_https'
  KEY_ENABLED = 'enabled'
  KEY_SKIP_ODER_THAN = 'skip_older_than'
  KEY_DOWNLOAD_SUBDIR = 'download_subdir'

  def __init__(self, config_filename: str) -> bool:
    """
    CTOR, load config schema and file
    content on class initialization.
    """
    try:
      with open(self.CONFIG_SCHEMA) as f:
        self.__config_schema = loads(f.read())
      with open(config_filename) as f:
        self.__config_data = loads(f.read())
    except FileNotFoundError as e:
      raise PodcastCatcherError(f'Config factory error: {e}') from e
    except JSONDecodeError as e:
      raise PodcastCatcherError(f'Config factory JSON parser error: {e}') from e

  def validate(self) -> bool:
    """
    Validate config against
    JSON schema.
    """
    try:
      validate(
        instance=self.__config_data,
        schema=self.__config_schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
      )
    except SchemaError as e:
      raise PodcastCatcherError(f'JSON schema error: {e}') from e
    except ValidationError as e:
      raise PodcastCatcherError(f'JSON config validation error: {e}') from e
    return True

  @staticmethod
  def __get_optional(
    data: dict[str, any], key: str, default: any, func: None = None
  ) -> any:
    """
    Try to get key from data. If key
    does not exist, return default instead.
    """
    if key in data:
      if func:
        return func(data[key])
      return data[key]
    return default

  def create_config(self) -> ConfigFile:
    """
    Create Config instance from
    loaded JSON config.
    """
    settings_tags = {}
    if self.KEY_TAGS in self.__config_data[self.KEY_SETTINGS]:
      for entry in self.__config_data[self.KEY_SETTINGS][self.KEY_TAGS]:
        settings_tags[entry[self.KEY_REPLACE]] = entry[self.KEY_WITH]

    settings = ConfigFile.Settings(
      download_dir=self.__config_data[self.KEY_SETTINGS][self.KEY_DOWNLOAD_DIR],
      data_dir=self.__config_data[self.KEY_SETTINGS][self.KEY_DATA_DIR],
      filename=self.__config_data[self.KEY_SETTINGS][self.KEY_FILENAME],
      tags=settings_tags,
    )
    feeds = []
    if self.KEY_FEEDS in self.__config_data:
      for entry in self.__config_data[self.KEY_FEEDS]:
        feed_tags = {}
        if self.KEY_TAGS in entry:
          for sub_entry in entry[self.KEY_TAGS]:
            feed_tags[sub_entry[self.KEY_REPLACE]] = sub_entry[self.KEY_WITH]

        feed = ConfigFile.Feed(
          name=entry[self.KEY_NAME],
          url=entry[self.KEY_URL],
          strict_https=self.__get_optional(entry, self.KEY_STRICT_HTTPS, True),
          enabled=self.__get_optional(entry, self.KEY_ENABLED, True),
          download_subdir=self.__get_optional(entry, self.KEY_DOWNLOAD_SUBDIR, None),
          skip_older_than=self.__get_optional(
            entry, self.KEY_SKIP_ODER_THAN, None, func=datetime.fromisoformat
          ),
          filename=self.__get_optional(entry, self.KEY_FILENAME, None),
          tags=feed_tags,
        )
        feeds.append(feed)

    return ConfigFile(settings, feeds)
