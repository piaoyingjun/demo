from django.urls import path

from . import views

app_name = 'booking'
urlpatterns = [
    # path('', views.my_debug_view, name='my_debug_view'),
    path('', views.mainpage, name='mainpage'),
    path('listflights/', views.listflights, name='listflights'),
    path('<int:flightid>/', views.flightstoticketflights, name='flightstoticketflights'),
    path('passenger_list/', views.passenger_list, name='passenger_list'),
    path('<str:passenger_name>/', views.passenger_info, name='passenger_name'),

]
