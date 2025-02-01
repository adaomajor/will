from django.http import HttpResponse, HttpResponseRedirect
from app.models import user
import hashlib as hs
class login():
	def __init__(self, username, passw, request):
		self.request = request
		self.username = username
		self.passw = hs.md5(str(passw).encode()).hexdigest()

	def sign(self):
		try:
			User = user.objects.get(username=self.username, password=self.passw)
			if User.pk:
				response = HttpResponseRedirect('/')
				response.set_cookie('z-will-state','online')
				response.set_cookie('z-will-token',User.token)
				response.set_cookie('z-will-user',User.username)
				response.set_cookie('z-will-id',User.pk)
				return response
			else:
				return "None"
		except:
			return "None"

	def logout(self):
		response = HttpResponseRedirect('/login')
		for cook in self.request.COOKIES:
			response.delete_cookie(cook)
		return response

	def is_logged(self):
		if 'z-will-state' in self.request.COOKIES and 'z-will-id' in self.request.COOKIES and 'z-will-user' in self.request.COOKIES and 'z-will-token' in self.request.COOKIES:
			try:
				User = user.objects.get(pk=int(self.request.COOKIES['z-will-id']) ,username=self.request.COOKIES['z-will-user'], token=self.request.COOKIES['z-will-token'])
				return True
			except:
				return False
		else:
			return False



