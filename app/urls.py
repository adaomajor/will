from django.urls import path
from app import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.sign, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('profile/id/<int:id>', views.userprofile),
    path('profile/settings', views.settings, name='settings'),
    path('home', views.home, name='home'),
    path('post', views.post, name='post'),
    path('posting', views.posting, name='posting'),
    path('like/<int:id>/<str:react>', views.like, name='like'),
    path('delete/post/<int:id>', views.delete, name='delete'),
    path('see/<int:id>', views.seemore, name='seemore'),
    path('update/<str:option>', views.update, name='update'),
    path('about', views.about, name='about'),
    path('profile/settings/delete/account', views.deleteAC, name='delete'),
    path('delete/delete/delete', views.deleteACC),
    path('search', views.searchUser),
    path('story', views.story),
]

