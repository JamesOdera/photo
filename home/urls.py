from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/<int:id>/<slug>/', views.image_detail, name='image_detail'),
    path('blog/', views.blog, name='blog'),
    path('add-photo/', views.addPhoto, name='add-photo'),
    path('dashboard/<int:id>/', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile_info/<int:id>/', views.profile_info, name='profile_info'),
    
    path('<int:id>/image_edit/', views.image_edit, name='image_edit'),
    path('<int:id>/image_delete/', views.image_delete, name='image_delete'),
]
