import pytest
from django.conf import settings

# # Set the Django settings module for the tests
# pytest_configure = pytest.config.getoption("--ds")

# if pytest_configure:
#     settings_module = pytest_configure
# else:
#     settings_module = "selecto.settings"
settings_module = "selecto.settings"

settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.admin",
        "products.apps.ProductsConfig",
        "homepage.apps.HomepageConfig",
    ],
    ROOT_URLCONF="selecto.urls",
)

# Load any fixtures you need for all your tests
pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
