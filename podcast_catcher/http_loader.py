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
    try:
      request = requests.get(url, verify=verify_https)
      if request.status_code != 200:
        raise PodcastCatcherError(f'HTTP error for feed {url}: {request.status_code}')
    except requests.ConnectTimeout as e:
      raise PodcastCatcherError(f'HTTP timeout for feed {url}: {e}') from None
    return request.text

  def download(self, source: str, target: str, verify_https: bool = True) -> None:
    """
    Download from source and write
    to target.
    """
    request = requests.get(source, verify=verify_https)
    with open(target, 'wb') as fd:
      for chunk in request.iter_content(chunk_size=4096):
        fd.write(chunk)
