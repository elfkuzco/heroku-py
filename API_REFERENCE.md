# heroku\-py Reference

_class_ _heroku_py_\.**HerokuClient**(_api_key_=_None_)

Create an instance of a heroku client for making API requests.

If _api_key_ is `None`, will try to load API key from _\.netrc_ file in
current user's home directory or load from environment variable `$HEROKU_API_KEY`.

All methods in the client return a JSON response from the server serialized into Python types.

Methods in the client include:

    create_app(app_name):
        Creates an app on Heroku.
        app_name should conform to the pattern ^[a-z][a-z0-9-]{1,28}[a-z0-9]$.


    get_app_info(app_name_or_id):
        Gets the details about an app given its app_name_or_id.


    delete_app(app_name_or_id):
        Deletes an app given its app_name_or_id


    list_apps():
        List existing apps owned by user


    update_app(app_name_or_id, *, new_name=None, maintenance=None):
        Update an existing app.
          new_name: The new name for the app.
          maintenance: A boolean indicating whether to put the app in maintenance mode.

        new_name and maintenance are passed in as keyword arguments.


    build_from_source(app_name_or_id, source_url, version=None, delay=1.5, sha256=None):

        Creates a new build of an existing app.
          app_name_or_id: the application's name or id on Heroku.
          source_url: URL where gzipped tar archive of source code for build was downloaded.
          version: A piece of metadata that you use to track what version of your
                      source code originated this build.
          delay: How long it takes in seconds to get the build status change from
                  "pending" to "succeeded" or "failed".
          sha256: an optional SHA256 checksum of the gzipped tarball for verifying its integrity.


    build_from_git(app_name_or_id, git_url, branch="main", version=None, delay=1.5):

        Generate build from source code repository on GitHub

        git_url: github repository url of the source code.
        branch: the git branch to get the source code from. Defaults to `main`.

    get_app_config(app_name_or_id):
        Get the applications config-vars

    create_config(app_name_or_id, **config_vars):
        Create new config vars for the app. Will update existing config vars if an
        existing key is found in config_vars.
        config_vars should be passed in as keyword arguments

    update_config(app_name_or_id, **config_vars):
        Update an application's existing config-vars.

    delete_config(app_name_or_id, *config_vars):
        Delete application's config vars.
        config_vars: string names of the application's existing variables
