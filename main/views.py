from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Batch, Semester, Course, Student, TheoryCourseResult, SessionalCourseResult, TableSheet
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
        
        table_sheet = TableSheet.objects.filter(batch_no=batch_no, semester_no=semester_no)
        
        return render(request, 'main/semester_view.html', {'batch_no':batch_no, 'semester_no':semester_no, 'courses':courses, 'table_sheet':table_sheet})
    
    # if not a POST request:
    courses = Course.objects.filter(batch_no=batch_no, semester_no=semester_no)
    
    students = Student.objects.filter(batch_no=batch_no)
    table_sheet_objects = TableSheet.objects.filter(batch_no=batch_no, semester_no=semester_no)
    
    table_sheet = list()
    for tb_sheet in table_sheet_objects:
        a_record = dict()
        a_record['reg_no'] = tb_sheet.reg_no
        student = Student.objects.filter(batch_no=batch_no, reg_no=tb_sheet.reg_no).first()
        a_record['name'] = student.name 
        a_record['batch_no'] = tb_sheet.batch_no
        a_record['semester_no'] = tb_sheet.semester_no
        a_record['course_results'] = json.loads(tb_sheet.course_results)
        a_record['current_semester_credits'] = tb_sheet.current_semester_credits
        a_record['current_semester_total_GP'] = tb_sheet.current_semester_total_GP
        a_record['overall_credits'] = tb_sheet.overall_credits
        a_record['overall_GP'] = tb_sheet.overall_GP
        
        table_sheet.append(a_record)
        
        print("*"*200)
        print(table_sheet[0]['course_results'])
        print("*"*200)
        # for course in courses: print(course.course_code)
        # print("*"*200)
    
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
        
        # try to get the TableSheet for this particular reg_no, then update this :
        try: 
            table_sheet_individual = TableSheet.objects.get(reg_no=reg_no, batch_no=batch_no, semester_no=semester_no)  
            course_results = json.loads(table_sheet_individual.course_results)
            course_results[course.course_code] = {'credits' : course.course_credits,
                                                  'GP' : GP,
                                                  'LG' : LG }
            table_sheet_individual.course_results = json.dumps(course_results)
            table_sheet_individual.current_semester_total_GP += float(GP)
            if float(GP) >= 2: 
                table_sheet_individual.current_semester_credits += course.course_credits
                table_sheet_individual.overall_credits += course.course_credits
                table_sheet_individual.overall_GP += float(GP)

            table_sheet_individual.save()
            
        # if there are no TableSheet found for this particular reg_no, then create one: 
        except:
            # *****Finding the result of this course and converting into JSON*****
            course_results = dict()
            course_results[course.course_code] = {'credits' : course.course_credits,
                                                  'GP' : GP,
                                                  'LG' : LG }
            course_results_json = json.dumps(course_results)  # converting the dict to str(JSON)
            # ********************************************************************
            
            # *******************Finding current semester credits*****************
            current_semester_total_GP = float(GP)
            if float(GP) >= 2: 
                current_semester_credits = course.course_credits
            else : current_semester_credits = 0
            # ********************************************************************
            
            # ********Finding overall credits (all semesters till now)************
            overall_credits = current_semester_credits 
            overall_GP = current_semester_total_GP 
            if semester_no > 1:
                prev_table_sheet = TableSheet.objects.get(reg_no=reg_no, batch_no=batch_no, semester_no=semester_no-1)
                overall_credits = prev_table_sheet.overall_credits + current_semester_credits
                overall_GP = prev_table_sheet.overall_GP + current_semester_total_GP 
            # ********************************************************************
            
            table_sheet_individual = TableSheet.objects.create(reg_no=reg_no, 
                                                               batch_no=batch_no, 
                                                               semester_no=semester_no,
                                                               course_results=course_results_json,
                                                               current_semester_credits=current_semester_credits,
                                                               current_semester_total_GP=current_semester_total_GP,
                                                               overall_credits=overall_credits,
                                                               overall_GP=overall_GP )
        
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