from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Comment
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm

# Create your views here.
@login_required(login_url="/login")
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required(login_url="/login")
def news_post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    request_user = request.user

    replies = Comment.objects.filter(post=post).exclude(parent=None)
    # print(replies)
    replyDict = {}
    for reply in replies:
        # print(reply)
        if reply.parent.pk not in replyDict.keys():
            replyDict[reply.parent.pk] = [reply]
        else:
            replyDict[reply.parent.pk].append(reply)
    return render(request, 'blog/post_detail.html', {'post': post, 'request_user': request_user, 'replyDict': replyDict, 'replies': replies})

def news_post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def news_post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required(login_url="/login")
@permission_required("blog.news_post_new", login_url="/login")
def news_post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def news_post_edit(request, pk):
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

def news_post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def news_add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog/post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

def news_comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def news_add_reply_to_comment(request, pk):
    if request.method == "POST":
        # form = CommentForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parend_id'))
            except:
                parend_id = None
            if parent_id:
                parend_obj = Comment.objects.get(id=parent_id)
                if parend_obj:
                    reply_comment = form.save(commit=False)
                    reply_comment.parent = parent_obj
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

def news_add_reply_to_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        user = request.user
        comment = request.POST.get('comment')
        postPk = request.POST.get('postPk')
        parentPk = request.POST.get('parentPk')
        print(comment)
        print("kaka", pk)
        print("kaka2", postPk, parentPk)
        print(request.POST)
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
            return redirect('news_post_detail', pk=post.pk)
            # print(comment)
            # comment.success(request, "Your reply has been posted successfully")
    return redirect('news_post_detail', pk)

