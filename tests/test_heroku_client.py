"""
Test execution matters as app creation is intended first and app deletion should
be the last test to execute.
"""

from heroku_py.heroku_client import HerokuClient

hk = HerokuClient()
git_url = "https://github.com/elfkuzco/heroku-py-testing-repo"
tarball_url = (
    "https://github.com/elfkuzco/heroku-py-testing-repo/raw/beta/heroku_demo.tar.gz"
)
repo_sha = str(hash(git_url)).strip("-")
app_name = "wonder-beetle-" + repo_sha[:6]
new_name = f"ravenous-eagle-{repo_sha[:6]}"


def test_create_app():
    app = hk.create_app(app_name)
    assert app["name"] == app_name


def test_get_app_info():
    app = hk.get_app_info(app_name)
    assert app["name"] == app_name


def test_build_from_source():
    build_details = hk.build_from_source(app_name, tarball_url)
    assert build_details["status"] in ["succeeded", "failed"]


def test_build_from_git():
    build_details = hk.build_from_git(app_name, git_url)
    assert build_details["status"] in ["succeeded", "failed"]


def test_update_app():
    maintenance = False
    app = hk.update_app(app_name, new_name=new_name, maintenance=maintenance)
    assert app["name"] == new_name
    assert app["maintenance"] == maintenance


def test_create_config():
    config_vars = hk.create_config(new_name, DEBUG=True, SECRET_KEY="xxxxxxxxxxxx")
    assert config_vars["DEBUG"] == "true"
    assert config_vars["SECRET_KEY"] == "xxxxxxxxxxxx"


def test_update_config():
    config_vars = hk.update_config(new_name, SECRET_KEY="some_random_key")
    assert config_vars["SECRET_KEY"] == "some_random_key"


def test_delete_config():
    config_vars = hk.delete_config(new_name, "DEBUG")
    assert "DEBUG" not in config_vars


def test_delete_app():
    app = hk.delete_app(new_name)
    assert app["name"] == new_name
