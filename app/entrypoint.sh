#!/bin/sh

while ! nc -z chromedriver 4444; do
  sleep 0.1
done

exec "$@"