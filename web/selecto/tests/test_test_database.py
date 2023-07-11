from django.conf import settings
import sys

def test_database_settings():
    print(settings.DATABASES)
    print(sys.argv)
    assert False