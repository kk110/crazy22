import os
import sys


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crazyEye.settings')
    import django
    django.setup()
    from backend.main import ManagementUtility
    ManagementUtility(sys.argv)