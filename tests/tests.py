import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_create():
    """This is Django-native functionality, so technically this doesn't need to be tested,
    but here's how you would!"""
    User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
    assert User.objects.count() == 1
