from . import views
from django.urls import path

urlpatterns = [
    # path('curt', views.curtaclan,name='curta'),
    path('cart/get-add', views.CartAPI.as_view(),name='get-add'),
    path('cart/update-item/<int:pk>', views.CartAPI.as_view(),name='update-item'),
    path('cart/delete-item/<int:pk>', views.CartAPI.as_view(),name='delete-item'),
    path('cart/items', views.CategoryAPI.as_view(),name='items'),


]
