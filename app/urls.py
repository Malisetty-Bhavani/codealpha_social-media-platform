from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
   path('register/', views.register_view, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('logout/', views.logout_view, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
]