FROM ghcr.io/sdr-enthusiasts/docker-baseimage:python

RUN set -x && \
# define packages needed for installation and general management of the container:
    TEMP_PACKAGES=() && \
    KEPT_PACKAGES=() && \
    KEPT_PIP3_PACKAGES=() && \
    KEPT_RUBY_PACKAGES=() && \
#
    TEMP_PACKAGES+=(pkg-config) && \
    TEMP_PACKAGES+=(git) && \
    TEMP_PACKAGES+=(gcc) && \
    TEMP_PACKAGES+=(python3-dev) && \
    TEMP_PACKAGES+=(pkg-config) && \
#
# Install all the apt, pip3, and gem (ruby) packages:
    apt-get update -q && \
    apt-get install -q -o APT::Autoremove::RecommendsImportant=0 -o APT::Autoremove::SuggestsImportant=0 -o Dpkg::Options::="--force-confold" -y --no-install-recommends  --no-install-suggests ${TEMP_PACKAGES[@]} ${KEPT_PACKAGES[@]} && \

    echo Uninstalling $TEMP_PACKAGES && \
    apt-get remove -y -q ${TEMP_PACKAGES[@]} && \
    apt-get autoremove -q -o APT::Autoremove::RecommendsImportant=0 -o APT::Autoremove::SuggestsImportant=0 -y && \
    apt-get clean -y -q && \
    rm -rf \
      /src/* \
      /tmp/* \
      /var/lib/apt/lists/* \
      /.dockerenv \
      /git
#
COPY rootfs/ /
#
#
RUN set -x && \
    pip3 install -r /usr/share/planelog/requirements.txt && \
    mkdir /opt/planelog


