#!/usr/bin/env bash
set -e

# 1) Custom banner
echo "🚀 OPEN PREVIEW AT: http://localhost:8000/"

# 2) Start your Sass watcher
npm run watch:css &

# 3) Run Django on 0.0.0.0 so it’s reachable from the host
python manage.py runserver 0.0.0.0:8000
