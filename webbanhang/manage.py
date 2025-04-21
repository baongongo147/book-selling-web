#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Được sử dụng để thực thi các câu lệnh quản lý dự án.
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webbanhang.settings')      # Xác định và thiết lập biến môi trường DJANGO_SETTINGS_MODULE
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)                                         # Được gọi để thực thi các lệnh từ dòng lệnh được truyền vào khi chạy file manage.py


if __name__ == '__main__':
    main()
