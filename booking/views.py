from venv import logger
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from django.views.generic import ListView,DetailView
from requests import request
from .models import AircraftsData, BoardingPasses, Flights, TicketFlights, Tickets

from django.db.models import Count,Subquery, OuterRef

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
        # 修正されたSubqueryを定義します
        ticket_flight_amount = TicketFlights.objects.filter(
            ticket_no=OuterRef('ticket_no'), 
            flight=OuterRef('flight')  # 修正点
        ).values('amount')[:1]

        ticket_flight_fare = TicketFlights.objects.filter(
            ticket_no=OuterRef('ticket_no'),
            flight=OuterRef('flight')  # 修正点
        ).values('fare_conditions')[:1]


        # メインクエリを構築します（この部分は変更不要）
        passenger_infos = BoardingPasses.objects.filter(
            ticket_no__passenger_name=passenger_name
        ).select_related(
            'ticket_no__book_ref',
            'flight__departure_airport',
            'flight__arrival_airport',
            'flight__aircraft_code'
        ).annotate(
            amount=Subquery(ticket_flight_amount),
            fare_conditions=Subquery(ticket_flight_fare)
        ).values(
            'seat_no',
            'boarding_no',
            'amount',
            'fare_conditions',
            'ticket_no__ticket_no',
            'ticket_no__passenger_name',
            'ticket_no__book_ref__book_date',
            'ticket_no__book_ref__total_amount',
            'flight__flight_no',
            'flight__status',
            'flight__scheduled_departure',
            'flight__scheduled_arrival',
            'flight__arrival_airport__airport_name',
            'flight__arrival_airport__city',
            'flight__aircraft_code__model'
        )[:200]

        # 実行されたSQL
        # SELECT "boarding_passes"."seat_no" AS "seat_no",
        #     "boarding_passes"."boarding_no" AS "boarding_no",
        #     (
        #         SELECT U0."amount" AS "amount"
        #         FROM "ticket_flights" U0
        #         WHERE (U0."flight_id" = ("boarding_passes"."flight_id") AND U0."ticket_no" = ("boarding_passes"."ticket_no"))
        #         LIMIT 1
        #     ) AS "amount",
        #     (
        #         SELECT U0."fare_conditions" AS "fare_conditions"
        #         FROM "ticket_flights" U0
        #         WHERE (U0."flight_id" = ("boarding_passes"."flight_id") AND U0."ticket_no" = ("boarding_passes"."ticket_no"))
        #         LIMIT 1
        #     ) AS "fare_conditions",
        #     "boarding_passes"."ticket_no" AS "ticket_no__ticket_no",
        #     "tickets"."passenger_name" AS "ticket_no__passenger_name",
        #     "bookings"."book_date" AS "ticket_no__book_ref__book_date",
        #     "bookings"."total_amount" AS "ticket_no__book_ref__total_amount",
        #     "flights"."flight_no" AS "flight__flight_no",
        #     "flights"."status" AS "flight__status",
        #     "flights"."scheduled_departure" AS "flight__scheduled_departure",
        #     "flights"."scheduled_arrival" AS "flight__scheduled_arrival",
        #     "airports_data"."airport_name" AS "flight__arrival_airport__airport_name",
        #     "airports_data"."city" AS "flight__arrival_airport__city",
        #     "aircrafts_data"."model" AS "flight__aircraft_code__model"
        # FROM "boarding_passes"
        # INNER JOIN "tickets"
        #     ON ("boarding_passes"."ticket_no" = "tickets"."ticket_no")
        # INNER JOIN "flights"
        #     ON ("boarding_passes"."flight_id" = "flights"."flight_id")
        # INNER JOIN "bookings"
        #     ON ("tickets"."book_ref" = "bookings"."book_ref")
        # INNER JOIN "airports_data"
        #     ON ("flights"."arrival_airport" = "airports_data"."airport_code")
        # INNER JOIN "aircrafts_data"
        #     ON ("flights"."aircraft_code" = "aircrafts_data"."aircraft_code")
        # WHERE "tickets"."passenger_name" = 'TATYANA IVANOVA'
        # LIMIT 200

        return render(request, "booking/passengerinfo.html", {"passengerinfos": passenger_infos})

listflights = ListFlights.as_view()
flightstoticketflights = FlightsToTicketFlights.as_view()
passenger_list = PassengerList.as_view()
passenger_info = PassengerInfo.as_view()