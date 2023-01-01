from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Batch, Semester, Course, Student, TheoryCourseResult, SessionalCourseResult, Result
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
        
        result = Result.objects.filter(batch_no=batch_no, semester_no=semester_no)
        
        return render(request, 'main/semester_view.html', {'batch_no':batch_no, 'semester_no':semester_no, 'courses':courses, 'result':result})
    
    # if not a POST request:
    courses = Course.objects.filter(batch_no=batch_no, semester_no=semester_no)
    students = Student.objects.filter(batch_no=batch_no)
    result_objects = Result.objects.filter(batch_no=batch_no, semester_no=semester_no)
    
    table_sheet = list()
    for result in result_objects:
        a_record = dict()
        a_record['reg_no'] = result.reg_no
        student = Student.objects.filter(batch_no=batch_no, reg_no=result.reg_no).first()
        a_record['name'] = student.name 
        a_record['batch_no'] = result.batch_no
        a_record['semester_no'] = result.semester_no
        a_record['course_results'] = json.loads(result.course_results)
        a_record['current_semester_credits'] = result.current_semester_credits
        
        # ********* Current semester GPA: **********************
        a_record['current_semester_GPA'] = result.current_semester_GPA
        # ******************************************************
        
        # ********* Current semester LG: **********************
        GPA = result.current_semester_GPA
        if GPA == 4.00 : LG = "A+"
        elif GPA >= 3.75 : LG = "A"
        elif GPA >= 3.50 : LG = "A-" 
        elif GPA >= 3.25 : LG = "B+"
        elif GPA >= 3.00 : LG = "B"
        elif GPA >= 2.75 : LG = "B-"
        elif GPA >= 2.50 : LG = "C+"
        elif GPA >= 2.25 : LG = "C"
        elif GPA >= 2.00 : LG = "C-" 
        else: LG = "F"
        a_record['current_semester_LG'] = LG
        # ******************************************************
        
        # ******** Overall credits, CGPA, LG *******************
        if result.semester_no > 1:
            prev_results = []
            for sem in range(1, semester_no):
                try:
                    semester = Result.objects.get(batch_no=batch_no, reg_no=result.reg_no, semester_no=sem)
                    prev_results.append(semester)
                except:
                    pass
            
            overall_credits, overall_point = result.current_semester_credits, result.current_semester_total_point
            
            for res in prev_results:
                overall_credits += res.current_semester_credits
                overall_point += res.current_semester_total_point
            
            a_record['overall_credits'] = overall_credits
            a_record['overall_CGPA'] = round((overall_point/overall_credits), 2) 
            
            CGPA = a_record['overall_CGPA']
            if CGPA == 4.00 : LG = "A+"
            elif CGPA >= 3.75 : LG = "A"
            elif CGPA >= 3.50 : LG = "A-" 
            elif CGPA >= 3.25 : LG = "B+"
            elif CGPA >= 3.00 : LG = "B"
            elif CGPA >= 2.75 : LG = "B-"
            elif CGPA >= 2.50 : LG = "C+"
            elif CGPA >= 2.25 : LG = "C"
            elif CGPA >= 2.00 : LG = "C-" 
            else: LG = "F"
            a_record['overall_LG'] = LG
        # ******************************************************
        
            a_record['range'] = range(2*(len(courses)-len(a_record['course_results'])))
            
        table_sheet.append(a_record)
    
    return render(request, 'main/semester_view.html', {'batch_no':batch_no, 'semester_no':semester_no, 'courses':courses, 'table_sheet':table_sheet})


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
                                              GP=float(GP),
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
                                                 GP=float(GP),
                                                 LG=LG )
            
            results = SessionalCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
        
        # try to get the Result for this particular reg_no, then update this :
        try: 
            result_individual = Result.objects.get(reg_no=reg_no, batch_no=batch_no, semester_no=semester_no)  
            course_results = json.loads(result_individual.course_results)
            course_results[course.course_code] = {'credits' : course.course_credits,
                                                  'GP' : GP,
                                                  'LG' : LG }
            result_individual.course_results = json.dumps(course_results)
            if float(GP) >= 2: 
                result_individual.current_semester_credits += course.course_credits
                result_individual.current_semester_total_point += float(GP)*course.course_credits  
                result_individual.current_semester_GPA = round((result_individual.current_semester_total_point / result_individual.current_semester_credits), 2)

            result_individual.save()
            
        # if there are no Result found for this particular reg_no, then create one: 
        except:
            # *****Finding the result of this course and converting into JSON*****
            course_results = dict()
            course_results[course.course_code] = {'credits' : course.course_credits,
                                                  'GP' : GP,
                                                  'LG' : LG }
            course_results_json = json.dumps(course_results)  # converting the dict to str(JSON)
            # ********************************************************************
            
            
            # **********Finding current semester total credits and total points**********
            if float(GP) >= 2: 
                current_semester_credits = course.course_credits
                current_semester_total_point = round((float(GP) * current_semester_credits), 2)
                current_semester_GPA = float(GP)
            else : 
                current_semester_credits = 0
                current_semester_total_point = 0
                current_semester_GPA = 0
            # ***************************************************************************
            
            result_individual = Result.objects.create(reg_no=reg_no, 
                                                      batch_no=batch_no, 
                                                      semester_no=semester_no,
                                                      course_results=course_results_json,
                                                      current_semester_credits=current_semester_credits,
                                                      current_semester_total_point=current_semester_total_point, 
                                                      current_semester_GPA=current_semester_GPA)
        
        params = {'course':course,'results':results}
        return render(request, 'main/course_view.html', params)
    
    else:   # if not a POST request
        if course_type == "Theory": 
            results = TheoryCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
        elif course_type == "Sessional":
            results = SessionalCourseResult.objects.filter(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
        
        params = {'course':course,'results':results}
        return render(request, 'main/course_view.html', params)


def students_view(request, batch_no):  
    students = Student.objects.filter(batch_no=batch_no)
    return render(request, 'main/students_view.html', {'batch_no':batch_no, 'students':students})


def gradesheet_view(request, session, reg_no):
    batch = Batch.objects.get(session=session)
    batch_no = batch.batch_no
    student = Student.objects.get(reg_no=reg_no)
    student_name = student.name 
    
    gradesheet = list()
    semester_results = Result.objects.filter(reg_no=reg_no)
    for result in semester_results:
        this_semester = list()
        course_results = json.loads(result.course_results)
        for cour in course_results.items():
            course_info = dict()
            course_info['course_code'] = cour[0]
            course = Course.objects.filter(batch_no=batch_no, course_code=cour[0]).first() 
            course_info['course_title'] = course.course_title
            course_info['credits'] = course.course_credits
            course_info['GP'] = cour[1]['GP']
            course_info['LG'] = cour[1]['LG']
            
            this_semester.append(course_info)

        gradesheet.append(this_semester)        

    # for gs in gradesheet : print(gs, end="\n\n")
        
    return render(request, 'main/gradesheet_view.html', {'session':session, 'reg_no':reg_no, 'student_name':student_name, 'gradesheet':gradesheet})