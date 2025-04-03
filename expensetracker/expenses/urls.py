from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.expense_list, name='expense_list'),
    path('expense/create/', views.expense_create, name='expense_create'),
    path('expense/update/<int:expense_id>/', views.expense_update, name='expense_update'),
    path('expense/delete/<int:expense_id>/', views.expense_delete, name='expense_delete'),
]
