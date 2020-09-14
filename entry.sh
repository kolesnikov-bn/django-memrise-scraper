#!/bin/sh

if [[ -f /app_from_host/entry.sh ]]; then
    echo "Running code from local mount"
    cd /app_from_host
else
    echo "Running code from image"
    cd /app
fi

env >> /etc/environment
python manage.py migrate \
&& python manage.py collectstatic --noinput \
&& exec gunicorn -c=config/gunicorn_config.py django_memrise_scraper.wsgi:application

