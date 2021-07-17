import requests
import re
import time
from .constants import HEROKU_API_URL
from . import authorization
from .utilities import get_commit_sha, handle_error
from .exceptions import HerokuException


class HerokuClient:
    def __init__(self, api_key=None):
        """
        Create an instance of a heroku client for making API requests.
        If api_key is None, will try to load API key from .netrc file in
        current user's home directory or load from environment variable
        $HEROKU_API_KEY.
        """

        if api_key is None:
            self.HEROKU_API_KEY = authorization.get_api_key()
        else:
            self.HEROKU_API_KEY = api_key

        self.headers = {
            "Accept": "application/vnd.heroku+json; version=3",
            "Authorization": f"Bearer {self.HEROKU_API_KEY}",
        }

    def create_app(self, app_name):
        """
        Creates an app on Heroku.
        app_name should conform to the pattern ^[a-z][a-z0-9-]{1,28}[a-z0-9]$ as
        specified in the Heroku API.
        Returns the response from the server.
        """

        name_regex = re.compile(r"^[a-z][a-z0-9-]{1,28}[a-z0-9]$")
        if name_regex.search(app_name) is None:
            raise ValueError(
                "Improper name configuration. Names must begin with an alphabet, can consist of numbers and hyphens as seperators."
            )
        payload = {"name": app_name}
        response = requests.post(HEROKU_API_URL, headers=self.headers, json=payload)
        handle_error(response)
        return response.json()

    def get_app_info(self, app_name_or_id):
        """
        Gets the details about an app given its app_name_or_id.
        """
        response = requests.get(
            f"{HEROKU_API_URL}/{app_name_or_id}", headers=self.headers
        )
        handle_error(response)
        return response.json()

    def delete_app(self, app_name_or_id):
        """
        Deletes an app given its app_name_or_id.
        """
        _headers = self.headers.copy()
        _headers["Content-Type"] = "application/json"

        response = requests.delete(
            f"{HEROKU_API_URL}/{app_name_or_id}", headers=_headers
        )
        handle_error(response)
        return response.json()

    def list_apps(self):
        """
        List existing apps.
        """
        response = requests.get(f"{HEROKU_API_URL}", headers=self.headers)
        handle_error(response)
        return [app["name"] for app in response.json()]

    def update_app(self, app_name_or_id, *, new_name=None, maintenance=None):
        """
        Update an existing app.
            new_name: The new name for the app.
            maintenance: A boolean indicating whether to put the app in maintenance mode.
        """
        payload = {}
        if new_name is not None:
            payload["name"] = new_name
        if maintenance is not None:
            if not isinstance(maintenance, bool):
                raise TypeError(
                    f"maintenance expected to be of type 'bool' but got {type(maintenance)}"
                )
            payload["maintenance"] = maintenance

        if payload.keys():
            response = requests.patch(
                f"{HEROKU_API_URL}/{app_name_or_id}", headers=self.headers, json=payload
            )
            handle_error(response)
            return response.json()
        else:
            raise HerokuException("Update operation cancelled as no data supplied.")

    def build_from_source(
        self, app_name_or_id, source_url, version=None, delay=1.5, sha256=None
    ):
        """
        Creates a new build of an existing app.

        app_name_or_id: the application's name or id on Heroku.
        source_url: URL where gzipped tar archive of source code for build was downloaded.
        version: A piece of metadata that you use to track what version of your
                    source code originated this build.
        delay: How long it takes in seconds to get the build status change from
                "pending" to "succeeded" or "failed".
        sha256: an optional SHA256 checksum of the gzipped tarball for verifying its integrity.
        """

        payload = {"source_blob": {"url": source_url}}
        if version is not None:
            payload["source_blob"]["version"] = version
        if sha256 is not None:
            payload["source_blob"]["checksum"] = "SHA256:" + sha256

        response = requests.post(
            f"{HEROKU_API_URL}/{app_name_or_id}/builds",
            headers=self.headers,
            json=payload,
        )
        handle_error(response)
        build_details = response.json()
        # Poll the API until app status changes from pending to either "succeeded" or "failed"
        status = build_details["status"]
        app_id = build_details["app"]["id"]
        build_id = build_details["id"]

        while status == "pending":
            time.sleep(delay)
            response = requests.get(
                f"{HEROKU_API_URL}/{app_id}/builds/{build_id}", headers=self.headers
            )
            handle_error(response)
            build_details = response.json()
            status = build_details["status"]

        return build_details

    def build_from_git(
        self, app_name_or_id, git_url, branch="main", version=None, delay=1.5
    ):
        """
        app_name_or_id: the application's name or id on Heroku.
        git_url: github repository url of the source code.
        branch: the git branch to get the source code from. Defaults to `main`.
        version: A piece of metadata that you use to track what version of your
                    source code originated this build. If version is not specified,
                    will use the commit hash from the git_url as the version.
        delay: How long it takes in seconds to get the build status change from
                "pending" to "succeeded" or "failed".
        """

        tarball_url = f"{git_url}/tarball/{branch}"

        if version is None:
            version = get_commit_sha(git_url, branch)

        return self.build_from_source(
            app_name_or_id, tarball_url, version=version, delay=delay
        )

    def get_app_config(self, app_name_or_id):
        """Get config-vars for the app"""
        response = requests.get(
            f"{HEROKU_API_URL}/{app_name_or_id}/config-vars", headers=self.headers
        )
        handle_error(response)
        return response.json()

    def _create_or_update(self, app_name_or_id, **config_vars):
        """Base helper to create or update application config vars.
        config_vars: keyword arguments of config variables to be created or updated
        """
        if config_vars.keys():
            response = requests.patch(
                f"{HEROKU_API_URL}/{app_name_or_id}/config-vars",
                headers=self.headers,
                json=config_vars,
            )
            handle_error(response)
            return response.json()
        else:
            raise HerokuException("No config vars passed in")

    def update_config(self, app_name_or_id, **config_vars):
        """Update an existing config variable."""
        return self._create_or_update(app_name_or_id, **config_vars)

    def delete_config(self, app_name_or_id, *config_vars):
        """Delete a config variable.
        config_vars: names of config vars to be deleted"""
        if config_vars:
            payload = {c: None for c in config_vars}
            response = requests.patch(
                f"{HEROKU_API_URL}/{app_name_or_id}/config-vars",
                headers=self.headers,
                json=payload,
            )
            handle_error(response)
            return response.json()
        else:
            raise HerokuException("No config vars passed in.")

    def create_config(self, app_name_or_id, **config_vars):
        """Create a config variable for the application."""
        return self._create_or_update(app_name_or_id, **config_vars)
