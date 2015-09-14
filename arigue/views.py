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
	username = request.session.get('username', '')
	cmdstr = 'free'
	# output = os.system(cmdstr)
	output = os.popen(cmdstr)
	arch = output.read()
	return render_to_response('monitor.html', {'arch': arch, 'username': username})


# assets view
def asset(request):
	username = request.session.get('username', '')
	return render_to_response('asset.html', {'username': username})

# homepage view
def homepage(request):
	username = request.session.get('username', '')
	return render_to_response('homepage.html', {'username': username})


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
	username = request.session.get('username', '')
	return render_to_response('index.html', {'username': username})


# arigue view
def arigue(request):
	username = request.session.get('username', '')
	return render_to_response('index.html', {'username': username})	


# login view
def login(request):
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			md5pwd = md5(password)
			print username, md5pwd
			user = Profile.objects.filter(username__exact=username, password__exact=md5pwd)
  			if user:
				request.session['username'] = username
				return HttpResponseRedirect('/index/')
  	else:
		uf = UserForm()
	return render_to_response('login.html', {'uf': uf})		


# logout view
def logout(request):
	# Delete session when user logout
	del request.session['username']
	return HttpResponseRedirect('/login/')


# Dashboard view
def dashboard(request):
	username = request.session.get('username', '')
	return render_to_response('dashboard.html', {'username': username})


# Server manager view
def server(request):
  	username = request.session.get('username', '')
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
	
	return render_to_response('server.html', {'perPage': perPage, 'username': username})


# Define UserForm model
class UserForm(forms.Form):
	username = forms.CharField(label='',
		widget=forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Username'
		})
	)
	# username = forms.CharField(widget=forms.TextInput)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'placeholder': 'Password'
		})
	)


# Use md5 to screct the user's password
# Just import the md5 module of python.
def md5(string):
	import hashlib
	m = hashlib.md5()
	m.update(string)
	return m.hexdigest()
