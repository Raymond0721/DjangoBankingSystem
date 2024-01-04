from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('add/', views.BankCreateView, name='bank_add'),
    path('<int:bank_id>/branches/add/', views.BranchCreateView,
         name='add_branch'),
    path('branch/<int:branch_id>/details/', views.BranchDetailView,
         name='branch_detail'),
    path('<int:bank_id>/branches/all/', views.BranchListView,
         name='bank_branches_list'),
    path('branch/<int:branch_id>/edit/', BranchUpdateView.as_view(),
         name='branch_edit'),
    path('all/', BankListView.as_view(), name='bank_list'),
    path('<int:bank_id>/details/', views.BankDetailView, name='bank_detail'),

]
