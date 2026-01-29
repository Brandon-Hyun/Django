from django.shortcuts import render, get_object_or_404
from blog.models import Blog

def blog_list(request):
    blogs = Blog.objects.all()

    # 가져온 쿠키 중 key 'visit' 값 가져오고 +1, 기본값 0.
    visits = int(request.COOKIES.get('visits',0)) + 1

    # 서버 세션에 키 'count' 저장, 이전 값 없으면 0 시작, 매 요청마다 +1
    request.session['count'] = request.session.get('count', 0) + 1

    context = {
        'blogs':blogs,
        'count':request.session['count']
    }

    response = render(request, 'blog_list.html', context)
    # HTTP 응답 객체에 쿠키 헤더를 추가, 키 값:'visits'
    # Django의 HttpResponse 객체는 self.cookies라는 쿠키저장소, Dict 같음..
    response.set_cookie('visits',visits)

    return response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog':blog}
    return render(request, 'blog_detail.html', context )
