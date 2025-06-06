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
        # try:
        # passenger_infos = get_list_or_404(TicketFlights.objects.select_related("ticket_no"), passenger_name=passenger_name)
        # passenger_infos = TicketFlights.objects.filter(ticket_no__passenger_name=passenger_name)
        passenger_infos = TicketFlights.objects.filter( \
            ticket_no__passenger_name=passenger_name \
            ).values( \
                'ticket_no__ticket_no', \
                'ticket_no__passenger_name', \
                'flight_id', \
                'fare_conditions', \
                'amount' \
            )
        logger.debug(f"Passenger Info: {passenger_infos}")
        return render(request, "booking/passengerinfo.html", {"passengerinfos": passenger_infos})
        # except TicketFlights.DoesNotExist:
        #     logger.debug(f"LOG:NO Passenger Name: ")
        #     raise Http404("No MyModel matches the given query.")

listflights = ListFlights.as_view()
flightstoticketflights = FlightsToTicketFlights.as_view()
passenger_list = PassengerList.as_view()
passenger_info = PassengerInfo.as_view()