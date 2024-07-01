"""
Abstraction of a feed.
"""

import feedparser


class Feed:
  """
  Actions on a feed.
  """

  def parse(self, text: str):
    """
    Parse feed from string.
    """
    d = feedparser.parse(text)
    for f in d.entries:
      print(f.title)
