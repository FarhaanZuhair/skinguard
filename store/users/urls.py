"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup/", views.signup,name='signup'),
    path("login/", views.login,name='login'),
    path("logout/", views.logout,name='logout'),
    # path('profilepage/', views.profilepage, name='profilepage'),
    path('profilepage/<int:pk>/', views.profilepage, name='profilepage'),
    path('edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('diagnose/', views.diagnose, name='diagnose'),
    path('view_diagnosis/<int:pk>/', views.view_diagnosis, name='view_diagnosis'),
    path('skin_cancer_diagnose/', views.skin_cancer_diagnose, name='skin_cancer_diagnose'),
    path('view_skin_diagnosis/<int:pk>/', views.view_skin_diagnosis, name='view_skin_diagnosis'),
   

    ]
