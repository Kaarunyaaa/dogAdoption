"""
URL configuration for dogAdoption project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from dogAdoptionapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.login_view),
    path('logout',views.logout_view),
    path('signup/',views.signup),
    path('adminn/',views.adminn),
    path('home/',views.home),
    path('rehome/',views.rehome),
    path('edit/<int:edit_id>/', views.edit),
    path('delete/<int:delete_id>/', views.delete),
    path('availabledogs/',views.availabledogs),
    path('moreDetails/<int:id>/', views.moreDetails, name='moreDetails'),
    path('adopt/<int:id>/', views.adopt_dog, name='adopt_dog'),
    path('dashboard/',views.dashboard),
    #path("adoption_requests/", views.adoption_requests, name="adoption_requests"),
    path("update_adoption_status/<int:id>/", views.update_adoption_status, name="update_adoption_status"),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

