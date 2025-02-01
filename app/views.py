from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from app.forms import *
from app.core.login import login
from app.core.settings import setting
from app.core.posts import Post
from app.core.search import search
from app.models import user
import re


# Create your views here.
date = datetime.now().date

def home(request):
	if login('','',request).is_logged() == True:
		info = setting(request).get()
		posts = Post(request,'').getLast5()
		return render(request, 'app/index.html', { 'info':info, 'title': 'Home', 'date': date, 'posts':posts, 'next_page':1 })
	else:
		return render(request, 'app/login.html', {'date': date ,'warning':'first you have to login' })



def sign(request):
	if login('','',request).is_logged() == True:
		return HttpResponseRedirect('home')
	else:
		if request.method == 'GET':
			return render(request, 'app/login.html', {'date': date })
		else:
			form = FormLogin(request.POST)
			if form.is_valid():
				username = form.data['username'].strip()
				passw    = form.data['password'].strip()
				signin   = login(username, passw, request)
				response = signin.sign()			
				if response == "None":
					return render(request, 'app/login.html', {'date': date , 'warning':"username or password is invalid!" })
				else:
					return response
			else:
				return render(request, 'app/login.html', {'date': date })
	

def register(request):
	if login('','',request).is_logged() == True:
		return HttpResponseRedirect('home')
	else:
		if request.method == "GET":
			return render(request, 'app/register.html', { 'date': date })
		elif  request.method == "POST":
			form = SignUpForm(request.POST)
			if form.is_valid():
				if len(form.data['password'].strip()) < 6 or form.data['password'].strip() != form.data['passwordconfirm'].strip():
					return render(request, 'app/register.html', { 'sucess':'error', 'warning':'the password fields must be equals and have a length greater than 6 character','date': date })
				if not re.search('[a-z0-9]+@+[a-z]+.com',form.data['email']):
					return render(request, 'app/register.html', { 'sucess':'error', 'warning':'Pealse, enter a valid e-amil','date': date })
				else:
					if setting(request).getusername(form.data['username']) == True:
						return render(request, 'app/register.html', { 'sucess':'error', 'warning':'you no longer can use this username, try another!','date': date })
					elif not re.search('[a-zA-Z]+[0-9]',form.data['username']):
						return render(request, 'app/register.html', { 'sucess':'error', 'warning':'try a valid username: [ e.g: adam564 ]','date': date })
					else:
						newUser = user()
						newUser.email = form.data['email'].strip()
						newUser.username = form.data['username'].strip()
						newUser.password = form.data['password'].strip()
						newUser.setup()
						newUser.save()
						return render(request, 'app/login.html', {'date': date , 'username': str(form.data['username']), 'password': str(form.data['password'])})
			return render(request, 'app/register.html', { 'sucess':'error', 'warning':'fill all the fields correctly','date': date })
		else:
			pass

def profile(request):
	if login('','',request).is_logged() == True:
		info = setting(request).get()
		posts = Post(request,'').getMyLast5()
		return render(request, 'app/profile.html', { 'info':info, 'title': 'Profile','date': date, 'on_profile': True ,'posts':posts } )
	else:
		return HttpResponseRedirect('/logout')
def userprofile(request, id):
	if login('','',request).is_logged() == True:
		info = setting(request).getProfile(id)
		if not info:
			return HttpResponseRedirect('/profile')
		posts = Post(request,'').getAnotherUserLast5(id)
		return render(request, 'app/profile.html', { 'info':info, 'title': 'Profile','date': date,'posts':posts } )
	else:
		return HttpResponseRedirect('/logout')

def post(request):
	if login('','',request).is_logged() == True:
		info = setting(request).get()
		return render(request, 'app/post.html', { 'info':info, 'title': 'Post', 'date': date })
	else:
		return render(request, 'app/login.html', {'date': date ,'warning':'first you have to login' })

def posting(request):
	if login('','',request).is_logged() == True:
		info = setting(request).get()

		if request.method == 'GET':
			return HttpResponseRedirect('/post')			
		elif request.method == 'POST':
			form = FormSimplePost(request.POST, request.FILES)
			if form.is_valid():
				poster = Post(request, form)
				poster.save()
				return HttpResponseRedirect('/')
			return render(request, 'app/post.html', { 'info':info, 'title': 'Post', 'date': date, 'warning':'Fill the post field' })
		else:
			return HttpResponseRedirect('/post')
	else:
		return render(request, 'app/login.html', {'date': date ,'warning':'first you have to login' })

def like(request, id, react):
	if login('','',request).is_logged() == True:
		if react == 'y' or react == 'n':
			like = Post(request, '')
			if like.like(id, react) == True:
				post = Post(request,'').getpost(id)
				return render(request, 'app/seemore.html', { 'title': 'Reading Post','post':post, 'date': date })
			else:
				post = Post(request,'').getpost(id)
				return render(request, 'app/seemore.html', { 'title': 'Reading Post','post':post, 'date': date })
		else:
			post = Post(request,'').getpost(id)
			return render(request, 'app/seemore.html', { 'title': 'Reading Post','post':post, 'date': date })
	else:
		return HttpResponseRedirect('/logout')

