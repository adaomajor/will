from app.models import users
import os, hashlib


class setting:
	def __init__(self, request):
		self.request = request

	def get(self):
		getter = users.objects.get(pk=self.request.COOKIES['z-will-id'])
		info = {
			'userid':getter.pk,
			'username':getter.username,
			'photo': getter.photo,
			'bio':getter.bio
		}
		return info



	def getProfile(self, userId):
		try:
			getter = users.objects.get(pk=userId)
			info = {
				'userid':getter.pk,
				'username':getter.username,
				'photo': getter.photo,
				'bio':getter.bio
			}
			return info
		except:
			return False

	def getusername(self, username):
		try:
			if users.objects.filter(username=username).count() > 0:
				return True
		except:
			return False
	def updateBio(self, bio, password):
		try:
			update = users.objects.filter(pk=self.request.COOKIES['z-will-id'],password=hashlib.md5(password.encode()).hexdigest())
			if update.get().password == hashlib.md5(password.encode()).hexdigest():
				update.update(bio=bio)
				return True	
		except:
			return False

	def updateUserName(self, nickname, password):
		try:
			
			user = update = users.objects.filter(username=nickname)
			if user.get().username:
				return False
		except:
			try:
				print("updating username")
				update = users.objects.filter(pk=self.request.COOKIES['z-will-id'],password=hashlib.md5(password.encode()).hexdigest())
				if update.get().password == hashlib.md5(password.encode()).hexdigest():
					update.update(username=nickname)

					print("updating username2")
					return True	
			except:
				return False

	def updatePhoto(self, photo):
		with open("./media/z-uploads/billUserPhoto_"+self.request.COOKIES['z-will-id']+".jpg",'wb+') as file:
			for chunk in photo.chunks():
				file.write(chunk)
			file.close()
		try:
			update = users.objects.filter(pk=self.request.COOKIES['z-will-id'])
			if update.get(pk=self.request.COOKIES['z-will-id']):
				update.update(photo="/public/z-uploads/billUserPhoto_"+self.request.COOKIES['z-will-id']+".jpg")
			return True
		except:
			os.unlink("/public/z-uploads/billUserPhoto_"+self.request.COOKIES['z-will-id']+".jpg")
			return False

	def updatePassword(self, password, newpassword):
		try:
			update = users.objects.filter(pk=self.request.COOKIES['z-will-id'],password=hashlib.md5(password.encode()).hexdigest())
			if update.get().password == hashlib.md5(password.encode()).hexdigest():
				update.update(password=hashlib.md5(newpassword.encode()).hexdigest())
				return True	
		except:
			return False

	def delete(self):
		try:
			deleter = users.objects.get(pk=self.request.COOKIES['z-will-id'])
			deleter.delete()
			return True
		except:
			return False