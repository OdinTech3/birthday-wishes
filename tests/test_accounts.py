import pytest
from django.urls import reverse
from core.models import Celebrant

@pytest.fixture
def celebrant(db):
    celebrant: Celebrant = Celebrant.objects.create(
        email="john@domain.com", first_name="Natalie", birthday="1991-01-28"
    )

    celebrant.set_password("password")
    celebrant.save()
    return celebrant


@pytest.mark.django_db
def test_sample(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200


def test_create_user(db):
    Celebrant.objects.create(email="jimmyneutron@cartoonet.com", birthday="1989-10-10")
    assert Celebrant.objects.count() == 1


@pytest.mark.django_db
def test_login_failed(client, celebrant: Celebrant):
    is_loggedin = client.login(username=celebrant.username, password="passwordistoocommon")
    assert not is_loggedin


@pytest.mark.django_db
def test_login(client, celebrant: Celebrant):
    is_loggedin = client.login(username=celebrant.username, password="password")
    assert is_loggedin


@pytest.mark.django_db
def test_signup(client):
    signup_url = reverse("account_signup")
    response = client.post(signup_url, {
        "email": "johnnybravo@cartoonet.com",
        "birthday": "1990-11-02",
        "first_name": "Johnny",
        "last_name": "Bravo",
        'password1': "#DoTheMonkeyStyle",
        'password2': "#DoTheMonkeyStyle"
    })

    assert Celebrant.objects.filter(email="johnnybravo@cartoonet.com").exists()
