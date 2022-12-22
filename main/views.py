from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Batch, Semester, Course, Student, TheoryCourseResult, SessionalCourseResult


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
        return render(request, 'main/semester_view.html', {'batch_no':batch_no, 'semester_no':semester_no, 'courses':courses})
    
    courses = Course.objects.filter(batch_no=batch_no, semester_no=semester_no)
    
    # ***experimental***
    students = Student.objects.filter(batch_no=batch_no)
    print("*"*30)
    
    table_sheet = list()   # a list to store all result records for all students in this semester
    
    for student in students:
        result_entry = dict()   # a dictionary to store result record for each student in this semster
        
        reg_no = student.reg_no
        # print("name:", student.name)
        # print("reg:", student.reg_no)
        result_entry['reg_no'] = reg_no
        result_entry['name'] = student.name
        
        total_credits = 0
        total_GP = 0
        final_LG = None
        for course in courses:
            # ******* Taking theory and sessional result of a student ******
            if course.course_type == "Theory":
                try:
                    course_result = TheoryCourseResult.objects.get(batch_no=batch_no, semester_no=semester_no, reg_no=reg_no)
                except: 
                    course_result = None
            elif course.course_type == "Sessional":
                try:
                    course_result = SessionalCourseResult.objects.get(batch_no=batch_no, semester_no=semester_no, reg_no=reg_no)
                except: 
                    course_result = None
            # _______________________________________________________________
            try: 
                result_entry[course.course_code] = {'credits' : course.course_credits,
                                                    'GP' : course_result.GP,
                                                    'LG' : course_result.LG }
            except:
                result_entry[course.course_code] = {'credits' : course.course_credits,
                                                    'GP' : None,
                                                    'LG' : None }

            total_credits += course.course_credits
            total_GP += course.course_credits * course_result.GP 
        
        final_GP = total_GP / total_credits
        result_entry[f"semester {semester_no}"] = {'credits' : total_credits,
                                                   'GP' : final_GP,
                                                   'LG' : 'X'}
        
    for record in table_sheet:
        print(record)
        
        
    print("*"*30)
    # ******************
    
    return render(request, 'main/semester_view.html', {'batch_no':batch_no, 'semester_no':semester_no, 'courses':courses})


def add_semester(request, batch_no):
    semesters = Semester.objects.filter(batch_no=batch_no)
    semester_no = len(semesters)+1
    semester = Semester.objects.create(batch_no=batch_no, semester_no=semester_no)
    return redirect('/main/')


def course_view(request, batch_no, semester_no, course_type, course_code):
    course_obj = Course.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
    course = course_obj[0] 
    if course_type == "Theory": 
        results = TheoryCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
    elif course_type == "Sessional":
        results = SessionalCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
    
    params = {'course':course,'results':results}
    return render(request, 'main/course_view.html', params)


def students_view(request, batch_no):  
    students = Student.objects.filter(batch_no=batch_no)
    return render(request, 'main/students_view.html', {'batch_no':batch_no, 'students':students})