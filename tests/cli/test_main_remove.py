# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
import pytest

from conda.exceptions import PackagesNotFoundError
from conda.gateways.disk.delete import path_is_clean
from conda.testing import CondaCLIFixture, TmpEnvFixture
from conda.testing.integration import PYTHON_BINARY, package_is_installed


def test_remove_all(tmp_env: TmpEnvFixture, conda_cli: CondaCLIFixture):
    with tmp_env("python") as prefix:
        assert (prefix / PYTHON_BINARY).exists()
        assert package_is_installed(prefix, "python")

        # regression test for #2154
        with pytest.raises(PackagesNotFoundError) as exc:
            conda_cli("remove", f"--prefix={prefix}", "python", "foo", "numpy", "--yes")
        exception_string = repr(exc.value)
        assert "PackagesNotFoundError" in exception_string
        assert "- numpy" in exception_string
        assert "- foo" in exception_string

        conda_cli("remove", f"--prefix={prefix}", "--all", "--yes")
        assert path_is_clean(prefix)


def test_remove_all_keep_env(tmp_env: TmpEnvFixture, conda_cli: CondaCLIFixture):
    with tmp_env("python") as prefix:
        assert (prefix / PYTHON_BINARY).exists()
        assert package_is_installed(prefix, "python")

        conda_cli("remove", f"--prefix={prefix}", "--all", "--keep-env", "--yes")
        assert not path_is_clean(prefix)
