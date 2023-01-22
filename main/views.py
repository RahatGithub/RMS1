from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Batch, Semester, Course, Student, TheoryCourseResult, SessionalCourseResult, Result, AssessmentResult
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
    cumulative_credits, cumulative_point, cumulative_LG = float(0), float(0), 'NA'   # for the overall result of all semesters
    for result in semester_results:
        a_semester = dict()
        course_results = json.loads(result.course_results)
        course_results_info = list()
        this_semester_credits, this_semester_point, this_semester_LG = float(0), float(0), 'NA'   # for only a particular semester
        for cour in course_results.items():
            course_info = list()
            course_info.append(cour[0])     # pushing the course_code at index=0
            course = Course.objects.filter(batch_no=batch_no, course_code=cour[0]).first() 
            course_info.append(course.course_title)    # pushing the course_title at index=1
            course_info.append(course.course_credits)  # pushing the course_credits at index=2
            course_info.append(cour[1]['GP'])      # pushing the obtained GP at index=3
            course_info.append(cour[1]['LG'])      # pushing the obtained LG at index=4
            if float(course_info[3]) >= 2:            # checking if the obtained GP >= 2 
                this_semester_credits += course_info[2]  # cumulative_credits += course_credits
                this_semester_point += float(course_info[3]) * course_info[2]  # cumulative_point += GP * course_credits
            course_results_info.append(course_info)
        
        a_semester['this_semester_credits'] = this_semester_credits
        a_semester['course_results_info'] = course_results_info
            
        this_semester_GP = round((this_semester_point/this_semester_credits), 2)
        a_semester['this_semester_GP'] = this_semester_GP
            
        if this_semester_GP == 4.00 : this_semester_LG = "A+"
        elif this_semester_GP >= 3.75 : this_semester_LG = "A"
        elif this_semester_GP >= 3.50 : this_semester_LG = "A-" 
        elif this_semester_GP >= 3.25 : this_semester_LG = "B+"
        elif this_semester_GP >= 3.00 : this_semester_LG = "B"
        elif this_semester_GP >= 2.75 : this_semester_LG = "B-"
        elif this_semester_GP >= 2.50 : this_semester_LG = "C+"
        elif this_semester_GP >= 2.25 : this_semester_LG = "C"
        elif this_semester_GP >= 2.00 : this_semester_LG = "C-" 
        else: this_semester_LG = "F"
        a_semester['this_semester_LG'] = this_semester_LG

        cumulative_credits += this_semester_credits
        a_semester['cumulative_credits'] = cumulative_credits
        cumulative_point += this_semester_point
        cumulative_GP = round((cumulative_point/cumulative_credits), 2)
        a_semester['cumulative_GP'] = cumulative_GP
        
        if cumulative_GP == 4.00 : cumulative_LG = "A+"
        elif cumulative_GP >= 3.75 : cumulative_LG = "A"
        elif cumulative_GP >= 3.50 : cumulative_LG = "A-" 
        elif cumulative_GP >= 3.25 : cumulative_LG = "B+"
        elif cumulative_GP >= 3.00 : cumulative_LG = "B"
        elif cumulative_GP >= 2.75 : cumulative_LG = "B-"
        elif cumulative_GP >= 2.50 : cumulative_LG = "C+"
        elif cumulative_GP >= 2.25 : cumulative_LG = "C"
        elif cumulative_GP >= 2.00 : cumulative_LG = "C-" 
        else: cumulative_LG = "F"
        a_semester['cumulative_LG'] = cumulative_LG
        
        
        gradesheet.append(a_semester)      

    for gs in gradesheet : print(gs, end="\n\n")
        
    return render(request, 'main/gradesheet_view.html', {'session':session, 'reg_no':reg_no, 'student_name':student_name, 'gradesheet':gradesheet})




# ************ EVERYTHING BELOW IS EXPERIMENTAL *************




