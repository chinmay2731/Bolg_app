from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from.models import Post
from .form import PostForm,RegisterForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    all_post = Post.objects.order_by('-publish_date')
    return render(request,'blog/index.html',{'post':all_post})
    #return HttpResponse(all_post)


def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('login')
    else:
        form = RegisterForm()
    return render(response,"registration/register.html",{'form':form})

