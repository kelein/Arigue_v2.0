from django.db import models

# Create your models here.

# Server Class
class Server(models.Model):
	hostname = models.CharField(max_length=50, unique=True)
	ipaddr = models.GenericIPAddressField(blank=False, null=False, unique=True)
	sysinfo = models.CharField(max_length=50)
	arch = models.CharField(max_length=50)
   	kernal = models.CharField(max_length=50) 	
	mem_total = models.IntegerField() 
	mem_free = models.IntegerField() 
	
	# def __unicode__(self):
	#	return self.ipaddr
	
	def __str__(self):
		return '%s, %s' % (self.hostname, self.ipaddr)

# Profile Class
class Profile(models.Model):
	username = models.CharField(max_length=10, unique=True)
	email = models.EmailField(max_length=20)
	password = models.CharField(max_length=50)
	jobstate = models.BooleanField()
	school = models.CharField(max_length=30)
	job = models.CharField(max_length=30) 
	userimg = models.FileField(upload_to='avatar/%Y%m%d/', max_length=100)

	def __unicode__(self):
		return self.username
