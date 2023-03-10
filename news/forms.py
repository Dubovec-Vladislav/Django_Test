from django import forms
from .models import News, Comment, ReplyComment
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(
        attrs={"class": "form-control"}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(
        attrs={"class": "form-control", "rows": 5}))
    captcha = CaptchaField()


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Повторите Пароль', widget=forms.PasswordInput(
        attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={"class": "form-control"}))


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = "__all__"
        fields = ["title", "content", "is_published", "category", "photo"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if re.match(r"\d", title):
            raise ValidationError("Название не должно начинаться с цифры")
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "comment", ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = ReplyComment
        fields = ["name", "comment", ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
