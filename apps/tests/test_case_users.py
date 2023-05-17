import pytest
from rest_framework.test import APIClient
from apps.models import *
# from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import pytest
from django.core import mail
from django.urls import reverse
from rest_framework import status
######################### Test Case for SignUp ###########################

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_signup_success(api_client):
    url = '/rest_signup/'
    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'phone_number': '34578',
        'email': 'test@gmail.com',
        'address': 'testaddress'
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['username'] == 'testuser'
    # Add more assertions as needed

@pytest.mark.django_db
def test_signup_missing_fields(api_client):
    url = '/rest_signup/'
    data = {'username': 'testuser'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 400
    response_data = response.data

    # Print or log the response data
    print('this is the response data', response_data)

    # Add your assertions based on the response data
    assert 'email' in response_data
    if 'email' in response_data:
        assert response_data['email'][0] == 'This field is required.'
    assert 'password' in response_data
    if 'password' in response_data:
        assert response_data['password'][0] == 'This field is required.'

    # Add more assertions as needed

    # Add more assertions as needed

# Add more test cases as needed


########################## Test Case for the SignIn #############################


@pytest.mark.django_db
def test_sign_in_success(api_client):
    # Create a test user
    username = 'testuser'
    password = 'testpassword'
    email = 'testemail@example.com'  # Provide a dummy email address
    user = User.objects.create_user(username=username, email=email, password=password)

    # Send a POST request to the sign-in endpoint
    url = '/rest_signin/'
    data = {'username': username, 'password': password}
    response = api_client.post(url, data, format='json')

    # Assert the response
    assert response.status_code == 200
    assert response.data['status'] == 200
    assert 'refresh' in response.data
    assert 'access' in response.data


    print('this is the response of the sigin',response)



################################### Verify otp Test Case #######################################


@pytest.fixture
def create_user(db):
    def make_user(email, otp):
        user = User.objects.create(email=email, otp=otp)
        return user
    return make_user

@pytest.mark.django_db
def test_verify_otp_success(api_client, create_user):
    # Create a user
    email = 'test@example.com'
    otp = '123456'
    user = create_user(email=email, otp=otp)

    # Prepare request data
    url = reverse('VerifyRestEmail', args=[email])
    data = {'otp': otp}

    # Make a POST request to verify OTP
    response = api_client.post(url, data, format='json')

    # Check the response status code
    assert response.status_code == status.HTTP_200_OK

    # Check the response data
    assert 'status' in response.data
    assert 'refresh' in response.data
    assert 'access' in response.data
    assert 'verification' in response.data

    # Check user fields after verification
    user.refresh_from_db()
    assert user.is_active
    assert user.is_verified
    assert user.is_logged_in
    assert user.jwt_token is not None

    # Check the email sent
    assert len(mail.outbox) == 1
    email_sent = mail.outbox[0]
    assert email_sent.subject == 'Welcome To The Family'
    assert email_sent.to == [email]

@pytest.mark.django_db
def test_verify_otp_invalid(api_client, create_user):
    # Create a user
    email = 'test@example.com'
    otp = '123456'
    user = create_user(email=email, otp=otp)

    # Prepare request data with invalid OTP
    url = reverse('VerifyRestEmail', args=[email])
    data = {'otp': '654321'}

    # Make a POST request to verify OTP with invalid OTP
    response = api_client.post(url, data, format='json')

    # Print response data for debugging
    print(response.data)

    # Check the response status code
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check the response data
    assert 'detail' in response.data
    assert response.data['detail'] == 'Invalid otp'

    # Print user object for debugging
    print(user.is_active)
    print(user.otp)

    # Check user fields after verification (should not be changed)
    user.refresh_from_db()
    # assert not user.is_active
    assert not user.is_verified
    assert not user.is_logged_in
    assert user.jwt_token is None
    assert user.phone_verified is False














