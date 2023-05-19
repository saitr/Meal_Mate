import pytest
from rest_framework.test import APIClient
from apps.models import *
# from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from apps.serializers.orderserializers import *
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs,email='test@example.com')
    return make_user

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs, email='test@example.com')
    return make_user


@pytest.mark.django_db
def test_order_add(api_client, create_user):
    user = create_user(username='testuser3', password='testpassword3')
    category = Categories.objects.create(category_name='Default Category')
    item = Items.objects.create(category=category, item_name='Item 1', item_price=10.0, is_available=True)
    cart_item = Cart.objects.create(user=user, item=item, quantity=1)

    data = {
        'user':user.id,
        'first_name': 'John',
        'last_name': 'Doe',
        'address': '123 Main St',
        'zip_code': 12345,
        'place': 'City',
        'payment_method': 'Cash On Delivery'
    }

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    response = api_client.post('/rest_order/', data=data)

    order = response.data['order']
    assert 'user' in order
    assert order['user'] == user.id
    assert 'first_name' in order
    assert order['first_name'] == 'John'
    assert 'last_name' in order
    assert order['last_name'] == 'Doe'
    assert 'address' in order
    assert order['address'] == '123 Main St'
    assert 'zip_code' in order
    assert order['zip_code'] == 12345
    assert 'place' in order
    assert order['place'] == 'City'
    assert 'payment_method' in order
    assert order['payment_method'] == 'Cash On Delivery'
    
