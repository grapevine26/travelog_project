from django.forms import ModelForm
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django_summernote import fields as summer_fields
from functools import partial
from .models import User, Post


class SignupForm(ModelForm):
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
    field_order = ['username', 'password', 'password_check', 'nickname', 'gender']

    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password', 'nickname', 'gender']


class LoginForm(ModelForm):
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput}
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
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

