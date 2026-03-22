#!/usr/bin/with-contenv bashio
# shellcheck shell=bash

bashio::log.info "Starting PaddiSense Installer..."

cd /app
exec python3 -m installer
