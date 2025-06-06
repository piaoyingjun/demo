from django.urls import path

from . import views

app_name = 'booking'
urlpatterns = [
    # path('', views.my_debug_view, name='my_debug_view'),
    path('', views.mainpage, name='mainpage'),
    path('listfights/', views.listfights, name='listfights'),
    path('<flight_id>/', views.flightstoticketflights, name='flightstoticketflights'),
]
