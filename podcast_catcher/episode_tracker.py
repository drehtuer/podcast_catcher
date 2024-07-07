"""
Manage state which episodes were
already downloaded.
"""

from json import dumps, loads
from pathlib import Path

from config_file import ConfigFile
from feed import Entry


class EpisodeTracker:
  """
  Keep track of already downloaded
  episodes per feed.
  """

  COMPLETED_FILES_EXTENSION = 'json'

  EPISODE_TITLE = 'title'
  EPISODE_URL = 'url'
  EPISODE_PUBLISHED = 'published'

  def __init__(self, config: ConfigFile, feed_name: str):
    """
    CTOR for EpisodeTracker.
    """
    data_dir = Path(config.settings().data_dir())
    # Ensure folder structure for data
    # dir exists. If not, create it.
    if not data_dir.exists():
      data_dir.mkdir(parents=True)
    self.__completed_downloads: list[dict[str, str]] = []
    self.__completed_file = data_dir.joinpath(
      f'{feed_name}.{self.COMPLETED_FILES_EXTENSION}'
    )
    try:
      with open(self.__completed_file) as fd:
        self.__completed_downloads = loads(fd.read())
    except FileNotFoundError:
      # File not yet created or deleted,
      # keep empty array and ignore exception.
      pass

  def complete(self, entry: Entry) -> None:
    """
    Register completed download
    of an episode.
    """
    self.__completed_downloads.append(
      {
        self.EPISODE_TITLE: entry.title(),
        self.EPISODE_URL: entry.enclosure(),
        self.EPISODE_PUBLISHED: str(entry.published()),
      }
    )

  def save(self) -> None:
    """
    Save current download state.
    """
    with open(self.__completed_file, 'w') as fd:
      fd.write(dumps(self.__completed_downloads))

  def already_downloaded_links(self) -> list[str]:
    """
    List of already downloaded episodes (URL links).
    """
    return [x[self.EPISODE_URL] for x in self.__completed_downloads]

  def latest_entry(self) -> str | None:
    """
    Get latest published and downloaded entry.
    """
    if len(self.__completed_downloads) > 0:
      sorted_list = sorted(
        self.__completed_downloads,
        key=lambda e: e[self.EPISODE_PUBLISHED],
      )
      # Return last entry, which is the newest entry.
      return sorted_list[-1]
    return None
