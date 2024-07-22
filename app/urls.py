from django.contrib import admin
from django.urls import path
from app import views as app_view
from django.conf.urls.static import static
from django_project import settings

urlpatterns = [
   
    path('',app_view.home,name='home'),
    path('signup',app_view.signup,name='signup'),
    path('student_login',app_view.studentlogin,name = 'userlogin'),
    path('adminlogin',app_view.adminlogin,name='adminlogin'),
    path('Bookdetails',app_view.Bookdetails,name='Bookdetails'),
    path('take',app_view.take,name='take'),
    path('add_book',app_view.lib,name='book'),
    path('updatebook/<pk>',app_view.updatebook,name='updatebook'),
    path('deletebook/<pk>',app_view.deletebook,name='deletebook'),
    path('takebook/<pk>',app_view.takebook,name='takebook'),
    path('retainbook/<pk>',app_view.retainbook,name='retainbook'),
    path('add_cash',app_view.add_cash,name='add_cash')

    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
