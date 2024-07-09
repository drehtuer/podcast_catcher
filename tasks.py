"""
python-invoke tasks
https://docs.pyinvoke.org/en/stable.

Both aliases of commands and documenting them
in the same step.
"""

from invoke import context, task

PYTHON_BIN = 'python3'
DOCUTILS_BIN = 'docutils'

DIST_DIR = 'dist'
EGG_INFO_DIR = 'podcast_catcher.egg-info'

MAIN_CLI = 'podcast_catcher/main_cli.py'
README_RST = 'README.rst'
README_HTML = 'README.html'


def ctx_run(ctx: context, cmd: list[str]) -> None:
  """
  Boiler plate function to flatten
  the command list and run the command
  in the current context.
  """
  ctx.run(' '.join(cmd))


def opt_config(config: str | None) -> list[str]:
  """
  If config is provided, return it with is as parameter flag.
  """
  if config is None:
    return []
  return ['--config', config]


@task
def build(ctx: context) -> None:
  """
  Build a python package.
  """
  cmd: list[str] = [
    PYTHON_BIN,
    '-m',
    'build',
  ]
  ctx_run(ctx, cmd)


@task
def doc(ctx: context) -> None:
  """
  Build documentation.
  """
  cmd: list[str] = [
    DOCUTILS_BIN,
    README_RST,
    README_HTML,
  ]
  ctx_run(ctx, cmd)


@task
def clean(ctx: context) -> None:
  """
  Delete build results.
  """
  cmd: list[str] = [
    'rm',
    '-rf',
    DIST_DIR,
    EGG_INFO_DIR,
    README_HTML,
  ]
  ctx_run(ctx, cmd)


@task
def download(ctx: context, config: str = None) -> None:
  """
  Run download.
  """
  cmd: list[str] = [
    PYTHON_BIN,
    MAIN_CLI,
    *opt_config(config),
    'download',
  ]
  ctx_run(ctx, cmd)


@task
def list_feeds(ctx: context, config: str = None) -> None:
  """
  Run download.
  """
  cmd: list[str] = [
    PYTHON_BIN,
    MAIN_CLI,
    *opt_config(config),
    'list_feeds',
  ]
  ctx_run(ctx, cmd)


@task
def list_episodes(ctx: context, feed: str, config: str = None) -> None:
  """
  Run download.
  """
  cmd: list[str] = [
    PYTHON_BIN,
    MAIN_CLI,
    *opt_config(config),
    'list_episodes',
    f'"{feed}"',
  ]
  ctx_run(ctx, cmd)


@task
def raw_feed(ctx: context, feed: str, config: str = None) -> None:
  """
  Run download.
  """
  cmd: list[str] = [
    PYTHON_BIN,
    MAIN_CLI,
    *opt_config(config),
    'raw_feed',
    f'"{feed}"',
  ]
  ctx_run(ctx, cmd)


@task
def version(ctx: context) -> None:
  """
  Run download.
  """
  cmd: list[str] = [
    PYTHON_BIN,
    MAIN_CLI,
    'version',
  ]
  ctx_run(ctx, cmd)
