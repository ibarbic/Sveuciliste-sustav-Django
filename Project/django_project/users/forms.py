from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, views
from .models import CustomUser, Upisi, Predmeti, Uloge


class UserRegisterForm(UserCreationForm):
    STATUS_CHOICES = [
        ('redovni', 'redovni'),
        ('izvanredni', 'izvanredni'),
        ('none', 'none'),
    ]
    email = forms.EmailField(max_length=64)
    status = forms.CharField(
        max_length=10, widget=forms.Select(choices=STATUS_CHOICES))

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'status']


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=64)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            print(email, password)
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class UpdateUpisiForm(forms.Form):
    class Meta:
        model = Upisi


class PredmetForm(forms.ModelForm):
    IZBORNI_CHOICES = [
        ('da', 'da'),
        ('ne', 'ne'),
    ]
    ime = forms.CharField(max_length=255)
    kod = forms.CharField(max_length=16)
    sem_redovni = forms.IntegerField(label="Semestar (redovni studenti)")
    sem_izvanredni = forms.IntegerField(label="Semestar (izvanredni studenti)")
    izborni = forms.CharField(
        max_length=2, widget=forms.Select(choices=IZBORNI_CHOICES))
    nositelj = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role=2))

    class Meta:
        model = Predmeti
        fields = ['ime', 'kod', 'bodovi', 'sem_redovni',
                  'sem_izvanredni', 'izborni', 'nositelj']


class StudentForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('redovni', 'redovni'),
        ('izvanredni', 'izvanredni'),
        ('none', 'none'),
    ]

    email = forms.EmailField(max_length=64)
    status = forms.CharField(
        max_length=10, widget=forms.Select(choices=STATUS_CHOICES))
    role = forms.ModelChoiceField(
        queryset=Uloge.objects.all())
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'status', 'role', 'username', 'password'
                  ]
