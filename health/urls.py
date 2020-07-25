from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
	path('admin/', admin.site.urls, name='admin'),
	path('', views.home, name='home'),
	path('signup', views.signup, name='signup'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('feedback', views.feedback, name='feedback'),
	path('add_profile', views.add_profile, name='add_profile'),
	path('see_profile', views.see_profile, name='see_profile'),
	path('doctor', views.doctor, name='doctor'),
	path('index', views.index, name='index'),
	path('question', views.question, name='question'),
	path('check_disease', views.check_disease, name='check_disease'),
]
