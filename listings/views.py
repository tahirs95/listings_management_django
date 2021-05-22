from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import BookingInfo, Listing, BlockDay

@csrf_exempt
@api_view(["GET"])
def get_listings(request):
    items = []
    max_price = request.GET.get('max_price', None)
    check_in = request.GET.get('check_in', None)

    if check_in:
        check_in_obj = datetime.strptime(check_in, '%Y-%m-%d')
    
    check_out = request.GET.get('check_out', None)

    if check_out:
        check_out_obj = datetime.strptime(check_out, '%Y-%m-%d')
    
    block_days = BookingInfo.objects.all()
    a = BookingInfo.objects.all()
    print(a.block_days.check_in)
    b = BookingInfo.objects.get(id=4)
    items.append({
        # "listing_type": b.listing.listing_type,
        # "title": b.listing.title,
        # "country": b.listing.country,
        # "city": b.listing.city,
        "price": b.price,
    })
    data = {'items':items}
    return Response(data)
