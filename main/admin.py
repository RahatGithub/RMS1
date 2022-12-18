from django.contrib import admin
from .models import Batch, Semester, Course, Student


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("batch_no", "session")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("semester_id", "semester_no")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_id", "course_code", "course_teacher")
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("reg_no", "batch_no", "name")