from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from .forms import PostForm

# Create your views here.
@login_required(login_url="/login")
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required(login_url="/login")
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required(login_url="/login")
@permission_required("blog.post_new", login_url="/login")
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})