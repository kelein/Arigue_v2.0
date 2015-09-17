from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse, FileResponse
from django.template import loader
from django.contrib import auth
from django.core.paginator import Paginator
from arigue.models import *
from arigue.form import *
import os


# view for modify user password
# def setting(request):
# 	if request.method == 'POST':
# 		pwdForm = PwdForm(request.POST)
# 		print pwdForm.as_p
		
# 		if pwdForm.is_valid():
# 			username = request.session.get('username', 'None')
# 			oldPwd = request.POST.get()
# 			user = auth.authenticate(username=username, password=oldPwd)
# 			if user is not None and user.is_active:
# 				newPwd = request.POST.get('newPwd', '')
# 				user.set_password(newPwd)
# 				user.save()
# 				return render_to_response('base.html', {'pwdForm': pwdForm})
# 			else:
# 				return render_to_response('', )
# 	else:
# 		pwdForm = PwdForm()
# 	return render_to_response('base.html', {'pwdForm': pwdForm})


# Rewirte setting view for user password modify.
def setting(request):
	username = request.session.get('username', 'None')
	if request.method == 'POST':
		pf = PwdForm(request.POST)
		if pf.is_valid():
			newPwd = pf.cleaned_data['newpassword']
			md5pwd = md5(newPwd)
			print newPwd, md5pwd
			user = Profile.objects.filter(username__exact=username)
			user.password = md5pwd
			user.save()
			# return render_to_response('base.html', {'username': username})
			return HttpResponseRedirect(request.META['HTTP_REFERRER'])
	else:
		pf = PwdForm()
	return render_to_response('base.html', {'pf': pf, 'username': username})
	

# view for test
def base(request):
	username = request.session.get('username', 'None')
	pf = PwdForm(request.POST)
	return render_to_response('base.html', {'username': username, 'pf': pf})


# monitor view
def monitor(request):
	username = request.session.get('username', 'None')
	cmdstr = 'free'
	# output = os.system(cmdstr)
	output = os.popen(cmdstr)
	arch = output.read()
	return render_to_response('monitor.html', {'arch': arch, 'username': username})


# assets view
def asset(request):
	username = request.session.get('username', 'None')
	return render_to_response('asset.html', {'username': username})

# homepage view
def homepage(request):
	username = request.session.get('username', 'None')
	return render_to_response('homepage.html', {'username': username})


# profile view
def profile(request):
	username = request.session.get('username', 'None')
	user = Profile.objects.get(username=username)
	print '==================profile view================='
	print user.username, user.userimg
	return render_to_response('profile.html', {'user': user})


# index view 
def index(request):
	username = request.session.get('username', 'None')
	return render_to_response('index.html', {'username': username})


# arigue view
def arigue(request):
	username = request.session.get('username', 'None')
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
	username = request.session.get('username', 'None')
	return render_to_response('dashboard.html', {'username': username})


# Server manager view
def server(request):
  	username = request.session.get('username', 'None')
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


# Use md5 to secret user's password
# Just import the md5 module of python.
def md5(string):
	import hashlib
	m = hashlib.md5()
	m.update(string)
	return m.hexdigest()
