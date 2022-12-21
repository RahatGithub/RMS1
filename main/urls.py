from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('semester_view/<str:batch_no>/<int:semester_no>', views.semester_view, name="semester_view"),
    path('students_view/<str:batch_no>', views.students_view, name="students_view")
]
