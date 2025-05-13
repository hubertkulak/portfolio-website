from django.shortcuts import render
from . models import NewPost
# Create your views here.

def blog(request,*arg, **kwargs):
	posts = NewPost.objects.all().order_by('created_at')
	return render(request ,"blog/blog.html", {'posts': posts})

