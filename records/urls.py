from django.urls import path
from . import views

app_name = 'records'
urlpatterns = [
    path('', views.login, name='login'),
    path('overview/', views.overview, name='overview'),
    path('record-visitor/', views.record_visitor, name='record_visitor'),
     path('check-out-visitor/<str:visitor_id>/', views.check_out_visitor, name='check_out_visitor'),
    path('visitor-list/', views.visitor_list, name='visitors'),
    path('visitor-list/details/<str:visitor_id>', views.details, name='details'),
    path('approve/<str:visitor_id>/', views.details, name='approve_visitor'),
    path('movements/', views.movements, name='movements'),
    path('search/', views.search_visitors, name='search_visitors'),
    path('logout/', views.logout_view, name='logout'),
    path('manual-checkout/', views.manual_checkout, name='manual_checkout'),
    path('delete/<str:visitor_id>/', views.delete_waiting, name='delete_waiting'),
    path('signup/', views.signup, name='signup'),

]