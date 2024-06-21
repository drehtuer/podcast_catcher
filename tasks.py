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
def download(ctx: context) -> None:
  cmd: list[str] = [
    PYTHON_BIN,

  ]
