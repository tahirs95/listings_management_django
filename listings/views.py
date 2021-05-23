from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, OuterRef, Subquery, Count, F
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
    
    block_days = BookingInfo.objects.all()
    a = BookingInfo.objects.all()
    b = BookingInfo.objects.get(id=4)
    print(b.block_days)
    # infos = BookingInfo.objects.filter(~Q(block_days__check_in__lt = datetime.now()))
    # qs_hotal_rooms_count = HotelRoom.objects.filter(hotel_room_type = OuterRef('pk')).annotate(room_count = Count('pk'))
    reserved_room_count = BlockDay.objects.filter(booking__hotel_room_type = OuterRef('pk')).annotate(blocked_count = Count('booking__hotel_room_type')).values('blocked_count')
    testing = HotelRoomType.objects.annotate(rooms_count = Count('hotel_rooms'), blocked_count = Count('booking_info__block_days'))
    # .filter(rooms_count__gt = Subquery(reserved_room_count))
    print(testing)
    infos = BookingInfo.objects.filter(block_days__check_in__lt = datetime.now())
    items = []
    for info in testing:
        items.append({
            # "listing_type": info.hotel_room_type.hotel.listing_type,
            # "title": info.hotel_room_type.title,
            # "country": info.hotel_room_type.hotel.country,
            # "city": info.hotel_room_type.hotel.city,
            "rooms_count": info.rooms_count,
            "blocked_count": info.blocked_count,
            "title": info.title

        })
    data = {'items':items}
    return Response(data)
