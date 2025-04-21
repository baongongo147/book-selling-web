"""
ASGI config for webbanhang project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
# file được tạo ra để định nghĩa và cấu hình một ASGI (Asynchronous Server Gateway Interface) application. 
# ASGI là một giao diện được sử dụng để xử lý các yêu cầu HTTP và WebSockets một cách không đồng bộ, phù hợp với các ứng dụng web yêu cầu hiệu suất cao và khả năng mở rộng.
# ASGI là một giao diện tiêu chuẩn cho các máy chủ web Python để tương tác với các ứng dụng web bất đồng bộ.
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webbanhang.settings')      #  Xác định và thiết lập biến môi trường DJANGO_SETTINGS_MODULE trong hệ thống, cho Django biết module cài đặt cấu hình settings của dự án là webbanhang.settings

application = get_asgi_application()                                        # Tạo một ứng dụng ASGI
