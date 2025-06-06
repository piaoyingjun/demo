from venv import logger
from django.shortcuts import get_list_or_404, get_object_or_404, render

from django.views.generic import ListView
from requests import request
from .models import Flights, TicketFlights


def mainpage(request):
    return render(request, 'booking/mainpage.html')

class ListFights(ListView):
    model = Flights
    template_name = 'booking/flights.html'
    context_object_name = 'flights'

    def get_queryset(self):
        return super().get_queryset().select_related("departure_airport","arrival_airport","aircraft_code")
        #return super().get_queryset().select_related().all()

class FlightsToTicketFlights(ListView):
    model = TicketFlights
    template_name = 'booking/ticketflights.html'
    # def get(self,request,flight_id):
    #     # ticket_flights = get_list_or_404(TicketFlights.objects.select_related(),flight_id=flight_id)
    #     ticket_flights = get_list_or_404(TicketFlights,flight_id=flight_id)
    #     return render(request, "booking/ticketflights.html", {"ticketflights":ticket_flights})
        # query_set = super().get_queryset().select_related("departure_airport","arrival_airport","aircraft_code")


listfights = ListFights.as_view()
flightstoticketflights = FlightsToTicketFlights.as_view()