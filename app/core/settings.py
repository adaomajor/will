from app.models import user
import os, hashlib


class setting:
	def __init__(self, request):
		self.request = request

	def get(self):
		getter = user.objects.get(pk=self.request.COOKIES['z-will-id'])
		info = {
			'userid':getter.pk,
			'username':getter.username,
			'photo': getter.photo,
			'bio':getter.bio
		}
		return info



	def getProfile(self, userId):
		try:
			getter = user.objects.get(pk=userId)
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
			if user.objects.filter(username=username).count() > 0:
				return True
		except:
			return False
	def updateBio(self, bio, password):
		try:
			update = user.objects.filter(pk=self.request.COOKIES['z-will-id'],password=hashlib.md5(password.encode()).hexdigest())
			if update.get().password == hashlib.md5(password.encode()).hexdigest():
				update.update(bio=bio)
				return True	
		except:
			return False

	def updateUserName(self, nickname, password):
		try:
			
			user = update = user.objects.filter(username=nickname)
			if user.get().username:
				return False
		except:
			try:
				update = user.objects.filter(pk=self.request.COOKIES['z-will-id'],password=hashlib.md5(password.encode()).hexdigest())
				if update.get().password == hashlib.md5(password.encode()).hexdigest():
					update.update(username=nickname)

					return True	
			except:
				return False

	def updatePhoto(self, photo):
		with open("./media/z-uploads/willUserPhoto_"+self.request.COOKIES['z-will-id']+".jpg",'wb+') as file:
			for chunk in photo.chunks():
				file.write(chunk)
			file.close()
		try:
			update = user.objects.filter(pk=self.request.COOKIES['z-will-id'])
			if update.get(pk=self.request.COOKIES['z-will-id']):
				update.update(photo="/public/z-uploads/willUserPhoto_"+self.request.COOKIES['z-will-id']+".jpg")
			return True
		except:
			os.unlink("/public/z-uploads/willUserPhoto_"+self.request.COOKIES['z-will-id']+".jpg")
			return False

	def updatePassword(self, password, newpassword):
		try:
			update = user.objects.filter(pk=self.request.COOKIES['z-will-id'],password=hashlib.md5(password.encode()).hexdigest())
			if update.get().password == hashlib.md5(password.encode()).hexdigest():
				update.update(password=hashlib.md5(newpassword.encode()).hexdigest())
				return True	
		except:
			return False

	def delete(self):
		try:
			deleter = user.objects.get(pk=self.request.COOKIES['z-will-id'])
			deleter.delete()
			return True
		except:
			return False