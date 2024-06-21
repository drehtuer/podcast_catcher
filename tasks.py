"""
python-invoke tasks
https://docs.pyinvoke.org/en/stable.

Both aliases of commands and documenting them
in the same step.
"""

from invoke import context, task

PYTHON_BIN='python3'
PIP_BIN='pip'
VENV_DIR='venv'
REQUIREMENTS_TXT='requirements.txt'

def ctx_run(ctx: context, cmd: list[str]) -> None:
  """
  Boiler plate function to flatten
  the command list and run the command
  in the current context.
  """
  ctx.run(' '.join(cmd))

@task
def venv(ctx: context) -> None:
  """
  Setup venv.

  Other virtual environment should
  work as well, you should know how
  to set them up in that case.

  Running `invoke` requires either
  installing the package from the
  host's package manager or `pip`.
  """
  cmd: list[str] = [
    PYTHON_BIN,
    '-m',
    'venv',
    VENV_DIR
  ]
  ctx_run(ctx, cmd)

  cmd = [
    PIP_BIN,
    'install',
    '-r',
    REQUIREMENTS_TXT
  ]
  ctx_run(ctx, cmd)

@task
def download(ctx: context) -> None:
  cmd: list[str] = [
    PYTHON_BIN,

  ]
