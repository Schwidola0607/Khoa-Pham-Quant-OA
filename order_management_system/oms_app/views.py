from django.shortcuts import render
from django.http import HttpResponse
from .models import Order


def index(request):
    latest_order_list = Order.objects.order_by("-placed_time")[:5]
    output = "\n\n".join([ord.__str__() for ord in latest_order_list])
    return HttpResponse(output)
