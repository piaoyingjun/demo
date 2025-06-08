from venv import logger
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from django.views.generic import ListView,DetailView
from requests import request
from .models import Flights, TicketFlights, Tickets

from django.db.models import Count

def mainpage(request):
    return render(request, 'booking/mainpage.html')

class ListFlights(ListView):
    model = Flights
    template_name = 'booking/flights.html'
    context_object_name = 'flights'

    def get_queryset(self):
        logger.debug(f"Logging in ListFlights: {self.request}")
        return super().get_queryset().select_related().all()[:100]

class FlightsToTicketFlights(ListView):
    def get(self,request,flightid):
        logger.debug(f"Flight ID: {flightid}")
        # try:
        ticket_flights = get_list_or_404(TicketFlights.objects.select_related("ticket_no"),flight_id=flightid)
        logger.debug(f"Ticket Flights: {ticket_flights}")
        return render(request, "booking/ticketflights.html", {"ticketflights":ticket_flights})
        # except TicketFlights.DoesNotExist:
        #     logger.debug(f"LOG:NO Flight ID: ")
        #     raise Http404("No MyModel matches the given query.")

class PassengerList(ListView):
    model = Tickets
    template_name = 'booking/passengerlist.html'
    context_object_name = 'passengerlist'

    def get_queryset(self):
        logger.debug(f"Logging in PassengerList: {self.request}")
        return super().get_queryset().select_related().values("passenger_name").annotate(pass_count=Count('passenger_name')).order_by('pass_count').reverse().values(*["passenger_name", "pass_count"])[:10]
    
class PassengerInfo(DetailView):
    def get(self, request, passenger_name):
        logger.debug(f"Passenger Name: {passenger_name}")
        passenger_infos = TicketFlights.objects.filter(
            ticket_no__passenger_name=passenger_name
        ).select_related(
            'ticket_no','flight_id','arrival_airpor','aircraft_code'
        ).values(
            'ticket_no__ticket_no',
            'ticket_no__passenger_name',
            'flight_id',
            'fare_conditions',
            'amount',
            'flight_id__scheduled_departure',
            'flight_id__scheduled_arrival',
            'flight_id__actual_departure',
            'flight_id__actual_arrival',
            'flight_id__arrival_airport__airport_name',
            'flight_id__arrival_airport__city',
            'flight_id__arrival_airport__timezone',
            'flight_id__aircraft_code__model'
        )[:200]
        return render(request, "booking/passengerinfo.html", {"passengerinfos": passenger_infos})

listflights = ListFlights.as_view()
flightstoticketflights = FlightsToTicketFlights.as_view()
passenger_list = PassengerList.as_view()
passenger_info = PassengerInfo.as_view()