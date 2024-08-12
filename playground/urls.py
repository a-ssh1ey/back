from django.urls import path
from . import views

urlpatterns = [
    path('create-deal/', views.create_deal, name='create_deal'),
    path('join-deal/', views.join_deal, name='join_deal'),
    path('get-user-deals/', views.get_user_deals, name='get_user_deals'),  # Новый URL
]
