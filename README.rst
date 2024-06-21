Yet another Podcast/RSS/Atom catcher
====================================

.. _FeedDl: https://github.com/drehtuer/feeddl
.. _greg: https://github.com/manolomartinez/greg
.. _stagger: https://github.com/staggerpkg/stagger

A small application that pulls podcasts from the world wide web.
It aims to be very flexible in the way the retrieved files are named, since this is a feature I'm missing in other pod catchers.

All configuration is done via a configuration file, no user interface is needed.
It's not intended to be a service, but could easily be called from a cron job or a simple systemd script to perform cyclic checks/downloads.
I mainly use it from WSL, so I only start it by hand manually.

The code is an iteration of `FeedDl`_, which was heavily inspired by `greg`_.
Greg lacked flexible naming options and FeedDl had problems downloading feeds with invalid certificates and used `stagger`_ (like greg), which doesn't work with Python > 3.10 anymore.


License
=======

The repo is published under the `MIT license <https://github.com/drehtuer/podcast_catcher/blob/main/LICENSE>`_


Installation
############

.. _DevContainer: https://containers.dev

The repo provides a `DevContainer`_ configuration that sets up the necessary environment for development, but also works for running the application.

If you don't want to use the docker container, you may install the required packages locally.
Either via pip (with version pinning):

.. code-block:: bash
   
   pip install -r requirements.txt

or via the host's package manager (Ubuntu 24.04):

.. code-block:: bash

   sudo apt install \
     --no-install-recommends \
     python3-invoke \
     python3-feedparser \
     python3-requests \
     python3-eyed3


Configuration
=============

TODO


Usage
=====

TODO
