from app.models import user
class search:
	def __init__(self, query):
		self.query = query

	def searchUsers(self):
		try:
			Users = user.objects.filter(username__startswith=self.query.strip())
			return Users
		except:
			return False