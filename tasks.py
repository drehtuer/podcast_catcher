"""
python-invoke tasks
https://docs.pyinvoke.org/en/stable.

Both aliases of commands and documenting them
in the same step.
"""

from invoke import context, task

PYTHON_BIN = 'python3'

DIST_DIR = 'dist'
EGG_INFO_DIR = 'podcast_catcher.egg-info'


def ctx_run(ctx: context, cmd: list[str]) -> None:
  """
  Boiler plate function to flatten
  the command list and run the command
  in the current context.
  """
  ctx.run(' '.join(cmd))


@task
def build(ctx: context) -> None:
  """
  Build a python package.
  """
  cmd: list[str] = [PYTHON_BIN, '-m', 'build']
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
  ]
  ctx_run(ctx, cmd)
