from django.contrib.auth.models import User
from .models import *
from django import forms


class ImageEditForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'category', 'image',)
        
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
            }),
            'image': forms.FileInput(attrs={
                
            }),
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Enter username...'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password...'}))


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    email = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        help_texts = {
            'username': None,
            'email': None,
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password Missmatch')
        return confirm_password
    
    
    
class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder':'Share Something about yourself...'
            }),
            'photo': forms.FileInput(attrs={
                
            }),
        }