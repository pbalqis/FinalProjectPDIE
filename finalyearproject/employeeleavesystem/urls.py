from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexPage, name='index'),
    path("hr_login/", views.HrLogin, name='hr_login'),
    path("emp_login/", views.EmpLogin, name='emp_login'),
    path("hr_dashboard/", views.HrDashboard, name="hr_dashboard"),
    path("emp_dashboard/", views.EmpDashboard, name="emp_dashboard"),
    path("profile/", views.ProfilePage, name="profile"),  
    path("leave/", views.LeavePage, name="leave"),
    path("logout/", views.LogoutPage, name="logout"),

    path("manageemp/", views.ManageEmpPage, name="manage_emp"),
    path("addemp/", views.AddEmpPage, name="add_emp"),
    path('profile/view/<str:employee_ic>/', views.ViewEmp, name='view_employee_profile'),
    path("profile/delete/<str:employee_ic>", views.delete_employee, name="delete_employee"),

    path('profile/update/<str:employee_ic>/', views.UpdatePage, name='profile_update'),
    path('profile/update-data/<str:employee_ic>/', views.UpdateDataProfile, name='update_data_profile'),
    #path("leavestatus/", views.LeaveStatus, name="leave_status"),

    path("manageleave/", views.ManageLeave, name="manage_leave"),

    path('leave/', views.LeavePage, name='leave'),
    path('manage_leave/', views.ManageLeave, name='manage_leave'),
    path('update_leave_status/<int:leave_id>/<str:status>/', views.UpdateLeaveStatus, name='update_leave_status'),
    path("leavestatus/", views.LeaveStatus, name="leave_status"),

    path("adddash/", views.AddNewDash, name="add_dashboard"),
    path('add_dashboard/', views.AddNewDash, name='add_dashboard'),
    path('update_announcement/<int:announcement_id>/', views.update_announcement, name='update_announcement'),
    path('delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),


]
