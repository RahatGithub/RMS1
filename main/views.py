from django.shortcuts import render
from django.http import HttpResponse
from .models import Batch


def index(request):
    batches = Batch.objects.all()
    return render(request, 'main/index.html', {'batches' : batches})