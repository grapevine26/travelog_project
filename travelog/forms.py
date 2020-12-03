from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django_summernote import fields as summer_fields
from functools import partial
from .models import User, Post


class SignupForm(UserCreationForm):
    nickname = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nickname', 'email']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'first_date', 'last_date', 'location', 'route', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'text_area', 'placeholder': '포스트의 제목을 입력하세요.'}),
            'first_date': DatePickerInput(format='%Y-%m-%d'),
            'last_date': DatePickerInput(format='%Y-%m-%d'),
            'location': forms.TextInput(attrs={'class': 'text_area', 'placeholder': '여행 장소를 적어주세요.'}),
            'route': forms.Textarea(attrs={'class': 'textarea_medium', 'placeholder': '여행 장소까지 가는 방법을 공유해주세요.'}),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '500px'}}),
        }
