#!/bin/bash

# Esperar a que arranque el escritorio
sleep 8

# Esperar a que Flask esté disponible
until curl -s http://localhost:5000 >/dev/null
do
    sleep 2
done

/usr/bin/chromium \
    --noerrdialogs \
    --disable-infobars \
    --disable-session-crashed-bubble \
    --check-for-update-interval=31536000 \
    --kiosk \
    http://localhost:5000
