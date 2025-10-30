import sys, os
import site
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, "/var/www/html/myapp")
os.chdir("/var/www/html/myapp")
site.addsitedir('/var/www/html/venv/lib/python3.12/site-packages')


from app import create_app
application = create_app()