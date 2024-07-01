"""
Handle HTTP(S) requests to access
the RSS/ATOM feed.
"""

import requests
from exception import PodcastCatcherError


class HttpLoader:
  """
  Wrapper around the requests library.
  While feedparser can download via HTTP(S),
  it offers fewer options than a dedicated HTTP(S)
  library.
  """

  def get_feed(self, url: str, verify_https: bool = True) -> str:
    """
    Fetch a feed via HTTP(S).
    """
    request = requests.get(url, verify=verify_https)
    if request.status_code != 200:
      raise PodcastCatcherError(f'HTTP error: {request.status_code}')
    return request.text
