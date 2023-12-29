from django.urls import path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('football/', views.football, name='football'),
    path('horse_racing/', views.horse_racing, name='horse_racing'),
    path('tennis/', views.tennis, name='tennis'),
    path('golf/', views.golf, name='golf'),
    path('tipster_league_table/', views.tipster_league_table, name='tipster_league_table'),
    path('latest_tips/', views.latest_tips, name='latest_tips'),
    path('blog/', views.blog, name='blog'),
    path('create-blog/', views.create_blog, name='create_blog'),
    path('blogs/<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
    path('latest-sports-blogs/', views.latest_sports_blogs, name='latest_sports_blogs'),
    path('general_chat/', views.general_chat, name='general_chat'),
    path('in_play/', views.in_play, name='in_play'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('submit-tips/', views.submit_tips, name='submit_tips'),
    path('submission-success/', views.submission_success, name='submission_success'),
    path('football-fixtures/', views.football_fixtures, name='football_fixtures'),
    path('racing-fixtures/', views.racing_fixtures, name='racing_fixtures'),
    path('tennis-fixtures/', views.tennis_fixtures, name='tennis_fixtures'),
    path('golf-fixtures/', views.golf_fixtures, name='golf_fixtures'),
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
