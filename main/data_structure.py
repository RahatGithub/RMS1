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


# ***************not tested yet**************

full_batch_overall_tt_marks = [
    [ '2018331501', 'Abdullah Al Naseeh', [[14,20], [17,20]] ],
    [ '2018331502', 'Geerbani Shashi', [[18,20], [19,20]] ],
    [ '2018331503', 'Lukman Chowdhury', [[0,20], [11,20]] ]
]


full_batch_overall_assessment_marks = [
    [ '2018331501', 'Abdullah Al Naseeh', [14,8] ],
    [ '2018331502', 'Geerbani Shashi', [18,10] ],
    [ '2018331503', 'Lukman Chowdhury', [11,7] ] 
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


ans = calculate_overall_marks("best_one", 30, [[8,20], [12,20]]) 
print(ans)