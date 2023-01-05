from io import BytesIO
from django.shortcuts import render 
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 
from .models import Batch, Student, Result, Course
import json

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO() 
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def generate_pdf(request, session, reg_no):
    # table_sheet = TableSheet.objects.filter(session=session, reg_no=reg_no).first()
    # context = {'table_sheet' : table_sheet}
    
    # pdf = render_to_pdf('main/gradesheet_view.html', context)
    
    # if pdf:
    #     response = HttpResponse(pdf, content_type="application/pdf")
    #     content = "inline; filename=TableSheet.pdf"
    #     response['Content-Disposition'] = content 
    #     return response 
    # return HttpResponse("Not found")
    
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
        
    context = {'gradesheet' : gradesheet, 
               'session' : session,
               'reg_no' : reg_no,
               'student_name' : student_name}
    pdf = render_to_pdf('main/gradesheet_view.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        content = "inline; filename=GradeSheet.pdf"
        response['Content-Disposition'] = content 
        return response 
    return HttpResponse("Not found")