# https://docs.docker.com/reference/dockerfile/
FROM ubuntu:24.04

LABEL name="Dev environment" \
  description="DevContainer for podcast_catcher" \
  version="1.4"

ARG ARG_USER
ARG ARG_USER_SHELL=/usr/bin/bash

# Suppress interactive prompts
# in apt
ARG DEBIAN_FRONTEND=noninteractive

ENV LANG=en_US.utf8

RUN \
  # apt cache folder in tmpfs, discarded after build.
  # Avoids deleting it manually at the end.
  --mount=type=tmpfs,target=/var/lib/apt/lists \
  --mount=type=tmpfs,target=/var/cache/apt \
  apt-get update \
  && apt-get upgrade \
  --yes \
  -qq \
  && apt-get install \
  --no-install-recommends \
  --yes \
  -qq \
  # Let's make sure these
  # exists, even if they
  # should be part of the
  # ubuntu base image.
  bash \
  # SCM + ssh support
  git \
  openssh-client \
  # For setting locale.
  # No locale may sometimes
  # cause strange problems.
  locales \
  # Python
  python3.12 \
  python-is-python3 \
  # Python packages,
  # no need for a virtual
  # environment
  python3-invoke \
  python3-feedparser \
  python3-requests \
  python3-eyed3 \
  # Set locale to us UTF-8
  && localedef \
  --inputfile=en_US \
  --force \
  --charmap=UTF-8 \
  --alias-file=/usr/share/locale/locale.alias \
  en_US.UTF-8 \
  # Create local non-root user.
  # vscode will map the UIDs
  # when accessing the container.
  && useradd \
  --shell ${ARG_USER_SHELL} \
  # home dir is needed by vscode
  # when updating UIDs.
  --create-home \
  ${ARG_USER}

USER ${ARG_USER}

# Keep container running, vscode needs to
# attach to it.
CMD [ "sleep", "infinity" ]
