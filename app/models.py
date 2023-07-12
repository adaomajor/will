from django.db import models
import hashlib as hs
import base64 as b64
import json
import random

# Create your models here.

APP_SECRET_KEY = b64.b64encode("adaomajorappwill2023".encode()).decode()

class users(models.Model):
	id       = models.AutoField(primary_key=True, null=False)
	username = models.CharField(max_length=20, null=False)
	bio      = models.CharField(max_length=150, null=True, default="Hi, I am a WILL's user")
	password = models.CharField(max_length=200,null=False)
	email    = models.EmailField(max_length=50, null=True)
	token    = models.CharField(max_length=300, null=False, default="auth_token")
	photo    = models.CharField(max_length=150,null=True, default="/public/z-uploads/useravatar.jpg")

	def setup(self):
		self.password = hs.md5(str(self.password).encode()).hexdigest()
		authentication_token = { 'APP_SECRET_KEY':APP_SECRET_KEY, 'username':self.username, 'UUID':random.randint(1000, 1000000) }
		self.token    = b64.b64encode(json.dumps(authentication_token).encode()).decode()
		return

	def __str__(self):
		return "%d %s %s" %(self.id, self.username, self.token)

	class Meta:
		db_table = 'users'

class posts(models.Model):
	id        = models.AutoField(primary_key=True, null=False)
	userID    = models.ForeignKey(users, on_delete=models.CASCADE, null=False)
	content   = models.CharField(max_length=300, null=True)
	timestamp = models.DateField(null=False)

	def __str__(self):
		return self.content[0:15]
	class Meta:
		db_table = 'posts'

class likes(models.Model):
	likechoice = (
		('y', 'YES'),
		('n', 'NO'),
	)

	id       = models.AutoField(primary_key=True, null=False)
	userID   = models.ForeignKey(users, on_delete=models.CASCADE, null=False)
	postID   = models.ForeignKey(posts, on_delete=models.CASCADE, null=False)
	reaction = models.CharField(max_length=1, null=False, choices=likechoice, default="y")

	def __str__(self):
		return "%s" %(self.reaction)

	class Meta:
		db_table = 'likes'
