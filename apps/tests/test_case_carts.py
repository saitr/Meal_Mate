import pytest
from rest_framework.test import APIClient
from apps.models import *
# from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

@pytest.fixture
def api_client():
    return APIClient()


######################### Category test case ################################

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs,email='test@example.com')
    return make_user


########################### Cart List Test Case ################################


@pytest.mark.django_db
def test_cart_list_success(api_client, create_user):
    # Create a user
    user = create_user(username='testuser', password='testpassword')

    # Create test items
    category = Categories.objects.create(category_name='Default Category')

    item1 = Items.objects.create(category=category,item_name='Item 1', item_price=10.0, is_available=True)
    item2 = Items.objects.create(category=category,item_name='Item 2', item_price=20.0, is_available=True)
    item3 = Items.objects.create(category=category,item_name='Item 3', item_price=30.0, is_available=True)

    # Create test carts
    cart1 = Cart.objects.create(user=user, item=item1, quantity=2)
    cart2 = Cart.objects.create(user=user, item=item2, quantity=1)
    cart3 = Cart.objects.create(user=user, item=item3, quantity=3)

    # Generate access token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Set the access token in the Authorization header
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Make a GET request to the cart list endpoint
    url = f'/rest_cart/{user.id}/'
    response = api_client.get(url, format='json')

    # Check the response status code
    assert response.status_code == 200

    # Check the response data format
    assert isinstance(response.data, dict)
    assert 'status' in response.data
    assert 'cart_list' in response.data


    assert response.status_code == status.HTTP_200_OK

    # Check the status code
    assert response.data['status'] == 200

    # Check the cart list
    cart_list = response.data['cart_list']
    assert isinstance(cart_list, list)
    assert len(cart_list) == 3

    # Check the cart details
    cart1_data = cart_list[0]
    assert 'user' in cart1_data
    assert 'item' in cart1_data
    assert 'quantity' in cart1_data
    assert cart1_data['user'] == user.id
    assert cart1_data['item'] == item1.id
    assert cart1_data['quantity'] == cart1.quantity

    cart2_data = cart_list[1]
    assert 'user' in cart2_data
    assert 'item' in cart2_data
    assert 'quantity' in cart2_data
    assert cart2_data['user'] == user.id
    assert cart2_data['item'] == item2.id
    assert cart2_data['quantity'] == cart2.quantity

    cart3_data = cart_list[2]
    assert 'user' in cart3_data
    assert 'item' in cart3_data
    assert 'quantity' in cart3_data
    assert cart3_data['user'] == user.id
    assert cart3_data['item'] == item3.id



##################################### Cart add Test Case ###############################



@pytest.mark.django_db
def test_cart_add_success(api_client, create_user):
    # Create a user
    user = create_user(username='testuser', password='testpassword')

    # Generate access token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Set the access token in the Authorization header
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    category = Categories.objects.create(category_name='Default Category')
    # Create an item
    item = Items.objects.create(category=category, item_name='Item 1', item_price=10.0, is_available=True)

    # Prepare request data
    url = f'/restadd_cart/{user.id}/'
    data = {'item_id': item.id, 'quantity': 2}

    # Make a POST request to add item to cart
    response = api_client.post(url, data, format='json', follow=True)

    # Check the response status code
    # assert response.data == status.HTTP_201_CREATED
    assert response.status_code == 200
    # Check the response data
    assert 'status' in response.data
    assert response.data['status'] == 201
    assert 'cart_item' in response.data

    # Check the cart item details
    cart_item = response.data['cart_item']
    assert 'user' in cart_item
    assert cart_item['user'] == user.id
    assert 'item' in cart_item
    assert cart_item['item'] == item.id
    assert 'quantity' in cart_item
    assert cart_item['quantity'] == 2

    # Check if the cart item is created in the database
    cart = Cart.objects.filter(user=user, item=item).first()
    assert cart is not None
    assert cart.quantity == 2






@pytest.mark.django_db
def test_cart_item_update(api_client, create_user):
    # Create a user
    user = create_user(username='testuser', password='testpassword')

    # Generate access token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Set the access token in the Authorization header
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    category = Categories.objects.create(category_name='Default Category')
    # Create an item
    item = Items.objects.create(category=category, item_name='Item 1', item_price=10.0, is_available=True)

    # Add an item to the cart
    cart_item = Cart.objects.create(user=user, item=item, quantity=2)

    # Prepare request data
    url = f'/restupdate_cart/{cart_item.id}/{user.id}/'
    data = {'action': 'increase'}

    # Make a PUT request to increase the quantity of the cart item
    response = api_client.put(url, data, format='json')

    # Check the response status code
    assert response.status_code == status.HTTP_200_OK

    # Check the response data
    assert 'status' in response.data
    assert response.data['status'] == 200
    assert 'cart_item' in response.data

    # Check the updated cart item details
    updated_cart_item = response.data['cart_item']
    assert 'user' in updated_cart_item
    assert updated_cart_item['user'] == user.id
    assert 'item' in updated_cart_item
    assert updated_cart_item['item'] == item.id
    assert 'quantity' in updated_cart_item
    assert updated_cart_item['quantity'] == 3

    # Check if the cart item is updated in the database
    cart_item.refresh_from_db()
    assert cart_item.quantity == 3

    # Make a PUT request to decrease the quantity of the cart item
    data = {'action': 'decrease'}
    response = api_client.put(url, data, format='json')

    print(response)

    # Check the response status code
    # assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the cart item is deleted from the database
    # assert not Cart.objects.filter(pk=cart_item.id).exists()



@pytest.mark.django_db
def test_cart_item_delete(api_client, create_user):
    # Create a user
    user = create_user(username='testuser', password='testpassword')

    # Generate access token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Set the access token in the Authorization header
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    category = Categories.objects.create(category_name='Default Category')

    # Create a cart item
    item = Items.objects.create(category=category,item_name='Item 1', item_price=10.0, is_available=True)
    cart_item = Cart.objects.create(user=user, item=item, quantity=1)

    # Prepare the request URL
    url = f'/delete_cart/{cart_item.id}/'

    # Make a DELETE request to delete the cart item
    response = api_client.delete(url)

    # Check the response status code
    assert response.status_code == status.HTTP_200_OK

    # Check the response data
    assert 'status' in response.data
    assert response.data['status'] == 'Deleted'

    # Check if the cart item is deleted from the database
    assert not Cart.objects.filter(pk=cart_item.id).exists()
