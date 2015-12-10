import sys

import django
import os
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'application.settings'
test_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(test_dir, 'test_project'))


def runtests():
    django.setup()
    test_runner = get_runner(settings)(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['protector', 'test_app'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
