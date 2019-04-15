from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostModelForm, CommentForm
from .models import Post, Comment

# Create your views here.
def create(request):
    # 만약 GET 요청이 오면
    if request.method == "POST":
        # 글을 작성하기
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            return redirect('posts:list')
    # 아니면 (GET 요청이 오면)
    else:
        # post를 작성하는 폼을 가져와 template에서 보여줌
        form = PostModelForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create.html', context)

def list(request):
    # 모든 Post를 보여줌
    posts = Post.objects.all()
    
    comment_form = CommentForm()
    context = {
        'posts':posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/list.html', context)
    
def delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    
    if post.user != request.user:
        return redirect('posts:list')
    
    post.delete()
    return redirect('posts:list')

def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.user != request.user:
        return redirect('posts:list')
        
    if request.method == "POST":
        # 수정내용 DB에 반영
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        # 수정 내용 편집
        form = PostModelForm(instance=post)
        context = {
            'form': form,
        }
        return render(request, 'posts/update.html', context)

def create_comments(request, post_id):
    comment_form = CommentForm(request.POST)
    
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
        
        return redirect('posts:list')