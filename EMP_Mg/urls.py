from django.contrib import admin
from django.urls import path
from office_emp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path('view_emp', views.view_emp, name='view_emp'),
    path("add_emp", views.add_emp, name="add_emp"),
    path("update_emp/", views.update_emp, name="update_emp"),
    # path("update_emp/<int:emp_id>/", views.update_emp, name="update_emp"),
    path("delete_emp", views.delete_emp, name="delete_emp"),
    path("delete_emp/<int:emp_id>", views.delete_emp, name="delete_emp"),
]
