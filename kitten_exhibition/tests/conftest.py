import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from kitten_exhibition.kitten_app.models import Breed, Kitten


@pytest.fixture
def test_user(db):
    return User.objects.create_user(id=1, username='testuser1', password='testpassword123')


@pytest.fixture
def breed(db):
    return Breed.objects.create(name='Test breed')


@pytest.fixture
def kitten(db, test_user):
    return Kitten.objects.create(id=1, color='Test color', description='Test description', age=12, owner=test_user)


@pytest.fixture
def client():
    return APIClient()