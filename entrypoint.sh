#!/usr/bin/env bash
set -e

+ echo "🔨 Building CSS..."
+ npm run build:css            # <- compile main.scss → main.css (once)
+
echo "🚀 OPEN PREVIEW AT: http://localhost:8000/"

npm run watch:css &          # still watch for edits
python manage.py runserver 0.0.0.0:8000