def assessments(request, batch_no, semester_no, course_code):
    students = Student.objects.filter(batch_no=batch_no)

    if request.method == "POST":
        if request.POST['form_name'] == 'add_tt_form':
            total_marks = int(request.POST['total_marks'])
            try: # if there is already an instance of AssessmentResult for this course
                assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
                tt_results = json.loads(assessment.tt_results)
                a_tt = dict()
                a_tt['total_marks'] = total_marks
                a_tt['results'] = list()
                tt_results.append(a_tt)
                tt_results_json = json.dumps(tt_results)
                assessment.tt_results = tt_results_json
                assessment.save() 
                assignment_results = json.loads(assessment.assignment_results)
                tt_counting_on = assessment.tt_counting_on
                assignment_counting_on = assessment.assignment_counting_on
            except: # if there is no instance of AssessmentResult for this course
                tt_results = list()
                a_tt = dict()
                a_tt['total_marks'] = total_marks
                a_tt['results'] = list()
                tt_results.append(a_tt)
                tt_results_json = json.dumps(tt_results)
                tt_counting_on = 20
                assignment_results = list()
                assignment_counting_on = 10
                AssessmentResult.objects.create(
                    batch_no = batch_no,
                    semester_no = semester_no,
                    course_code = course_code,
                    tt_mode = "normal",
                    tt_counting_on = tt_counting_on,
                    tt_results = tt_results_json,
                    assignment_counting_on = assignment_counting_on,
                    assignment_results = "[]"
                )

            context = {
                'batch_no' : batch_no,
                'semester_no' : semester_no,
                'course_code' : course_code,
                'students' : students,
                'tt_results' : tt_results,
                'tt_mode' : "normal",
                'tt_counting_on' : tt_counting_on,
                'assignment_results' : assignment_results, 
                'assignment_counting_on' : assignment_counting_on
            }
            return render(request, 'main/assessment.html', context)

        elif request.POST['form_name'] == 'add_assignment_form':
            total_marks = int(request.POST['total_marks'])
            try: # if there is already an instance of AssessmentResult for this course
                assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
                assignment_results = json.loads(assessment.assignment_results)
                a_assignment = dict()
                a_assignment['total_marks'] = total_marks
                a_assignment['results'] = list()
                assignment_results.append(a_assignment)
                assignment_results_json = json.dumps(assignment_results)
                assessment.assignment_results = assignment_results_json
                assessment.save() 
                tt_results = json.loads(assessment.tt_results)
                tt_mode = assessment.tt_mode
                tt_counting_on = assessment.tt_counting_on
                assignment_counting_on = assessment.assignment_counting_on
            except: # if there is no instance of AssessmentResult for this course
                assignment_results = list()
                a_assignment = dict()
                a_assignment['total_marks'] = total_marks
                a_assignment['results'] = list()
                assignment_results.append(a_assignment)
                assignment_results_json = json.dumps(assignment_results)
                tt_results = list()
                tt_counting_on = 20 
                assignment_counting_on = 10
                tt_mode = "normal"
                AssessmentResult.objects.create(
                    batch_no = batch_no,
                    semester_no = semester_no,
                    course_code = course_code,
                    tt_mode = tt_mode,
                    tt_counting_on = tt_counting_on,
                    tt_results = "[]",
                    assignment_results = assignment_results_json,
                    assignment_counting_on = assignment_counting_on
                )

            context = {
                'batch_no' : batch_no,
                'semester_no' : semester_no,
                'course_code' : course_code,
                'students' : students,
                'tt_results' : tt_results,
                'tt_mode' : tt_mode,
                'tt_counting_on' : tt_counting_on,
                'assignment_results' : assignment_results,
                'assignment_counting_on' : assignment_counting_on
            }
            return render(request, 'main/assessment.html', context)

        elif request.POST['form_name'] == 'add_tt_marks_form':
            tt_no = int(request.POST['tt_no'])
            reg_no = request.POST['reg_no']
            student = Student.objects.get(reg_no=reg_no)
            name = student.name 
            obtained_marks = int(request.POST['obtained_marks'])
            assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
            tt_results = json.loads(assessment.tt_results)            
            a_record = [reg_no, name, obtained_marks]
            tt_results[tt_no-1]['results'].append(a_record)
            tt_results_json = json.dumps(tt_results)
            assessment.tt_results = tt_results_json
            assessment.save()
            assignment_results = json.loads(assessment.assignment_results)
            tt_mode = assessment.tt_mode
            tt_counting_on = assessment.tt_counting_on
            assignment_counting_on = assessment.assignment_counting_on

            context = {
                'batch_no' : batch_no,
                'semester_no' : semester_no,
                'course_code' : course_code,
                'students' : students,
                'tt_results' : tt_results,
                'tt_mode' : tt_mode,
                'tt_counting_on' : tt_counting_on,
                'assignment_results' : assignment_results,
                'assignment_counting_on' : assignment_counting_on
            }
            return render(request, 'main/assessment.html', context)
        
        elif request.POST['form_name'] == 'add_assignment_marks_form':
            assignment_no = int(request.POST['assignment_no'])
            reg_no = request.POST['reg_no']
            student = Student.objects.get(reg_no=reg_no)
            name = student.name 
            obtained_marks = int(request.POST['obtained_marks'])
            assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
            assignment_results = json.loads(assessment.assignment_results)            
            a_record = [reg_no, name, obtained_marks]
            assignment_results[assignment_no-1]['results'].append(a_record)
            assignment_results_json = json.dumps(assignment_results)
            assessment.assignment_results = assignment_results_json
            assessment.save()
            tt_results = json.loads(assessment.tt_results)
            tt_mode = assessment.tt_mode
            tt_counting_on = assessment.tt_counting_on
            assignment_counting_on = assessment.assignment_counting_on

            context = {
                'batch_no' : batch_no,
                'semester_no' : semester_no,
                'course_code' : course_code,
                'students' : students,
                'tt_results' : tt_results,
                'tt_mode' : tt_mode,
                'tt_counting_on' : tt_counting_on,
                'assignment_results' : assignment_results,
                'assignment_counting_on' : assignment_counting_on
            }
            return render(request, 'main/assessment.html', context)
        
        elif request.POST['form_name'] == 'tt_info_submit_form':
            tt_mode = request.POST['tt_mode']
            tt_counting_on = int(request.POST['counting_on'])
            try:
                assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
                assessment.tt_mode = tt_mode 
                assessment.tt_counting_on = tt_counting_on
                assessment.save() 
                tt_results = json.loads(assessment.tt_results)
                assignment_results = json.loads(assessment.assignment_results) 
                assignment_counting_on = assessment.assignment_counting_on
            except:
                tt_results, assignment_results = [], []
                assignment_counting_on = 10
                AssessmentResult.objects.create(
                    batch_no = batch_no,
                    semester_no = semester_no, 
                    course_code = course_code, 
                    tt_mode = tt_mode, 
                    tt_counting_on = tt_counting_on, 
                    tt_results = "[]",
                    assignment_counting_on = assignment_counting_on,
                    assignment_results = "[]"
                )
            context = {
                'batch_no' : batch_no,
                'semester_no' : semester_no,
                'course_code' : course_code,
                'students' : students,
                'tt_results' : tt_results,
                'tt_mode' : tt_mode, 
                'tt_counting_on' : tt_counting_on, 
                'assignment_results' : assignment_results,
                'assignment_counting_on' : assignment_counting_on
            }
            return render(request, 'main/assessment.html', context) 
        
        elif request.POST['form_name'] == 'assignment_info_submit_form':
            assignment_counting_on = int(request.POST['counting_on'])
            try:
                assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
                assessment.assignment_counting_on = assignment_counting_on
                assessment.save() 
                tt_results = json.loads(assessment.tt_results)
                assignment_results = json.loads(assessment.assignment_results) 
                tt_counting_on = assessment.tt_counting_on
                tt_mode = assessment.tt_mode
            except:
                tt_results, assignment_results = [], []
                tt_mode = "normal"
                tt_counting_on = 20
                AssessmentResult.objects.create(
                    batch_no = batch_no,
                    semester_no = semester_no, 
                    course_code = course_code, 
                    tt_mode = tt_mode, 
                    tt_counting_on = tt_counting_on, 
                    tt_results = "[]",
                    assignment_counting_on = 10,
                    assignment_results = "[]"
                )
            context = {
                'batch_no' : batch_no,
                'semester_no' : semester_no,
                'course_code' : course_code,
                'students' : students,
                'tt_results' : tt_results,
                'tt_mode' : tt_mode,
                'tt_counting_on' : tt_counting_on, 
                'assignment_results' : assignment_results,
                'assignment_counting_on' : assignment_counting_on

            }
            return render(request, 'main/assessment.html', context)


    # if it is a GET request:
    try:
        assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
        # for term tests:
        tt_results = json.loads(assessment.tt_results)
        tt_mode = assessment.tt_mode
        tt_counting_on = assessment.tt_counting_on
        # for assignments:
        assignment_results = json.loads(assessment.assignment_results)
        assignment_counting_on = assessment.assignment_counting_on
    except:
        tt_results = list()
        assignment_results = list()
        tt_mode = "normal"
        tt_counting_on = 20
        assignment_counting_on = 10

    context = {
        'batch_no' : batch_no,
        'semester_no' : semester_no,
        'course_code' : course_code,
        'students' : students,
        'tt_results' : tt_results,
        'tt_mode' : tt_mode,
        'tt_counting_on' : tt_counting_on,
        'assignment_results' : assignment_results,
        'assignment_counting_on' : assignment_counting_on
    }

    return render(request, 'main/assessment.html', context)



