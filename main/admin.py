from django.contrib import admin
from .models import Batch, Semester, Course, Student, TheoryCourseResult, SessionalCourseResult


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("batch_no", "session")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("semester_no", "batch_no")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_code", "batch_no", "course_teacher", "course_type")
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("reg_no", "batch_no", "name")
    

@admin.register(TheoryCourseResult)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("reg_no", "course_code", "batch_no", "GP", "LG")
    
@admin.register(SessionalCourseResult)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("reg_no", "course_code", "batch_no", "GP", "LG")