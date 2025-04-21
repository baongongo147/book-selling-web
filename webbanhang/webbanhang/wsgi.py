"""
WSGI config for webbanhang project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
# file dùng deploy project lên server
# WSGI (Web Server Gateway Interface) là một giao diện tiêu chuẩn giữa ứng dụng web và máy chủ web trong Python
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webbanhang.settings')      # Xác định và thiết lập biến môi trường DJANGO_SETTINGS_MODULE trong hệ thống

application = get_wsgi_application()                                        # Tạo ra một ứng dụng WSGI
