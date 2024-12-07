from django.urls import path
from . import views


urlpatterns = [
    path('teacher',views.TeacherAPIView.as_view(),name='teacher'),
    path('student',views.StudentAPIView.as_view(),name='student'),
    path('course',views.CourseAPIView.as_view(),name='course'),
    path('one_course/<uuid:course_id>',views.GetStudentsEnroledInCourse.as_view(),name='get_students'),
    path('course_query',views.CourseQueryAPI.as_view(),name='course_query'),
    path('number_of_teachers',views.TeachersInASingleCourse.as_view(),name='number_of_teachers'),
    path('course_search',views.CourseSearch.as_view(),name='course_search'),
    path('years_experience',views.CourseSearchYearsOfExperience.as_view(),name='experience'),
    path('most_expensive',views.MostExpensiveCourseAPI.as_view(),name='most_expensive'),
    path('total_students',views.TotalStudentsAPI.as_view({'get':'list'}),name='total_students'),
    path('students_per_course',views.StudentsPerCourseAPI.as_view({'get':'list'}),name='students_per_course'),
    path('filter_by_subject',views.FilterBySubject.as_view({'get':'list'}),name='filter_by_subject'),
    path('annotate_students',views.AnnotatingStudents.as_view({'get':'list'}),name='annotate_students'),
    path('query_students',views.QueryStudentsAPI.as_view({'get':'list'}),name='query'),
    path('students_enrolled',views.StudentsEnroledAPI.as_view({'get':'list'}),name='students_enrolled')
    ]
