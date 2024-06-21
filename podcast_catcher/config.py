"""
Read configuration from a JSON file.
"""

import json


class Config:
  """
  Providing configuration for the application.
  """

  def __init__(self, filename: str) -> None:
    """
    CTOR for Config class.

    RAII, configuration is only loaded once when
    the class is instantiated and remains immutable.
    """
    with open(filename, encoding='utf-8') as fp:
      self.__config = json.load(fp)