def delete(request, id):
	if login('','',request).is_logged() == True:
		deleter = Post(request,'')
		if deleter.delete(id) == True:
			return HttpResponseRedirect('/profile')
		else:
			return render(request, 'app/warning.html', {'title': 'warning', 'date': date, 'warning':'You\'re not the owner of this post, therefore, you can\'t delete it!' })
	else:
		return HttpResponseRedirect('/logout')


def settings(request):
	if login('','',request).is_logged() == True:
		info = setting(request).get()
		return render(request, 'app/settings.html', { 'info': info, 'title': 'Editing profile', 'date':date})
	else:
		return HttpResponseRedirect('/logout')


def seemore(request, id):
	if login('','',request).is_logged() == True:
		post = Post(request,'').getpost(id)
		return render(request, 'app/seemore.html', { 'title': 'Reading Post','post':post, 'date': date } )
	else:
		return HttpResponseRedirect('/logout')

def update(request, option):
	if login('','',request).is_logged() == True:
		if request.method == "GET":
			return HttpResponseRedirect('/profile')	
		elif request.method == "POST":
			info = setting(request).get()
			t = loader.get_template('app/settings.html')
			if option == "photo":
				form = PhotoUpDate(request.POST, request.FILES)
				if form.is_valid():
					if setting(request).updatePhoto(request.FILES['photo']) == True:
						return HttpResponseRedirect('/profile/settings')
				else:
					return HttpResponseRedirect('/profile/settings')
			elif option == 'bio':
				form = updateUserBio(request.POST)
				if form.is_valid():
					bio = form.data['biography'].strip()
					passw = form.data['password'].strip()
					if setting(request).updateBio(bio, passw) == True:
						return HttpResponseRedirect('/profile')
					return render(request, 'app/settings.html', { 'bioWarning':'Please, fill the field correctly', 'title': 'Update Your Infos','info':info, 'date': date } )


			elif option == 'username':
				form = updateUserName(request.POST)
				if form.is_valid():
					username = form.data['username'].strip()
					passw = form.data['password'].strip()
					if setting(request).updateUserName(username, passw) == True:
						return HttpResponseRedirect('/profile')
					else:
						return render(request, 'app/settings.html', { 'usernameWarning':'Please, try another username!', 'title': 'Update Your Infos','info':info, 'date': date } )
				return render(request, 'app/settings.html', { 'usernameWarning':'Please, fill that correctly!', 'title': 'Update Your Infos','info':info, 'date': date } )

			elif option == 'password':
				form = updateUserPass(request.POST)
				if form.is_valid():
					passw = form.data['Opassword'].strip()
					newpassw = form.data['password'].strip()
					if setting(request).updatePassword(passw, newpassw) == True:
						return HttpResponseRedirect('/profile')
				return render(request, 'app/settings.html', { 'passWarning':'Please, fill the field correctly!', 'title': 'Update Your Infos','info':info, 'date': date } )	
			else:
				return HttpResponseRedirect('/profile/settings')
		else:
			return HttpResponseRedirect('/profile/settings')
	else:
		return HttpResponseRedirect('/logout')

def about(request):
	return render(request, 'app/about.html', { 'title': 'About Us', 'date': date })

def logout(request):
	loggerOut = login('', '' ,request)
	return loggerOut.logout()

def deleteAC(request):
	if login('','',request).is_logged() == True:
		return render(request, 'app/delete.html', { 'title': 'Delete Your account','date': date } )
	else:
		return HttpResponseRedirect('/logout')

def deleteACC(request):
	if login('','',request).is_logged() == True:
		if setting(request).delete() == True:
			return HttpResponseRedirect('/logout')
		else:
			return render(request, 'app/delete.html', { 'title': 'Delete Your account','date': date, 'warning':'Sorry <x> something was wrong... Plz, try later' } )
	else:
		return HttpResponseRedirect('/logout')
def searchUser(request):
	if login('','',request).is_logged() == True:
		query = request.GET.get('query')
		if query or query != "":
			users = search(query).searchUsers()
			if not users:
				return render(request,'app/search.html', {'error': 'No user found, try another search'})
			else:
				template = loader.get_template('app/search.html')
				return HttpResponse(template.render({'users':users, 'query': query}, request))
		else:
			return render(request,'app/search.html', {'error': 'fill the search field, please!'})
	else:
		return HttpResponseRedirect('/logout')

def story(request):
	if login('','',request).is_logged() == True:
		if re.search('\d',request.GET.get('next')):
			next = int(request.GET.get('next'))
		else:
			return HttpResponseRedirect('/home')
		
		info = setting(request).get()
		posts = Post(request,'').getStory(next)
		next += 1

		context = { 'info':info, 'title': 'WL story', 'date': date, 'posts':posts, 'next_page':next}
		if len(posts) <= 0:
			context['noPostWarning'] = 'end of the posts'

		return render(request, 'app/index.html', context)
	else:
		return HttpResponseRedirect('/logout')