from app.models import users
class search:
	def __init__(self, query):
		self.query = query

	def searchUsers(self):
		try:
			Users = users.objects.filter(username__startswith=self.query.strip())
			return Users
		except:
			return False