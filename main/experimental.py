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
                record_entry[course.course_code] = {'credits' : course.course_credits,
                                                    'GP' : course_result.GP, 
                                                    'LG' : course_result.LG}
            except:
                try:
                    course_result = SessionalCourseResult.objects.get(reg_no=student.reg_no, batch_no=batch_no, semester_no=semester_no, course_code=course.course_code)
                    record_entry[course.course_code] = {'credits' : course.course_credits,
                                                    'GP' : course_result.GP, 
                                                    'LG' : course_result.LG}
                except:
                    record_entry[course.course_code] = {'credits' : course.course_credits,
                                                    'GP' : None, 
                                                    'LG' : None}
            current_semester_credits += course.course_credits
            current_semester_total_GP += course.course_credits * float(course_result.GP) 
        
        current_semester_final_GPA =  round((current_semester_total_GP/current_semester_credits), 2) 
        record_entry[f"semester {semester_no}"] = {'total_credits' : current_semester_credits,
                                                   'final_GPA' : current_semester_final_GPA,
                                                   'final_LG' : 'X'}
        
        table_sheet.append(record_entry) 
    
        
    
    print("#"*150)
    # _________________________________________________________________________________