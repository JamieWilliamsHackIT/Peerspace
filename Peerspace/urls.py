"""Peerspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('docs/', views.docs_view, name='docs'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('users/', include('django.contrib.auth.urls')),
    path('posts/', include('posts.urls', namespace='posts')),
]


from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,
#                             document_root=settings.STATIC_ROOT),
