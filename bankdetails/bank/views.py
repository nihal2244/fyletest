from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Banks, Branches
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

# Create your views here.


def getifsc(request):
    ifsc_code = get_object_or_404(Branches, pk=ifsc)
    print(ifsc_code)
    return HttpResponse(ifsc_code)
