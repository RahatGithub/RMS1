from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Batch, Semester, Course, Student, TheoryCourseResult, SessionalCourseResult
import json


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
    if request.method == "POST":
        batch_no = batch_no
        semester_no = semester_no
        course_code = request.POST['course_code']
        course_title = request.POST['course_title']
        course_credits = request.POST['course_credits']
        course_type = request.POST['course_type']
        course_teacher = request.POST['course_teacher']
        
        course = Course.objects.create(batch_no=batch_no, 
                                       semester_no=semester_no, 
                                       course_code=course_code, 
                                       course_title=course_title, 
                                       course_credits=course_credits,
                                       course_type=course_type,
                                       course_teacher=course_teacher)
        
        courses = Course.objects.filter(batch_no=batch_no, semester_no=semester_no)
        
        return render(request, 'main/semester_view.html', {'batch_no':batch_no, 'semester_no':semester_no, 'courses':courses})
    
    courses = Course.objects.filter(batch_no=batch_no, semester_no=semester_no)
    
    # __________________________________experimental___________________________________
    print("#"*150)
    
    students = Student.objects.filter(batch_no=batch_no)
    table_sheet = list()
    
    for student in students:
        record_entry = dict() 
        record_entry['reg_no'] = student.reg_no
        record_entry['name'] = student.name 
        
        current_semester_credits = 0
        current_semester_total_GP = 0
        final_LG = None
        
        for course in courses:
            try: 
                course_result = TheoryCourseResult.objects.get(reg_no=student.reg_no, batch_no=batch_no, semester_no=semester_no, course_code=course.course_code)
            except:
                course_result = SessionalCourseResult.objects.get(reg_no=student.reg_no, batch_no=batch_no, semester_no=semester_no, course_code=course.course_code)
            
            record_entry[course.course_code] = {'credits' : course.course_credits,
                                                'GP' : course_result.GP, 
                                                'LG' : course_result.LG}
            current_semester_credits += course.course_credits
            current_semester_total_GP += course.course_credits * float(course_result.GP) 
        
        current_semester_final_GPA =  round((current_semester_total_GP/current_semester_credits), 2) 
        record_entry[f"semester {semester_no}"] = {'total_credits' : current_semester_credits,
                                                   'final_GPA' : current_semester_final_GPA,
                                                   'final_LG' : 'X'}
        
        table_sheet.append(record_entry) 
    
        
    
    print("#"*150)
    # _________________________________________________________________________________
    
    return render(request, 'main/semester_view.html', {'batch_no':batch_no, 'semester_no':semester_no, 'courses':courses})


def add_semester(request, batch_no):
    semesters = Semester.objects.filter(batch_no=batch_no)
    semester_no = len(semesters)+1
    semester = Semester.objects.create(batch_no=batch_no, semester_no=semester_no)
    return redirect('/main/')


def course_view(request, batch_no, semester_no, course_type, course_code):
    
    course = Course.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
    
    if request.method == "POST":
        if course_type == "Theory":
            reg_no = request.POST['reg_no']
            part_a_decode = request.POST['part_a_decode']
            part_a_marks = request.POST['part_a_marks']
            part_b_decode = request.POST['part_b_decode']
            part_b_marks = request.POST['part_b_marks']
            assessment_marks = request.POST['assessment_marks']
            total_marks = request.POST['total_marks']
            GP = request.POST['GP']
            LG = request.POST['LG']
            
            TheoryCourseResult.objects.create(reg_no=reg_no, 
                                              batch_no=batch_no, 
                                              semester_no=semester_no,
                                              course_code=course_code,
                                              part_a_decode=part_a_decode,
                                              part_a_marks=part_a_marks,
                                              part_b_decode=part_b_decode,
                                              part_b_marks=part_b_marks,
                                              assessment_marks=assessment_marks,
                                              total_marks=total_marks,
                                              GP=GP,
                                              LG=LG )
            
            results = TheoryCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
            
        elif course_type == "Sessional":
            reg_no = request.POST['reg_no']
            lab_marks = request.POST['lab_marks']
            assessment_marks = request.POST['assessment_marks']
            total_marks = request.POST['total_marks']
            GP = request.POST['GP']
            LG = request.POST['LG']
            
            SessionalCourseResult.objects.create(reg_no=reg_no, 
                                              batch_no=batch_no, 
                                              semester_no=semester_no,
                                              course_code=course_code,
                                              lab_marks=lab_marks,
                                              assessment_marks=assessment_marks,
                                              total_marks=total_marks,
                                              GP=GP,
                                              LG=LG )
            
            results = SessionalCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
        
        params = {'course':course,'results':results}
        return render(request, 'main/course_view.html', params)
    
    else:   
        if course_type == "Theory": 
            results = TheoryCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
        elif course_type == "Sessional":
            results = SessionalCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
        
        params = {'course':course,'results':results}
        return render(request, 'main/course_view.html', params)


def students_view(request, batch_no):  
    students = Student.objects.filter(batch_no=batch_no)
    return render(request, 'main/students_view.html', {'batch_no':batch_no, 'students':students})