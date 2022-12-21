from django.shortcuts import render
from django.http import HttpResponse
from .models import Batch, Semester, Course, Student


def index(request):
    if request.method == "POST":  # when submitting the 'add batch' form
        batch_no = request.POST['batch_no']
        session = request.POST['session']
        batch_id = batch_no + '_' + session
        batch = Batch.objects.create(batch_id=batch_id, batch_no=batch_no, session=session)
        batches = Batch.objects.all()
        return render(request, 'main/index.html', {'batches' : batches})

    batches = Batch.objects.all()    
    all_batches = list()
    for batch in batches:
        new_dict = dict()
        semester_list = Semester.objects.filter(batch_no=batch.batch_no)
        new_list = list()
        for semester in semester_list: 
            new_list.append(semester)
        new_dict['batch_id'] = batch.batch_id
        new_dict['batch_no'] = batch.batch_no
        new_dict['session'] = batch.session
        new_dict['semesters'] = new_list
        all_batches.append(new_dict)

    return render(request, 'main/index.html', {'all_batches' : all_batches})


def semester_view(request, batch_no, semester_no):  
    courses = Course.objects.filter(batch_no=batch_no, semester_no=semester_no)
    return render(request, 'main/semester_view.html', {'batch_no':batch_no, 'semester_no':semester_no, 'courses':courses})


def students_view(request, batch_no):  
    students = Student.objects.filter(batch_no=batch_no)
    print(students)
    return render(request, 'main/students_view.html', {'batch_no':batch_no, 'students':students})