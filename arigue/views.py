from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, FileResponse
from django.template import loader
from django.contrib import auth
from django.core.paginator import Paginator
from arigue.models import *
from django import forms

import os


# view for test
def base(request):
	return render_to_response('base.html', {})


# monitor view
def monitor(request):
	cmdstr = 'free'
	# output = os.system(cmdstr)
	output = os.popen(cmdstr)
	arch = output.read()
	return render_to_response('monitor.html', {'arch': arch})

# assets view
def asset(request):
	return render_to_response('asset.html', {})

# homepage view
def homepage(request):
	return render_to_response('homepage.html', {})

# Define form model
class UserForm(forms.Form):
	nickname = forms.CharField(label='nickname: ', max_length=10)
	email = forms.EmailField(label='Email: ')
	password = forms.CharField(label='Password: ', widget=forms.PasswordInput())
	jobstate = forms.BooleanField(label='Jobstate: ')
	school = forms.CharField(max_length=30)
	job = forms.ChoiceField(label='Job: ', widget=forms.Select())
	userimg = forms.FileField(label='User Image: ', widget=forms.FileInput)	


# profile view
# Kallen Ding, Agu 31 2015
def profile(request):
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
			nickname = uf.cleaned_data['nickname']
			email = uf.cleaned_data['email']
			password = uf.cleaned_data['password']
			jobstate = uf.cleaned_data['jobstate']
			school = uf.cleaned_data['school']
			job = uf.cleaned_data['job']
			userimg = uf.cleaned_data['userimg']
			# Save data into database
			profile = Profile()
			profile.nickname = nickname
			profile.email = email
			profile.password = password
			profile.jobstate = jobstate
			profile.school = school
			profile.job = job
			profile.userimg = userimg
			profile.save()
			return render_to_response('success.html', {'username': username})
	else:
		uf = UserForm()
	return render_to_response('profile.html', {'uf': uf})


# index view 
def index(request):
 	t = loader.get_template('index.html')	
	return HttpResponse(t.render())

# arigue view
def arigue(request):
	return render_to_response('index.html', {})


# login view
def login(request):
	# print request.POST.get('username')
	# print request.POST.get('password')

	username = request.POST.get('username')
	password = request.POST.get('password')
	user = auth.authenticate(username=username, password=password)
  	
  	if user is not None:
		auth.login(request, user)
  		return HttpResponseRedirect('/dashboard')
  	else:
		return render_to_response('index.html', {'login err': 'Wrong username or password'})		


# logout view
def logout(request):
	return render_to_response('login.html', {})

# Dashboard view
def dashboard(request):
	return render_to_response('dashboard.html', {'user': request.user})

# Server manager view
def server(request):
  	t = loader.get_template('server.html')
	# Get all objects in model Server
	allServers = Server.objects.all()
	# Records of each page
	pageSize = 5
	# Instance a Paginator object 
	paginator = Paginator(allServers, pageSize)	
	# Total page number
	pageCount = paginator.num_pages
	print "Total Page: %s" % pageCount

	# ## Exception Solutino ##	
	try:
  		pageIndex = int(request.GET.get('page', '1'))
		print "Page Index: %s" % pageIndex
	except ValueError:
		pageIndex = 1
		perPage = paginator.page(pageIndex)	
	# Raised when page() is given a valid value but 
	# no objects exist on that page.
	try:
		perPage = paginator.page(pageIndex)	
	except (EmptyPage, InvaildPage):
		perPage = paginator.page(pageCount)	
	
	return render_to_response('server.html', {'perPage': perPage})
