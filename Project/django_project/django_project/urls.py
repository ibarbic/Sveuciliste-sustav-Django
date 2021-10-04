"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from sveuciliste.views import home
from users.views import registration_view
from users.views import test
from users.views import login_view
from users.views import logout_view
from users.views import student_view_pk
from users.views import mentor_view
from users.views import mentor_studenti_view
from users.views import admin_studenti_redovni_view
from users.views import admin_studenti_izvanredni_view
from users.views import mentor_predmeti_view
from users.views import mentor_predmeti_add_view
from users.views import mentor_predmeti_edit_view
from users.views import admin_studenti_edit_view
from users.views import admin_studenti_add_view
from users.views import admin_mentori_view
from users.views import admin_view
from users.views import admin_studenti_view
from users.views import admin_predmeti_view
from users.views import admin_predmeti_edit_view
from users.views import admin_predmeti_add_view
from users.views import admin_predmeti_studenti_view
from users.views import mentor_predmeti_studenti_view
from users.views import mentor_studenti_neplozeni_view
from users.views import mentor_studenti_polozeni_view
from users.views import mentor_studenti_ispisani_view
from users.views import admin_studenti_zadnja_godina_view
urlpatterns = [
    path('', home, name='home'),
    path('register/', registration_view, name='register'),
    #path('admin/', admin.site.urls),
    path('test/', test, name='test'),
    path('login/', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('student/<int:pk>/', student_view_pk, name='student'),
    path('mentor/', mentor_view, name='mentor'),
    path('mentor_studenti/', mentor_studenti_view, name='mentor_studenti'),
    path('admin_studenti_redovni/', admin_studenti_redovni_view,
         name='admin_studenti_redovni'),
    path('admin_studenti_izvanredni/', admin_studenti_izvanredni_view,
         name='admin_studenti_izvanredni'),
    path('mentor_predmeti/', mentor_predmeti_view, name='mentor_predmeti'),
    path('mentor_predmeti_add/', mentor_predmeti_add_view,
         name='mentor_predmeti_add'),
    path('mentor_predmeti_edit/<int:pk>/',
         mentor_predmeti_edit_view, name='mentor_predmeti_edit'),
    path('admin/', admin_view, name='admin'),
    path('admin_studenti_edit/<int:pk>/',
         admin_studenti_edit_view, name='admin_studenti_edit'),
    path('admin_studenti_add/', admin_studenti_add_view,
         name='admin_studenti_add'),
    path('admin_mentori/', admin_mentori_view, name='admin_mentori'),
    path('admin_studenti/', admin_studenti_view, name='admin_studenti'),
    path('admin_predmeti/', admin_predmeti_view, name='admin_predmeti'),
    path('admin_predmeti_edit/<int:pk>/',
         admin_predmeti_edit_view, name='admin_predmeti_edit'),
    path('admin_predmeti_add/', admin_predmeti_add_view,
         name='admin_predmeti_add'),
    path('admin_predmeti_studenti/<int:pk>/',
         admin_predmeti_studenti_view, name='admin_predmeti_studenti'),
    path('mentor_predmeti_studenti/<int:pk>/',
         mentor_predmeti_studenti_view, name='mentor_predmeti_studenti'),
    path('mentor_studenti_nepolozeni/<int:pk>/',
         mentor_studenti_neplozeni_view, name='mentor_studenti_nepolozeni'),
    path('mentor_studenti_polozeni/<int:pk>/',
         mentor_studenti_polozeni_view, name='mentor_studenti_polozeni'),
    path('mentor_studenti_ispisani/<int:pk>/',
         mentor_studenti_ispisani_view, name='mentor_studenti_ispisani'),
    path('admin_studenti_zadnja_god/',
         admin_studenti_zadnja_godina_view, name='admin_studenti_zadnja_godina'),




]
