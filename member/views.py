from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect
from django.urls import reverse

def sign_up(request):
    # username = request.POST.get('username')
    # password1 = request.POST.get('password1')
    # password2 = request.POST.get('password2')
    #
    # print('username', username)
    # print('password1', password1)
    # print('password2', password2)

    # username 중복확인작업
    # 패스워드가 맞는지, 그리고 패스워드 정책에 올바른지 (대소문자)

    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():     # if문 분기 안 할 시(form not valid) form에 에러 넣어서 반환
    #         form.save()
    #         return redirect('/accounts/login/')
    # else:                       # else 없이 바로 form = 선언하면 새로생김. (if에서 탈락한 에러메시지 날라감)
    #     form = UserCreationForm()

    form = UserCreationForm(request.POST or None)
    if form.is_valid():     # if문 분기 안 할 시(form not valid) form에 에러 넣어서 반환
        form.save()
        return redirect(settings.LOGIN_URL)



    context = {
        'form': form
    }
    return render(request, 'registration/signup.html',context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())

        next = request.GET.get('next')
        if next:
            return redirect(next)

        # config/urls.py 에서 name='blog_list' 일치하는 주소로
        return redirect(reverse('blog_list'))

    context = {
        'form': form
    }
    return render(request, 'registration/login.html',context)



