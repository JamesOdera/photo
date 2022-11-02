from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
     # USER AUTHENTICATION
    path('signin/', views.user_login, name='signin'),
    path('logout/', views.user_logout, name='user_logout'),
    path('signup/', views.signup, name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
