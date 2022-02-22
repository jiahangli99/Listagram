from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts_index, name='index'),
    path('posts/<int:photo_id>/', views.post_detail, name='detail'),
    path('create/photo/', views.add_photo, name='add_photo'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='photo_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]