#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "*/5 * * * * source $DIR/venv/bin/activate && python $DIR/crawler.sh >> /tmp/crawler.log" | env EDITOR=vim crontab
