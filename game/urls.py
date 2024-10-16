from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('account', views.account, name='account'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('signout/', views.signout, name='signout'),
    path('scan', views.scan_qr, name='scan_qr'),
]
