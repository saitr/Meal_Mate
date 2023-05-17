import pytest
from rest_framework.test import APIClient
from apps.models import *
# from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_item_list_success(api_client):
    # Create test items
    category = Categories.objects.create(category_name='Default Category')
    item1 = Items.objects.create(category=category,item_name='Item 1', item_price=10.0, is_available=True)
    item2 = Items.objects.create(category=category,item_name='Item 2', item_price=20.0, is_available=True)
    item3 = Items.objects.create(category=category,item_name='Item 3', item_price=30.0, is_available=True)

    url = '/item_list/'
    response = api_client.get(url, format='json')

    assert response.status_code == 200

    # Check the response data format
    assert isinstance(response.data, list)

    # Check the number of items in the response
    assert len(response.data) == 3

    # Check the item details
    item1_data = response.data[0]
    # assert item1_data['id'] == 1
    assert item1_data['item_name'] == item1.item_name
    assert item1_data['item_price'] == item1.item_price
    assert item1_data['is_available'] == item1.is_available

    item2_data = response.data[1]
    # assert item2_data['id'] == 2
    assert item2_data['item_name'] == item2.item_name
    assert item2_data['item_price'] == item2.item_price
    assert item2_data['is_available'] == item2.is_available

    item3_data = response.data[2]
    # assert item3_data['id'] == 3
    assert item3_data['item_name'] == item3.item_name
    assert item3_data['item_price'] == item3.item_price
    assert item3_data['is_available'] == item3.is_available

