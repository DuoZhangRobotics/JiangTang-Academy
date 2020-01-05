from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, TutorialCategory, TutorialSeries, Tutorial, Photo, Github, UserMessage
from django.db import models
from tinymce.widgets import TinyMCE
from form_utils.forms import BetterForm, BetterModelForm
from PIL import Image
from django.core.files import File


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",)
        # exclude = {}

    # "city",
    # "description", "phone", "avatar", "website", "email"


class EditUserInfo(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description',
                  'city',
                  'website',
                  'phone',
                  )


class UserAvatarForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height',)

    def save(self):
        photo = super(UserAvatarForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo


class UploadCourses(forms.ModelForm):
    tutorial_content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Tutorial
        fields = ('tutorial_title', 'tutorial_series', "tutorial_categories", "tutorial_content", "file", "videofile",)


class AddNewCategory(forms.ModelForm):
    class Meta:
        model = TutorialCategory
        exclude = ("category_slug",)


class AddNewSeries(forms.ModelForm):
    class Meta:
        model = TutorialSeries
        exclude = ()


class GithubLogin(forms.ModelForm):
    class Meta:
        model = Github
        fields = ("github_username", "github_password",)
        widgets = {
            "github_password": forms.PasswordInput(attrs={'class': 'form-control'}),
            "github_username": forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserContact(forms.ModelForm):
    message = forms.CharField(widget=TinyMCE(attrs={'placeholder': 'Your Message'}))
    class Meta:
        model = UserMessage
        exclude = ()
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'Your Name'}),
            "email": forms.TextInput(attrs={'placeholder': 'Your Email'}),
            "subject": forms.TextInput(attrs={'placeholder': 'Your Subject'},),
        }
