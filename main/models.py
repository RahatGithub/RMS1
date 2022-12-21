from django.db import models


class Batch(models.Model):
    id = models.AutoField
    batch_id = models.CharField(max_length=18, default="") # It shall be removed later, all the work will be modified accrodingly 
    batch_no = models.CharField(max_length=6, default="")               
    session = models.CharField(max_length=8, default="")                
    

class Semester(models.Model):
    id = models.AutoField 
    batch_no = models.CharField(max_length=8, default="")
    semester_no = models.IntegerField(default=None)
    courses_json = models.CharField(max_length=5000, default="")

   
class Course(models.Model):
    id = models.AutoField
    # course_id = models.CharField(max_length=20, default="")
    batch_no = models.CharField(max_length=8, default="")
    semester_no = models.IntegerField(default=None)
    course_code = models.CharField(max_length=8, default="")
    course_title = models.CharField(max_length=60, default="")
    course_type =  models.CharField(max_length=10, default="")
    course_credits = models.FloatField(default=0) 
    course_teacher = models.CharField(max_length=40, default="") 
    # course_results_json = models.CharField(max_length=5000, default="")  # e.g. {'2018331500' : {'GP':'3.75', 'LG':'A'}} 


class Student(models.Model):
    id = models.AutoField 
    reg_no = models.CharField(max_length=10, default="")
    batch_no = models.CharField(max_length=6, default="")
    session = models.CharField(max_length=8, default="")   
    name = models.CharField(max_length=60, default="")
    father_name = models.CharField(max_length=60, default="")
    mother_name = models.CharField(max_length=60, default="")
    address = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=11, default="")
    isResidential = models.BooleanField(default=False)
    isCR = models.BooleanField(default=False) 
    average_cgpa = models.FloatField(default=0)
    remarks = models.CharField(max_length=500, default="")