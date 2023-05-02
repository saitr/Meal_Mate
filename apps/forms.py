from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm


#######################Sign UP form##################################

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'address', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
################# verifying the otp form #########################


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(label='Enter the OTP', max_length=6)


###################Signin form#################################

class SignInForm(forms.Form):
    username= forms.CharField(max_length=100,label='please enter username')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')


################## changing the email form #####################

class ChangeUserDetails(forms.Form):
    username = forms.CharField(max_length=100,label='Username:')
    email = forms.EmailField(label='Email:')
    phone_number = forms.IntegerField(label="Phone Number:")
    address = forms.CharField(max_length=100,label = 'Address:')





