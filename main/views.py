from django.shortcuts import render
from django.http import HttpResponse
from .models import Batch


def index(request):
    batches = Batch.objects.all()
    if request.method == "POST":
        batch_no = request.POST['batch_no']
        session = request.POST['session']
        batch_id = batch_no + session
        print(batch_id)
        batch = Batch.objects.create(batch_id=batch_id, batch_no=batch_no, session=session)
        batches = Batch.objects.all()
        return render(request, 'main/index.html', {'batches' : batches})
    
    return render(request, 'main/index.html', {'batches' : batches})
        