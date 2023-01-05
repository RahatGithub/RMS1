from django.urls import path
from . import views
from .pdf import generate_pdf

urlpatterns = [
    path('', views.index, name="index"),
    path('semester_view/<str:batch_no>/<int:semester_no>', views.semester_view, name="semester_view"),
    path('students_view/<str:batch_no>', views.students_view, name="students_view"),
    path('add_semester/<str:batch_no>', views.add_semester, name="add_semester"),
    path('course_view/<str:batch_no>/<int:semester_no>/<str:course_type>/<str:course_code>', views.course_view, name="course_view"),
    path('gradesheet_view/<str:session>/<str:reg_no>', generate_pdf, name="generate_pdf"),
    path('search', views.search, name="search")
    # path('table_sheet_pdf/<str:session>/<str:reg_no>/', generate_pdf, name="generate_pdf")
]
