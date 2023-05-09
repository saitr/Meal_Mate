from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

#######################Sign UP form##################################

class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-2','placeholder': 'Password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input--style-2','placeholder': 'Email'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class': 'input--style-2','placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2','placeholder': 'Address'}))

    class Meta:
        model = User
        fields = ('username','password', 'email', 'phone_number', 'address',)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
################# verifying the otp form #########################


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


###################Signin form#################################

class SignInForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-2','placeholder': 'Password'}))
    class Meta:
        model = User
        fields = ('username', 'password')




################## changing the user_details form #####################

class ChangeUserDetails(forms.Form):
    # username = forms.CharField(max_length=100,label='Username:')
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'UserName'}))
    # email = forms.EmailField(label='Email:')
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input--style-2', 'placeholder': 'Email'}))
    # phone_number = forms.IntegerField(label="Phone Number:")
    phone_number= forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input--style-2', 'placeholder': 'Phone Number'}))
    # address = forms.CharField(max_length=100,label = 'Address:')
    address= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Address'}))
    display_picture = forms.FileField(label='Change Display Picture',required=False)


#################### Order Form #################################

class OrderForm(forms.Form):
    PAYMENT_CHOICES =(   
    ("CASH ON DELIVERY", "COD"),
    ("UPI", "UPI"),
    ("CARD", "CARD"),
    )

    first_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'First Name'}))

    last_name= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Last Name'}))

    address= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Address'}))

    zip_code= forms.CharField(widget=forms.NumberInput(attrs={'class': 'input--style-2', 'placeholder': 'Zip Code'}))

    place= forms.CharField(widget=forms.TextInput(attrs={'class': 'input--style-2', 'placeholder': 'Place'}))

    payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'required': True}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # Get the user object from kwargs
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['address'].initial = self.user.address # Set the default value of the address field to the user's address

    def save(self, *args, **kwargs):
        # Save the order details here
        pass
