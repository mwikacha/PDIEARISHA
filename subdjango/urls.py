from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.homepage, name="homepage"),
    path('login2/', views.login2, name="login2"),
    path('login3/', views.login3, name="login3"),
    path('employeeprofile/', views.employeeprofile, name="employeeprofile"),
    path('leaveapplication/', views.leaveapplication, name="leaveapplication"),
    path('leavehistory/', views.leavehistory, name="leavehistory"),
    path('leavestatus/', views.leavestatus, name="leavestatus"),
    path('leaveoverview/', views.leaveoverview, name="leaveoverview"),
    path('manager1/', views.manager1, name="manager1"),
    path('manageleave/', views.manageleave, name="manageleave"),
    path('employeelist/', views.employeelist, name="employeelist"),
    path('addemployee/', views.addemployee, name="addemployee"),
    path('employeelist2/', views.employeelist2, name="employeelist2"),
    path('edit_employee/<str:employee_name>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<str:employee_name>/', views.delete_employee, name='delete_employee'),
    path('login_details/<str:employee_name>/', views.login_details, name='login_details'),
    path('editleave/<str:start_date>/', views.editleave, name='editleave'),
    path('deleteleave/<str:start_date>/', views.deleteleave, name='deleteleave')
] 

