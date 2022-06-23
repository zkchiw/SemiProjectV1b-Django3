from django.urls import path
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/join/ 경로 요청시 member apps의 join함수가 처리함(views)
    path ('join/', views.join, name= 'join'),
    path ('login/', views.login, name= 'login'),
    path ('logout/', views.logout, name= 'logout'),
    path ('myinfo/', views.myinfo, name= 'myinfo')

]