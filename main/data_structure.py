# *****************final***************
assignment_results = [
    # ass 1:
    {   'total_marks' : 10, 
        'results' : [   
            ['2018331501', 'bustan', 8],  # student 1
            ['2018331502', 'shashi', 5],  # student 2
            ['2018331503', 'lukman', 10], # student 3
        ]    
    }
]

tt_results = [
    # tt 1:
    {   'total_marks' : 20, 
        'results' : [   
            ['2018331501', 'bustan', 12], # student 1
            ['2018331502', 'shashi', 17], # student 2
            ['2018331503', 'lukman', 11], # student 3
        ]    
    },
    # tt 2:
    {   'total_marks' : 20, 
        'results' : [   
            ['2018331501', 'bustan', 0],  # student 1
            ['2018331502', 'shashi', 18], # student 2
            ['2018331503', 'lukman', 15], # student 3 
        ]    
    }
]

attendance_results = [
    # class 1:
    {   'equal_to' : 1, 
        'attendance' : [   
            ['2018331501', 'bustan', 1], # student 1
            ['2018331502', 'shashi', 1], # student 2
            ['2018331503', 'lukman', 0], # student 3
        ]    
    },
     # class 2:
    {   'equal_to' : 2, 
        'attendance' : [   
            ['2018331501', 'bustan', 0], # student 1
            ['2018331502', 'shashi', 2], # student 2
            ['2018331503', 'lukman', 2], # student 3
        ]    
    },
]


# ***************not tested yet**************

full_batch_overall_tt_marks = [
    [ '2018331501', 'Abdullah Al Naseeh', [[14,20], [17,20]] ],
    [ '2018331502', 'Geerbani Shashi', [[18,20], [19,20]] ],
    [ '2018331503', 'Lukman Chowdhury', [[0,20], [11,20]] ]
]


full_batch_overall_assessment_marks = [
    [ '2018331501', 'Abdullah Al Naseeh', [14,8,7] ],  # [reg_no, name, [overall_tt_marks, overall_assignment_marks, overall_attendance_marks] ]
    [ '2018331502', 'Geerbani Shashi', [18,10,6] ],
    [ '2018331503', 'Lukman Chowdhury', [11,7,8] ] 
]


# students = Student.objects.filter(batch_no=batch_no)
# full_batch_overall_tt_marks = list()

# for i,student in enumerate(students):
#     a_std = list() 
#     a_std.append(student.reg_no)
#     a_std.append(student.name)
#     all_tt_marks = list()
#     for tt_res in tt_results:
#         obtained_marks = tt_res['results'][i][2]
#         total_marks = tt_res['total_marks']
#         all_tt_marks.append([obtained_marks, total_marks])
#     a_std.append(all_tt_marks)
#     full_batch_overall_tt_marks.append(a_std)



# def overall_assessment(request, batch_no, semester_no, course_code):
#     assessment = AssessmentResult.objects.get(batch_no=batch_no, semester_no=semester_no, course_code=course_code)
#     tt_results = json.loads(assessment.tt_results)
#     assignment_results = json.loads(assessment.assignment_results)
#     tt_mode = assessment.tt_mode 
#     tt_counting_on = assessment.tt_counting_on
#     assignment_counting_on = assessment.assignment_counting_on
#     students = Student.objects.filter(batch_no=batch_no)
    
#     full_batch_overall_assessment_marks = list()

    
#     for i,student in enumerate(students):
#         a_std = list() 
#         a_std.append(student.reg_no)
#         a_std.append(student.name)
#         all_tt_marks = list()
#         all_assignment_marks = list()

#         # calculating tt marks
#         for tt_res in tt_results:
#             obtained_marks = tt_res['results'][i][2]
#             total_marks = tt_res['total_marks']
#             all_tt_marks.append([obtained_marks, total_marks])
#         a_std_final_tt_marks = calculate_overall_marks(tt_mode, tt_counting_on, all_tt_marks)
#         a_std.append(a_std_final_tt_marks)

#         # calculating assignment marks
#         for ass_res in assignment_results:
#             obtained_marks = ass_res['results'][i][2]
#             total_marks = ass_res['total_marks']
#             all_assignment_marks.append([obtained_marks, total_marks])
#         a_std_final_assignment_marks = calculate_overall_marks("average", assignment_counting_on, all_assignment_marks)
#         a_std.append(a_std_final_assignment_marks)
    
#         # finally getting all records of tt and assignments
#         full_batch_overall_assessment_marks.append(a_std)



#     context = {
#         'batch_no' : batch_no,
#         'semester_no' : semester_no,
#         'course_code' : course_code,
#         'full_batch_overall_assessment_marks' : full_batch_overall_assessment_marks
#     }
    
#     return render(request, 'main/overall_assessment.html', context)
#     # return HttpResponse(full_batch_overall_assessment_marks)









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
        final_marks = ceil(total_marks/num)

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


# ans = calculate_overall_marks("best_one", 30, [[8,20], [12,20]]) 
# print(ans)


def calculate_attendance(counting_on, results):  # e.g. (10, [ [1,1],[0,2],[2,2],[1,1] ])
    total_classes = 0
    attended_classes = 0
    for result in results:
        total_classes += result[1]
        attended_classes += result[0]
    try:
        final_marks = ceil((attended_classes/total_classes)*counting_on)
    except: 
        final_marks = 0

    return final_marks


ans = calculate_attendance(10, [[1,1],[0,2],[2,2],[1,1]])
print(ans)