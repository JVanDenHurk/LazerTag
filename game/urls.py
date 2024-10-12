from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('signup/', views.signup, name='signup'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('scan/<int:player_id>/', views.scan_qr, name='scan_qr'),
]
