from django.urls import path
from .views import recommend_products_view

urlpatterns = [
    path('recommend/<int:user_id>/', recommend_products_view, name='recommend_products'),
]
