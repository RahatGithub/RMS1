    # ________________________________experimental___________________________________
    students = Student.objects.filter(batch_no=batch_no)
    print("*"*200)
    
    table_sheet = list()   # a list to store all result records for all students in this semester
    
    for student in students:
        result_entry = dict()   # a dictionary to store result record for each student in this semester
        reg_no = student.reg_no
        result_entry['reg_no'] = reg_no
        result_entry['name'] = student.name
        
        total_credits = 0
        total_GP = 0
        final_LG = None
        
        for course in courses:
            try: 
                course_result = TheoryCourseResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course.course_code, reg_no=reg_no)
            except:
                course_result = SessionalCourseResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course.course_code, reg_no=reg_no)
            
            result_entry[course.course_code] = {'credits' : course.course_credits,
                                                'GP' : course_result.GP, 
                                                'LG' : course_result.LG}
            total_credits += course.course_credits
            total_GP += course.course_credits * float(course_result.GP) 
        
        final_GPA =  round((total_GP/total_credits), 2) 
        result_entry[f"semester {semester_no}"] = {'total_credits' : total_credits,
                                                   'final_GPA' : final_GPA,
                                                   'final_LG' : 'X'}
        
        table_sheet.append(result_entry)
        
    # _____finally printing the output________
    for record in table_sheet:
        print(record)
    
        
    print("*"*200)
    # __________________________________________________________________________________