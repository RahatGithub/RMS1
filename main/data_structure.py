# tt_results = [
#         [ '2018331501', 'Abdullah Al Naseeh', [[12,20], [15,20]] ],  # student 1 -> [obtained_marks, total_marks]
#         [ '2018331502', 'Geerbani Shashi', [[10,20], [0,20]] ],  # student 2 -> [obtained_marks, total_marks]
#         [ '2018331503', 'Lukman Chowdhury', [[0,20], [18,20]] ],  # student 3 -> [obtained_marks, total_marks]
# ]


assignment_results = [
        [ '2018331501', 'Abdullah Al Naseeh', [[8,10]] ],  # student 1 -> [obtained_marks, total_marks]
        [ '2018331502', 'Geerbani Shashi', [[0,10]] ],  # student 2 -> [obtained_marks, total_marks]
        [ '2018331503', 'Lukman Chowdhury', [[9,10]] ],  # student 3 -> [obtained_marks, total_marks]
]


attendance_results = [
        [ '2018331501', 'Abdullah Al Naseeh', 7 ],  # student 1 -> attended class
        [ '2018331502', 'Geerbani Shashi', 6 ],  # student 2 -> attended class
        [ '2018331503', 'Lukman Chowdhury', 8 ],  # student 3 -> attended class
]







tt_results = [
    # tt 1:
    {   'total_marks' : 20, 
        'results' : [   
            ['2018331501', 12], # student 1
            ['2018331502', 17], # student 2
            ['2018331503', 11], # student 3
        ]    
    },
    # tt 2:
    {   'total_marks' : 20, 
        'results' : [   
            ['2018331501', 0],  # student 1
            ['2018331502', 18], # student 2
            ['2018331503', 15], # student 3 
        ]    
    }
]


assignment_results = [
    # ass 1:
    {   'total_marks' : 10, 
        'results' : [   
            ['2018331501', 8],  # student 1
            ['2018331502', 5],  # student 2
            ['2018331503', 10], # student 3
        ]    
    }
]

# *********Model**********
# AssessmentResult:
# 	id 
# 	batch_no
# 	semester_no
# 	course_code
# 	tt_mode
# 	tt_counting_on
# 	tt_results
# 	assignment_counting_on
# 	assignment_results
# 	attendance_counting_on
# 	total_classess
# 	attended_classes
# 	total_assessment_marks	
