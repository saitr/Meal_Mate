import pytest
from rest_framework.test import APIClient
from apps.models import *
# from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    return APIClient()


######################### Category test case ################################

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs,email='test@example.com')
    return make_user

@pytest.mark.django_db 
def test_category_list_success(api_client,create_user):

    user = create_user(username='testuser', password='testpassword')

    # Generate access token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Set the access token in the Authorization header
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    #Creating the category list.

    category1 = Categories.objects.create(category_name='veg')
    category2 = Categories.objects.create(category_name='Non-Veg')
    category3 = Categories.objects.create(category_name='Juice')

    url = '/rest_category/'

    response = api_client.get(url,format='json')

    assert response.status_code == 200