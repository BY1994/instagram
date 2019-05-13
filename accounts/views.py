from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

# Create your views here.
def signup(request):
    # 회원가입
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 가입된 유저의 Profile 레코드도 함께 생성
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})
    

def login(request):
    if request.method == "POST":
        # 실제 로그인(세션의 유저 정보를 넣는다.)
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
        return redirect('posts:list')
    else:
        # 유저로부터 username과 비밀번호를 받는다.
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form':form})

def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
def profile(request, username):
    # username을 가진 유저의 상세 정보를 보여주는 페이지
    profile = get_object_or_404(get_user_model(), username=username) 
    # User.objects.get(username=username) 이거랑 같다.
    return render(request, 'accounts/profile.html', {'profile': profile})
    
def delete(request):
    # POST 계정을 삭제한다 == DB에서 user를 삭제한다.
    if request.method == "POST":
        request.user.delete()
        return redirect('accounts:signup')
    # GET -> 진짜 삭제 하시겠습니까?
    return render(request, 'accounts/delete.html')
    
@login_required
def follow(request, user_id):
    person = get_object_or_404(get_user_model(), pk=user_id)
    # 만약 이미 팔로우한 사람이라면
    if request.user in person.followers.all():
        person.followers.remove(request.user) # user=request.user
    #  -> 언팔
    # 아니면,
    else:
        person.followers.add(request.user)
    #  -> 팔로우
    return redirect('profile', person.username)
    
@login_required
def change_profile(request):
    # 프로필 정보 수정
    if request.method == "POST":
        profile_form = ProfileForm(data=request.POST,instance=request.user.profile, files=request.FILES) # 
        if profile_form.is_valid():
            profile_form.save()
        return redirect('profile', request.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'accounts/change_profile.html', {'profile_form':profile_form})