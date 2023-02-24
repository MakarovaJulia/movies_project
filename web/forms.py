from django import forms
from django.contrib.auth import get_user_model

from web.models import Movie, MovieGenre

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class MovieForm(forms.ModelForm):
    release_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))

    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = Movie
        fields = ('title', 'release_date', 'duration', 'image', 'genres')


class MovieGenreForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = MovieGenre
        fields = ('title',)
