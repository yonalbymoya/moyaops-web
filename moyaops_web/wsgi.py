import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moyaops_web.settings")

_django_app = get_wsgi_application()


def application(environ, start_response):
    host = environ.get("HTTP_HOST", "")
    if "_" in host:
        environ["HTTP_HOST"] = host.replace("_", "-")
    return _django_app(environ, start_response)
