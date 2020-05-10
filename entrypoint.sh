#!/bin/sh -e

case "$1" in
  run)
    flask run --host=0.0.0.0
    ;;
  *)
    exec "$@"
esac
