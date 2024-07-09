Podcast_Catcher: Yet another Podcast/RSS/Atom catcher
=====================================================

.. _FeedDl: https://github.com/drehtuer/feeddl
.. _greg: https://github.com/manolomartinez/greg
.. _stagger: https://github.com/staggerpkg/stagger

A small application that pulls podcasts from the world wide web.
It aims to be very flexible in the way the retrieved files are named, since this is a feature I'm missing in other pod catchers.

All configuration is done via a configuration file, no user interface is needed.
It's not intended to be a service, but could easily be called from a cron job or a simple systemd script to perform cyclic checks/downloads.
I mainly use it from WSL, so I only start it by hand manually.

The code is an iteration of `FeedDl`_, which was heavily inspired by `greg`_.
Greg lacked flexible naming options and FeedDl had problems downloading feeds with invalid certificates and used `stagger`_ (like greg), which doesn't work with Python >3.9 anymore.
`FeedDl`_ was written in a rush to keep the podcasts flowing, this repo is a proper rewrite from ground up.

License
=======

This repo is published under the `GPLv2 license <https://github.com/drehtuer/podcast_catcher/blob/main/LICENSE>`_


Dependencies
############

.. _python_build: GitHub<https://github.com/pypa/build/>
.. _python_build_license: https://github.com/pypa/build/blob/main/LICENSE
.. _python_docutils: https://sourceforge.net/projects/docutils/
.. _python_docutils_license: https://sourceforge.net/p/docutils/code/HEAD/tree/trunk/docutils/COPYING.txt
.. _python_invoke: https://github.com/pyinvoke/invoke
.. _python_invoke_license: https://github.com/pyinvoke/invoke/blob/main/LICENSE
.. _python_feedparser: https://github.com/kurtmckee/feedparser
.. _python_feedparser_license: https://github.com/kurtmckee/feedparser/blob/develop/LICENSE
.. _python_jsonschema: https://github.com/python-jsonschema/jsonschema
.. _python_jsonschema_license: https://github.com/python-jsonschema/jsonschema/blob/main/COPYING
.. _python_mutagen: https://github.com/quodlibet/mutagen
.. _python_mutagen_license: https://github.com/quodlibet/mutagen/blob/main/COPYING
.. _python_pygments: https://github.com/pygments/pygments
.. _python_pygments_license: https://github.com/pygments/pygments/blob/master/LICENSE
.. _python_requests: https://github.com/psf/requests
.. _python_requests_license: https://github.com/psf/requests/blob/main/LICENSE
.. _python_setuptools: https://github.com/pypa/setuptools
.. _python_setuptools_license: https://github.com/pypa/setuptools/blob/main/LICENSE

================================= ======= ==================================================
Dependency                        Version License
================================= ======= ==================================================
`build <python_build>`_           1.0.3   `MIT <python_build_license_>`_
`docutils <python_docutils>`_     0.20.1  `Multiple licenses <python_docutils_license_>`_
`feedparser <python_feedparser>`_ 6.0.10  `feedparser license <python_feedparser_license_>`_
`invoke <python_invoke>`_         2.0.0   `BSD2 <python_invoke_license_>`_
`jsonschema <python_jsonschema>`_ 4.10.3  `MIT <python_jsonschema_license_>`_
`mutagen <python_mutagen>`_       1.46.0  `GPL2 <python_mutagen_license_>`_
`pygments <python_pygments>`_     2.17.2  `BSD2 <python_pygments_license_>`_
`requests <python_requets>`_      2.31.0  `Apache 2.0 <python_requests_license_>`_
`setuptools <python_setuptools>`_ 68.1.2  `MIT <python_setuptools_license_>`_
================================= ======= ==================================================

Installation
############

For Development
===============
.. _DevContainer: https://containers.dev

The repo provides a `DevContainer`_ configuration that sets up the necessary environment for development, but also works for running the application.

If you don't want to use the docker container, you may install the required packages locally in a virtual environment (e.g. venv).
Either via pip (with version pinning):

.. code-block:: bash
   
   pip install -r requirements.txt

or via the host's package manager (Ubuntu 24.04):

.. code-block:: bash

   sudo apt install \
     --no-install-recommends \
     python3-build \
     python3-docutils \
     python3-feedparser \
     python3-invoke \
     python3-jsonschema \
     python3-mutagen \
     python3-pygments \
     python3-requests \
     python3-setuptools \
     python3-venv

Configuration
=============

.. _config_schema: https://github.com/drehtuer/podcast_catcher/blob/main/podcast_catcher/config.schema.json
.. _config_json: https://github.com/drehtuer/podcast_catcher/blob/main/config/config.json
.. _mutagen_keys: https://github.com/quodlibet/mutagen/blob/release-1.46.0/mutagen/easyid3.py#L470

Global and per-feed configuration is stored in a JSON config file.
By default, the file is located at ``~/.config/podcast_catcher/config.json``, but other location can be set using the ``--config`` argument.

Configuration is split between ``settings`` and ``feeds``.

Settings covers global options, e.g. the base ``download_dir`` and ``data_dir``, but also settings wich may be overriden per feed.
These options may contain placeholders, which will expand per feed.

Entries in the ``tags`` array map ID3 tags and must follow the keys available in `mutagen <mutagen_keys_>`_.

Available placeholders:

* ``%feed_title%``
* ``%feed_subtitle%``
* ``%feed_description%``
* ``%feed_link%``
* ``%feed_date%``
* ``%feed_datetime%``
* ``%episode_date%``
* ``%episode_datetime%``
* ``%episode_url_basename%``
* ``%episode_url_extension%``
* ``%episode_title%``
* ``%episode_author%``
* ``%episode_summary%``
* ``%episode_link%``

Keep in mind that not all feeds provide the necessary data for each placeholder.
The ``raw_feed`` subcommand is useful to check what is available for each feed.

For details, check the `example config.json <config_json_>`_ and `JSON schema description <config_schema_>`_.


Usage
=====

podcast_catcher shows a help message if invoked with ``-h`` or ``--help``.

Global flags:

* ``--config``: Provide a non-standard location of the configuration file.
  Default location is ``~/.config/podcast_catcher/config.json``.

Subcommands:

* ``download``: Check for new episodes and download them.
* ``list_feeds``: Shows a list of all feeds defined in the configuration.
  Shows the last successful download for each entry.
* ``list_episodes``: This subcommand requires the name of the feed as an additional positional parameter.
  It checks online for new episodes and prints them.
  The name is case-sensitive, if in doubt, check first with ``list_feeds``.
* ``raw_feed``: This is more a debugging command and requires the name of the feed as additional parameter.
  It shows the unparsed RSS/ATOM text as downloaded from the feed.
  The name is case-sensitive, if in doubt, check first with ``list_feeds``.
* ``version``: Shows the version of podcast_catcher.
