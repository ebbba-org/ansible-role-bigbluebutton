#!/bin/bash
FULL="/usr/share/meteor/bundle/programs/web.browser/app/resources/images/virtual-backgrounds"
THUMB="${FULL}/thumbnails"

cd "$FULL"
for pic in *.jpg; do
    convert "$pic" -resize 50x50^ -gravity Center -extent 50x50 "${THUMB}/${pic}"
done