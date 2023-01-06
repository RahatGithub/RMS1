from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Batch, Semester, Course, Student, Teacher, TheoryCourseResult, SessionalCourseResult, Result
from main.pdf import generate_pdf
import json

# this is the dashboard
def dashboard(request):
    if request.method == "POST":  # when submitting the 'add batch' form
        if request.POST['form_name'] == 'add_batch_form':
            batch_no = request.POST['batch_no']
            session = request.POST['session']
            batch_id = batch_no + '_' + session
            batch = Batch.objects.create(batch_id=batch_id, batch_no=batch_no, session=session)
            batches = Batch.objects.all()   
            return render(request, 'index.html', {'batches' : batches, 'teachers' : teachers}) 
        elif request.POST['form_name'] == 'add_teacher_form':
            name = request.POST['name']
            designation = request.POST['designation']
            department = request.POST['department']
            institute = request.POST['institute']
            teacher = Teacher.objects.create(name=name, designation=designation, department=department, institute=institute)
            teachers = Teacher.objects.all()
            return render(request, 'index.html', {'batches' : batches, 'teachers' : teachers})
        elif request.POST['form_name'] == 'gradesheet_generator_form':
            reg_no = request.POST['reg_no']
            student = Student.objects.get(reg_no=reg_no)
            session = student.session 
            return generate_pdf(request, session, reg_no)
        
        
    teachers = Teacher.objects.all()
    batches_collection = Batch.objects.all()    
    batches = list()
    for batch in batches_collection:
        new_dict = dict()
        semester_list = Semester.objects.filter(batch_no=batch.batch_no)
        new_list = list()
        for semester in semester_list: 
            new_list.append(semester)
        new_dict['batch_id'] = batch.batch_id
        new_dict['batch_no'] = batch.batch_no
        new_dict['session'] = batch.session
        new_dict['semesters'] = new_list
        batches.append(new_dict)

    return render(request, 'index.html', {'batches' : batches, 'teachers' : teachers})
    
    


# main.pdf.generate_pdf() does the same thing and it opens as a pdf but here, the gradesheet_view opens the gradesheet as a webpage
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

    # for gs in gradesheet : print(gs, end="\n\n")
        
    return render(request, 'main/gradesheet_view.html', {'session':session, 'reg_no':reg_no, 'student_name':student_name, 'gradesheet':gradesheet})