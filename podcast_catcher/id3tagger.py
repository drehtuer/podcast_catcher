"""
Add/modift id3 tags in media files.
"""

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import MutagenError
from mutagen import File


class ID3Tagger:
  """
  Wrap ID3 tag actions.
  """

  def __init__(self, media_file: str):
    """
    CTOR for id3tag.
    """
    try:
      self.__mediafile: EasyID3 = EasyID3(media_file)
    except MutagenError as e:
      print(f'\n\t\tException: {e}')
      # File has no ID3 tags, create the tags
      # first before loading it as EasyID3
      file = File(media_file, easy=True)
      file.add_tags()
      file.save(media_file, v1=2)
      self.__mediafile: EasyID3 = EasyID3(media_file)

  def save(self) -> None:
    """
    Save tags to media file.
    """
    self.__mediafile.save()

  def set(self, tag: str, value: str) -> None:
    """
    Set ID3 tags.
    """
    self.__mediafile[tag] = value

  def info(self) -> str:
    """
    Return stream information from mediafile.
    """
    return self.__mediafile.pprint()

  def valid_tags(self) -> list[str]:
    """
    Get a list of valid tag keys.
    """
    return [key for key in EasyID3.valid_keys]
