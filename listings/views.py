from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, OuterRef, Subquery, Count, F, functions 
from .models import BookingInfo, Listing, BlockDay, HotelRoom, HotelRoomType

@csrf_exempt
@api_view(["GET"])
def get_listings(request):
    max_price = request.GET.get('max_price', None)
    check_in = request.GET.get('check_in', None)

    if check_in:
        check_in_obj = datetime.strptime(check_in, '%Y-%m-%d')
    
    check_out = request.GET.get('check_out', None)

    if check_out:
        check_out_obj = datetime.strptime(check_out, '%Y-%m-%d')
    
    qs_reserved_room_count = BlockDay.objects \
        .filter(booking = OuterRef('pk')) \
        .values('booking') \
        .annotate(reserved_count = Count('*')) \
        .values('reserved_count') \

    available_bookigs = BookingInfo.objects \
        .annotate(rooms_count = Count('hotel_room_type__hotel_rooms'), reserved_count = functions.Coalesce(Subquery(qs_reserved_room_count), 0)) \
        .filter(Q(rooms_count__gt = F('reserved_count')) | Q(Q(listing__isnull = False) & Q(reserved_count = 0)))

    items = []
    for booking in available_bookigs:
        items.append({
            # "listing_type": info.hotel_room_type.hotel.listing_type,
            # "title": info.hotel_room_type.title,
            # "country": info.hotel_room_type.hotel.country,
            # "city": info.hotel_room_type.hotel.city,
            "rooms_count": booking.rooms_count,
            "reserved_count": booking.reserved_count,
            "title": booking.hotel_room_type.title if booking.hotel_room_type else booking.listing.title,
            "price": booking.price
        })
    data = {'items':items}
    return Response(data)
