"""
URL configuration for project project.

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
from django.urls import path , include
from tickets import views 
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


routers = DefaultRouter()
routers.register('guests',views.Viewset_Guest)
routers.register('movie',views.Viewset_Movie)
routers.register('reservation',views.Viewset_Reservation)


urlpatterns = [
    path('admin/', admin.site.urls),
    # الطريقه الاولى
    path('django/jsonresponsenomodel/',views.no_rest_no_model,name='no_rest_no_model'),
    
    # الطريقه الثانيه
    path('django/jsonresponsfrommodel',views.no_rest_from_model,name='no_rest_from_model'),

    # POT AND GET الطريقه الثالثه 
    #3.1
    path('rest/FBV_view',views.FBV_view,name='FBV_viwe'),

    # GET AND PUT AND DELETE الطريقه الثالثه 
    # 3.2
    path('rest/FBV_pk/<int:pk>',views.FBV_pk,name='FBV_pk'),

    # الطريقه الرابعه 
    # work with classes
    #4.1
    # rest with GET and POST by Class
    path('rest/CBV_List',views.CBV_List.as_view()),

    # الطريقه الرابعه 
    # work with classes
    #4.2
    # rest with GET and PUT and DELETE by Class
    path('rest/CBV_pk/<int:pk>',views.CBV_Pk.as_view()),


    # هذه الطريقه نستخدم الكلاسات
    #5.1 List and create == GET and POST  
    # with class mixins
    path('rest/mixins_list/',views.Mixins_List.as_view(),name='mixins_list'),


    # الطريقه الخامسه
    #5.2 List and Update and Delete == GET and PUT and DELETE
    # with mixins
    path('rest/mixins_pk/<int:pk>/',views.Mixins_Pk.as_view(),name='mixins_pk'),

    #6
    #6.1 List and create == GET and POST  
    # with class generics
    path('rest/generic_list/',views.Generic_List.as_view(),name='generic_list'),

    #6.2 List and Update and Delete == GET and PUT and DELETE
    # with generics
    path('rest/generic_pk/<int:pk>',views.Generic_pk.as_view(),name='generics_pk'),

    #7
    # use viewset 
    # ⬆⬆⬆ routers استعداء الروابط  من ال 
    path('rest/viewset',include(routers.urls)),

    #8
    #find movie use GET
    path('find_movie',views.find_movie,name='find_movie'),

    #9 
    #create reservation 
    path('create_reservation/',views.create_reservation,name='create_reservation'),


    #10
    # اضافه زر تسجيل وخروج
    path('api-auth',include('rest_framework.urls')),

    #11
    #Token auth
    path('api-token-auth',obtain_auth_token)
    
]
