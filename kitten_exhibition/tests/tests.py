import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from kitten_exhibition.kitten_app import serializers
from kitten_exhibition.kitten_app.models import Kitten


@pytest.mark.django_db
def test_create_kitten(client, test_user):
    create_kitten_url = reverse('kitten-create')

    client.login(username=test_user.username, password='testpassword123')
    data = {'color': 'red', 'description': ' New Test description', 'age': '30', 'owner': 1}
    response = client.post(create_kitten_url, data)
    print(response)

    assert response.status_code == 201
    assert Kitten.objects.get(color='red')


@pytest.mark.django_db
def test_update_kitten(client, test_user, kitten):
    update_kitten_url = reverse('kitten-update', kwargs={'pk': kitten.pk})
    data = {'color': 'blue'}
    token = str(RefreshToken.for_user(test_user).access_token)
    response = client.patch(update_kitten_url, headers={'Authorization': 'Bearer ' + token}, format='json', data=data, partial=True)
    kitten.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert kitten.color == 'blue'


@pytest.mark.django_db
def test_delete_kitten(client, test_user, kitten):
    delete_kitten_url = '/api/kittens/1/delete/'
    token = str(RefreshToken.for_user(test_user).access_token)
    response = client.delete(delete_kitten_url, headers={'Authorization': 'Bearer ' + token})

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Kitten.objects.filter(id=kitten.pk).exists()


@pytest.mark.django_db
def test_kitten_list(client):
    url = reverse('kittens-list')
    response = client.get(url)
    kittens = Kitten.objects.all()
    serializer = serializers.KittenSerializer(kittens, many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
