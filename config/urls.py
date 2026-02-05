from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import include,path
from blog import views
from member import views as member_views
from django.views.generic import TemplateView, RedirectView
from django.views import View
from blog import cb_views

class AboutView(TemplateView):
    template_name = 'about.html'

class TestView(View):
    def get(self, request):
        return render(request,'test_get.html')

    def post(self, request):
        return render(request,'test_post.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('blog.urls')),
    path('fb/', include('blog.fbv_urls')),
    # path('<int:pk>/', views.blog_detail, name='blog_detail'),
    # path('create/', views.blog_create, name='blog_create'),
    # path('<int:pk>/update/', views.blog_update, name= 'blog_update'),
    # path('<int:pk>/delete/', views.blog_delete, name= 'blog_delete'),

    # Auth
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/',member_views.sign_up,name='signup'),
    path('login/',member_views.login, name='login'),
    # path('about', AboutView.as_view(), name='about'),
    # path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    # path('redirect2/',lambda req: redirect('about')),
    # path('test/', TestView.as_view(), name='test'),
    #
    # path('', cb_views.BlogListView.as_view(), name='list'),
    # path('<int:pk>/', cb_views.BlogDetailView.as_view(), name='detail'),
    # path('create/', cb_views.BlogCreateView.as_view(), name='create'),
    # path('<int:pk>/update/',cb_views.BlogUpdateView.as_view(), name='update'),
    # path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='delete'),
]
