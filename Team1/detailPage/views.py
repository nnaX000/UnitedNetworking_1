from django.shortcuts import render, get_object_or_404
import pandas as pd
from django.conf import settings
from django.http import Http404

def detailPage(request):
    return render(request, 'detailed_center.html')
