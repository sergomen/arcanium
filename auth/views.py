from django.shortcuts import render,redirect
from .forms import RegisterForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Post, Comment
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

# Create your views here.
@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        # post_id = request.POST.get("post-id")
        # post = Post.objects.filter(id=post_id).first()
        post = Post.objects.filter(created_at__lte=timezone.now())
        if post and (post.author == request.user or request.user.has_perm("auth.delete_post")):
            post.delete()

    return render(request, 'auth/home.html', {"posts": posts})

@login_required(login_url="/login")
@permission_required("auth.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
    else:
        form = PostForm()
    return render(request, 'auth/create_post.html', {"form": form})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    request_user = request.user

    replies = Comment.objects.filter(post=post).exclude(parent=None)
    
    replyDict = {}
    for reply in replies:
        
        if reply.parent.pk not in replyDict.keys():
            replyDict[reply.parent.pk] = [reply]
        else:
            replyDict[reply.parent.pk].append(reply)
    return render(request, 'auth/post_detail.html', {'post': post, 'request_user': request_user, 'replyDict': replyDict, 'replies': replies})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'auth/add_comment_to_post.html', {'form': form})

def add_reply_to_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        user = request.user
        comment = request.POST.get('comment')
        postPk = request.POST.get('postPk')
        parentPk = request.POST.get('parentPk')
        # print(comment)
        # print("kaka", pk)
        # print("kaka2", postPk, parentPk)
        # print(request.POST)
        if parentPk == "":
            pass
        else:
            parent = Comment.objects.get(pk=parentPk)
            comment = Comment(post=post, author=user, text=comment, parent=parent)
            comment.save()
            # comment = form.save(commit=False)
            # comment.post = post
            # comment.author = request.user
            # comment.save()
            return redirect('post_detail', pk=post.pk)
            # print(comment)
            # comment.success(request, "Your reply has been posted successfully")
    return redirect('post_detail', pk)