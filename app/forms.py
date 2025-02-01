from django import forms
from django.db import models
from app.models import post, user
import hashlib as hs

class FormLogin(forms.Form):
	username = forms.CharField(max_length=30, required=True)
	password = forms.CharField(max_length=100, required=True)

class FormSimplePost(forms.Form):
	content = forms.CharField(max_length=300,required=True)
	photo  = forms.FileField(required=False)

class PhotoUpDate(forms.Form):
	photo = forms.FileField(required=True)

class updateUserName(forms.Form):
	username = forms.CharField(max_length=12, required=True)
	password = forms.CharField(max_length=100, required=True)

class updateUserBio(forms.Form):
	biography = forms.CharField(max_length=150, required=True)
	password = forms.CharField(max_length=100, required=True)

class updateUserPass(forms.Form):
	Opassword = forms.CharField(max_length=100,min_length=4, required=True)
	password = forms.CharField(max_length=100,min_length=5, required=True)

class SignUpForm(forms.Form):
	email = forms.CharField(max_length=150, required=True)
	username = forms.CharField(max_length=30, required=True)
	password = forms.CharField(max_length=200, required=True)
	passwordconfirm = forms.CharField(max_length=200, required=True)
