"""
WSGI config for expdeploy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import traceback
import signal
import time

from django.core.wsgi import get_wsgi_application


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)) #added 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expdeploy.settings")

try:
	application = get_wsgi_application()
	print 'WSGI without exception'
except Exception:
	print 'handling WSI exception'
	traceback.print_exc()
	if 'mod_wsgi' in sys.modules:
		os.kill(os.getpid(), signal.SIGINT)
		time.sleep(2.5)
