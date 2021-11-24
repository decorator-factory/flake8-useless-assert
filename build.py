from pathlib import Path

import toml

from flake8_useless_assert import UselessAssert


plugin_version = UselessAssert.version

pyproject_config = toml.load(Path("pyproject.toml"))
pyproject_version = pyproject_config["tool"]["poetry"]["version"]


if plugin_version != pyproject_version:
    raise RuntimeError(
        "Versions in `setup.py` ({0}) and `pyproject.toml` ({1}) don't match!"
        .format(plugin_version, pyproject_version)
    )
