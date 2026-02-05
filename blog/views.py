from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from blog.forms import BlogForm
from blog.models import Blog

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    # 제목과 본문 모두 검색 대상으로 설정
    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )
        # blogs = blogs.filter(content__icontains=q)

    paginator = Paginator(blogs, 9)
    page = request.GET.get('page')
    object_list = paginator.get_page(page)

    # # 가져온 쿠키 중 key 'visit' 값 가져오고 +1, 기본값 0.
    # visits = int(request.COOKIES.get('visits',0)) + 1

    # # 서버 세션에 키 'count' 저장, 이전 값 없으면 0 시작, 매 요청마다 +1
    # request.session['count'] = request.session.get('count', 0) + 1

    context = {
        # 'blogs':blogs,
        # 'count':request.session['count'],
        'object_list':page_object.object_list,
        'page_obj': page_object,
    }

    # response = render(request, 'blog_list.html', context)
    # # HTTP 응답 객체에 쿠키 헤더를 추가, 키 값:'visits'
    # # Django의 HttpResponse 객체는 self.cookies라는 쿠키저장소, Dict 같음..
    # response.set_cookie('visits',visits)

    return render(request,'blog_list.html',context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog':blog}
    return render(request, 'blog_detail.html', context )

@login_required()
def blog_create(request):
    # if request.user.is_authenticated:
    #     return redirect('login')

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse('fb:detail',kwargs= {'pk': blog.pk} ))

    context = {'form':form}
    return render(request, 'blog_create.html',context)

@login_required()
def blog_update(request, pk):
    # if request.user != blog.author:
    #     raise Http404
    blog = get_object_or_404(Blog, pk=pk, author=request.user)

    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('fb:detail',kwargs={'pk': blog.pk}))

    context = {
        'form':form,
    }

    return render(request,'blog_update.html',context)

@login_required()
# 삭제나 수정은 GET 아니고 POST요청으로 받아야함 (검색엔진,캐시서버, 유저가 뒤로고침,새로고침 할 수있음)
# GET 요청은 폼 제출이나 인증 절차 없어도 실행됨.,
# require_http_methods는 리스트로 받는게, 메서드가 GET, POST 둘 다 허용할수도,, 복수 가능!!
@require_http_methods(['POST'])
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('fb:list'))

