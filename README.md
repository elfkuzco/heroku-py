# heroku-py

A Python3 wrapper around the [v3 Heroku API](https://devcenter.heroku.com/categories/platform-api).

- [Description](#description)
- [Installation](#installation)
- [Example Usage](#example-usage)
- [Acknowledgements](#acknowledgements)
- [Reference](API_REFERENCE.md)

# Description

heroku-py is a Python3 wrapper around some of the [v3 Heroku API](https://devcenter.heroku.com/categories/platform-api) endpoints.

heroku-py currently only exposes most of the common endpoints that you probably use
everyday during development such as performing CRUD operations on an app and deploying
builds of versions of your source code.

# Installation

```
$ pip3 install heroku-py
```

# Example Usage

After [installation](#installation),

```
>>> from heroku_py import HerokuClient

# loads API key from .netrc file in home directory or $HEROKU_API_KEY environment variable
# if no api_key is passed in during initialization.

>>> hk = HerokuClient()
>>> hk.create_app("wonder-beetle")

    {'acm': False,
    'archived_at': None,
    'build_stack': {'id': '2be35cd6-418a-417e-9531-42c5de1dfb96',
                 'name': 'heroku-20'},
    'buildpack_provided_description': None,
    'created_at': '2021-05-29T23:07:51Z',
    'git_url': 'https://git.heroku.com/wonder-beetle-1998.git',
    'id': 'd178bf7c-189d-4f1d-bc7b-b6e9fc012c5c',
    'internal_routing': None,
    'maintenance': False,
    'name': 'wonder-beetle-1998',
    'organization': None,
    'owner': {'email': 'orjiuchechukwu52@yahoo.com',
           'id': 'f7088035-f7f4-4359-8fab-e9d4431ceac3'},
    'region': {'id': '59accabd-516d-4f0e-83e6-6e3757701145', 'name': 'us'},
    'released_at': '2021-05-29T23:07:52Z',
    'repo_size': None,
    'slug_size': None,
    'space': None,
    'stack': {'id': '2be35cd6-418a-417e-9531-42c5de1dfb96', 'name': 'heroku-20'},
    'team': None,
    'updated_at': '2021-05-29T23:07:55Z',
    'web_url': 'https://wonder-beetle-1998.herokuapp.com/'}
```

To deploy a build to your app with your code's repository on GitHub,

```
>>> hk.build_from_git("wonder-beetle-1998", "https://github.com/elfkuzco/heroku-py-testing-repo",
                      branch="main", delay=1.2)

  {'app': {'id': 'd178bf7c-189d-4f1d-bc7b-b6e9fc012c5c'},
   'buildpacks': [{'url': 'https://buildpack-registry.s3.amazonaws.com/buildpacks/heroku/nodejs.tgz'}],
   'created_at': '2021-05-29T23:13:52Z',
   'id': 'a7c79e7f-e615-49fa-9fba-f4bfd93fcb33',
   'output_stream_url': 'https://build-output.heroku.com/streams/...',
   'release': {'id': 'f7dc20e3-c179-434b-9b22-9f2202aa808a'},
   'slug': {'id': '357d2fd4-dd5d-4235-95eb-0726bcb48643'},
   'source_blob': {'checksum': None,
                   'url': 'https://github.com/elfkuzco/heroku-py-testing-repo/tarball/main',
                   'version': '8bcc6b743f8956529df467dc86a4130754f0eddb',
                   'version_description': None},
   'stack': 'heroku-20',
   'status': 'succeeded',
   'updated_at': '2021-05-29T23:14:07Z',
   'user': {'email': 'orjiuchechukwu52@yahoo.com',
            'id': 'f7088035-f7f4-4359-8fab-e9d4431ceac3'}}

```

To build from a gzipped tarball of your source code hosted somewhere,

```
>>> hk.build_from_source("wonder-beetle-1998",
                        "https://github.com/elfkuzco/heroku-py-testing-repo/raw/beta/heroku_demo.tar.gz",
                        version="1.2.5")
```

To update an app's details,

```
>>> hk.udpate_app("wonder-beetle-1998", new_name="ravenous-eagle-2021", maintenance=True)

  {'acm': False,
   'archived_at': None,
   'build_stack': {'id': '2be35cd6-418a-417e-9531-42c5de1dfb96',
                   'name': 'heroku-20'},
   'buildpack_provided_description': 'Node.js',
   'created_at': '2021-05-29T23:07:51Z',
   'git_url': 'https://git.heroku.com/ravenous-eagle-2021.git',
   'id': 'd178bf7c-189d-4f1d-bc7b-b6e9fc012c5c',
   'internal_routing': None,
   'maintenance': True,
   'name': 'ravenous-eagle-2021',
   'organization': None,
   'owner': {'email': 'orjiuchechukwu52@yahoo.com',
             'id': 'f7088035-f7f4-4359-8fab-e9d4431ceac3'},
   'region': {'id': '59accabd-516d-4f0e-83e6-6e3757701145', 'name': 'us'},
   'released_at': '2021-05-29T23:23:20Z',
   'repo_size': None,
   'slug_size': 34060308,
   'space': None,
   'stack': {'id': '2be35cd6-418a-417e-9531-42c5de1dfb96', 'name': 'heroku-20'},
   'team': None,
   'updated_at': '2021-05-29T23:28:11Z',
   'web_url': 'https://ravenous-eagle-2021.herokuapp.com/'}

```

To delete an app,

```
>>> hk.delete_app("ravenous-eagle-2021")
```

Check out [API Reference](API_REFERENCE.md).

# Acknowledgements

- [Richard Okonicha](https://github.com/konichar) whose initiative I developed upon
  to build this package.
