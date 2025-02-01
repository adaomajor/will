from app.models import post as posts, user as users, like as likes
from datetime import datetime

class Post:
	def __init__(self, request, form):
		self.request = request
		self.form = form

	def save(self):

		content = self.form.data['content'].strip()
		newpost = posts()
		newpost.content = content
		newpost.timestamp = datetime.now()
		newpost.userID = users.objects.get(pk=self.request.COOKIES['z-will-id'])
		newpost.save()

	def getMyLast5(self):
		post = posts.objects.filter(userID=users.objects.get(pk=self.request.COOKIES['z-will-id'])).order_by('-id')[0:5]
		POSTS = []
		for pst in post:
			ctxt = {
				'id': pst.id,
				'userID': pst.userID,
				'timestamp': pst.timestamp,
				'likes': likes.objects.filter(postID=pst, reaction='y').count(),
				'dislikes' : likes.objects.filter(postID=pst, reaction='n').count(),
			}
			if len(pst.content) > 80:
				ctxt['content'] = pst.content[0:80]
				ctxt['too_long'] = 'too_long'
			else:
				ctxt['content'] = pst.content


			POSTS.append(ctxt)
		return POSTS

	def getLast5(self):
		post = posts.objects.all().order_by('-id')[0:5]
		POSTS = []
		for pst in post:
			ctxt = {
				'id': pst.id,
				'userID': pst.userID,
				'timestamp': pst.timestamp,
				'likes': likes.objects.filter(postID=pst, reaction='y').count(),
				'dislikes' : likes.objects.filter(postID=pst, reaction='n').count(),
			}
			if len(pst.content) > 80:
				ctxt['content'] = pst.content[0:80]
				ctxt['too_long'] = 'too_long'
			else:
				ctxt['content'] = pst.content

			POSTS.append(ctxt)
		return POSTS

	def getAnotherUserLast5(self, userId):
		post = posts.objects.filter(userID=userId).order_by('-id')[0:5]
		POSTS = []
		for pst in post:
			ctxt = {
				'id': pst.id,
				'userID': pst.userID,
				'timestamp': pst.timestamp,
				'likes': likes.objects.filter(postID=pst, reaction='y').count(),
				'dislikes' : likes.objects.filter(postID=pst, reaction='n').count(),
			}
			if len(pst.content) > 35:
				ctxt['content'] = pst.content[0:60]
				ctxt['too_long'] = 'too_long'
			else:
				ctxt['content'] = pst.content
			POSTS.append(ctxt)
		return POSTS


	def like(self, id, reaction):
		try:
			posts.objects.get(pk=id)
		except:
			return False
		
		try:
			oldLike = likes.objects.get(userID=users.objects.get(pk=self.request.COOKIES['z-will-id']), postID=posts.objects.get(pk=id))
			if oldLike.id:
				if oldLike.reaction != reaction:
					likes.objects.filter(userID=oldLike.userID,postID=oldLike.postID).update(reaction=reaction)
					return True
		except:
			like = likes()
			like.userID = users.objects.get(pk=self.request.COOKIES['z-will-id'])
			like.postID = posts.objects.get(pk=id)
			like.reaction = reaction
			like.save()
			return True 


	def delete(self,id):
		try:
			post = posts.objects.get(pk=id, userID=users.objects.get(pk=self.request.COOKIES['z-will-id'])).delete()
			return True
		except:
			return False

	def getpost(self,id):
		try:
			post = posts.objects.get(pk=id)
			POST = {
				'post': post,
				'like': likes.objects.filter(postID=post, reaction='y').count(),
				'dislike': likes.objects.filter(postID=post, reaction='n').count(),
			}

			return POST
		except:
			return

	def getStory(self, index):
		starter = (int(index) * 5)
		offset  = ((int(index) + 1) * 5)
		post = posts.objects.all().order_by('-id')[ starter : offset ]
		POSTS = []
		for pst in post:
			ctxt = {
				'id': pst.id,
				'userID': pst.userID,
				'timestamp': pst.timestamp,
				'likes': likes.objects.filter(postID=pst, reaction='y').count(),
				'dislikes' : likes.objects.filter(postID=pst, reaction='n').count(),
			}
			if len(pst.content) > 80:
				ctxt['content'] = pst.content[0:80]
				ctxt['too_long'] = 'too_long'
			else:
				ctxt['content'] = pst.content

			POSTS.append(ctxt)
		return POSTS


		