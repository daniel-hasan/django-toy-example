"""web_pirates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from toy.views.with_form import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ListPerson.as_view(),name="home"),


    path('edit/<int:person_id>/', PersonUpdate.as_view(),name="editar_dados"),
    path('salvar_dados/<str:redirect_to>/', PersonUpdate.as_view(),name="salvar_dados"),

    path('eye_color/<int:person_id>/', EyeColorUpdate.as_view(),name="cor_do_olho"),
    path('salvar_olho/<str:redirect_to>/', EyeColorUpdate.as_view(),name="salvar_olho"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