def overall_assessment(request, batch_no, semester_no, course_code):
    assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
    tt_results = json.loads(assessment.tt_results)
    assignment_results = json.loads(assessment.assignment_results)
    tt_mode = assessment.tt_mode 
    tt_counting_on = assessment.tt_counting_on
    assignment_counting_on = assessment.assignment_counting_on
    students = Student.objects.filter(batch_no=batch_no)
    
    full_batch_overall_assessment_marks = list()

    
    for i,student in enumerate(students):
        a_std = list() 
        a_std.append(student.reg_no)
        a_std.append(student.name)
        all_tt_marks = list()
        all_assignment_marks = list()

        # calculating tt marks
        for tt_res in tt_results:
            obtained_marks = tt_res['results'][i][2]
            total_marks = tt_res['total_marks']
            all_tt_marks.append([obtained_marks, total_marks])
        a_std_final_tt_marks = calculate_overall_marks(tt_mode, tt_counting_on, all_tt_marks)
        a_std.append(a_std_final_tt_marks)

        # calculating assignment marks
        for ass_res in assignment_results:
            obtained_marks = ass_res['results'][i][2]
            total_marks = ass_res['total_marks']
            all_assignment_marks.append([obtained_marks, total_marks])
        a_std_final_assignment_marks = calculate_overall_marks("average", assignment_counting_on, all_assignment_marks)
        a_std.append(a_std_final_assignment_marks)
    
        # finally getting all records of tt and assignments
        full_batch_overall_assessment_marks.append(a_std)



    context = {
        'batch_no' : batch_no,
        'semester_no' : semester_no,
        'course_code' : course_code,
        'full_batch_overall_assessment_marks' : full_batch_overall_assessment_marks
    }
    
    return render(request, 'main/overall_assessment.html', context)
    # return HttpResponse(full_batch_overall_assessment_marks)
    




from math import ceil

def calculate_overall_marks(mode, counting_on, results):  # e.g. ("normal", 20, [[8,10], [9,10]])
    final_marks = 0
    if mode == "normal":
        for result in results:
            final_marks += result[0]

    elif mode == "average":
        num = len(results) 
        total_marks = 0
        for result in results:
            total_marks += int((counting_on/result[1])*result[0])
        try:
            final_marks = ceil(total_marks/num)
        except:
            final_marks = 0

    elif mode == "best_one":
        marks = [] 
        for result in results:
            marks.append(int((counting_on/result[1])*result[0]))
        final_marks = max(marks)

    elif mode == "best_two":
        marks = [] 
        for result in results:
            marks.append(int((counting_on/result[1])*result[0])) 
        best = marks.pop(marks.index(max(marks))) // int(counting_on/result[1])
        second_best = marks.pop(marks.index(max(marks))) // int(counting_on/result[1])
        final_marks = (best + second_best) // 2

    return final_marks
