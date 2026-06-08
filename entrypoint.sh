#!/bin/sh
set -e

echo "→ Esperando PostgreSQL..."
until python manage.py migrate --noinput 2>/dev/null; do
    echo "   Base de datos no disponible, reintentando en 2s..."
    sleep 2
done

echo "→ Cargando datos iniciales..."
python manage.py seed_data

echo "→ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput -v0

echo "→ Iniciando Gunicorn..."
exec gunicorn moyaops_web.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
