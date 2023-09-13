from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'records'
urlpatterns = [
    path('', views.login, name='login'),
    path('overview/', views.overview, name='overview'),
    path('record-visitor/', views.record_visitor, name='record_visitor'),
    path('check-out-visitor/<str:visitor_id>/', views.check_out_visitor, name='check_out_visitor'),
    path('visitor-list/', views.visitor_list, name='visitors'),
    path('visitor-list/details/<str:visitor_id>/', views.details, name='details'),
    path('movements/', views.movements, name='movements'),
    path('search/', views.search_visitors, name='search_visitors'),
    path('logout/', views.logout_view, name='logout'),
    path('manual-checkout/', views.manual_checkout, name='manual_checkout'),
    path('delete/<str:visitor_id>/', views.delete_waiting, name='delete_waiting'),
    path('signup/', views.signup, name='signup'),
    path('logs/', views.logs, name='logs'),
    path('all-visitors/', views.all_visitors, name='all_visitors'),
    path('approve/<str:visitor_id>/', views.details, name='approve_visitor'),
    re_path(r'^qr_codes/(?P<visitor_id>\d+).png$', views.get_qr_code, name='get_qr_code'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)