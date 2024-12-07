from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import APIView
from .models import Teacher, Student, Course
from .serializers import TeacherSerializer, StudentSerializer ,CourseSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from django.db.models import Q , Max, Sum, Count, Case ,When, Value, CharField
from django.db.models import OuterRef,Subquery,Exists
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.db import connection




class TeacherAPIView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class GetStudentsEnroledInCourse(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'course_id'

    def get(self, request, *args, **kwargs):
            try:
                course = self.get_object() 
            except Course.DoesNotExist:
                raise NotFound(detail=f'No course with the id {kwargs["course_id"]} found.')
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)


# querying the data


# filter the courses according to the duration and the charge
class CourseQueryAPI(generics.GenericAPIView,mixins.ListModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        # Get query parameters
        charge = self.request.query_params.get('charge')
        duration = self.request.query_params.get('duration')
        # if one of the paramaters are missing throw errors
        if charge is None or duration is None:
            missing_params = []
            if charge is None:
                missing_params.append("Charge paramater is not provided.")
            if duration is None:
                missing_params.append("Douration is not provided.")
            raise ValidationError({'detail':f'{" ".join(missing_params)}'})

        queryset = super().get_queryset()
        # filter the courses 
        queryset = Course.objects.filter(duration__lte=duration, charge__lte=charge)
        # return the queryset
        return queryset

    def get(self,request,*args,**kwargs):
        courses = self.get_queryset()
        # if there are no courses we responde with an empty list and a 204 no content
        if not  courses.exists():
            return Response([],status=status.HTTP_204_NO_CONTENT)
            # we serialize the data before we send it to the client
        serializer = self.serializer_class(courses,many=True)
            # sending the serialized data to the client alongside a 200 ok message
        return Response(serializer.data,status=status.HTTP_200_OK)



# count how many teachers are traching in a course
class TeachersInASingleCourse(APIView):
    def get(self, request, *args, **kwargs):
        # Get the course_id from request data (body)
        course_id = request.data.get('course_id')
        # if course_id is not provided throw error 400 bad request
        if not course_id:
            return Response({'error': 'No course_id provided in the body'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve the course using the provided course_id
            course = Course.objects.get(course_id=course_id)
            # count the teachers
            number_of_teachers = course.teachers.count()
            # from the course extract the teachers
            teachers = course.teachers.all()
            # create a list with the teachers
            teachers_list = []
            # loop and append each teacher to the list
            for teacher in teachers:
                teachers_list.append(teacher.name)

            data = {
             'number_of_teachers':number_of_teachers,
             'name_of_teachers': ", ".join(teachers_list)
                    }
        except Course.DoesNotExist:
            raise NotFound(detail=f'No course with the id {course_id} found.')
            # send the data and a 200 ok status
        return Response(data,status=status.HTTP_200_OK)
      

        




# filter courses according to the charge and the starting teaching year
class CourseSearch(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        # get the charge and years query paramaters
        charge = self.request.query_params.get('charge')
        beginning_teaching_param = self.request.query_params.get('beginning_teaching')
        # if the paramaters are not provided throw an error
        if charge is None or beginning_teaching_param is None:
            errors = []
            if charge is None :
                errors.append('Charge paramater not provided')
            if  beginning_teaching_param is None:
                errors.append('Year of teaching not provided')
            raise ValidationError({"error":', '.join(errors)})
        # validate the charge
        try:
            charge = Decimal(charge)
        except InvalidOperation:
            raise ValidationError({'charge': 'Charge must be a valid decimal number.'})
        # validate the year of teaching
        try:
            beginning_teaching_param = datetime.strptime(beginning_teaching_param, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError({'beginning_teaching': 'Beginning teaching must be a valid date in YYYY-MM-DD format.'})

        queryset= super().get_queryset()
        # filter the courses according to the charge and the year of beginning teaching
        queryset = queryset.filter(
            Q(charge__lte=charge) & 
            Q(teachers__beginning_teaching__gte=beginning_teaching_param)
        # teachers filed is a many to many field in the course model
        ).distinct()
        return queryset






# filter coruses according to charge and teachers years of experience
class CourseSearchYearsOfExperience(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        # get the charge and years query paramaters
        charge = self.request.query_params.get('charge')
        years_of_experience = self.request.query_params.get('years_of_experience')
        # if the paramaters are not provided throw an error
        if charge is None or years_of_experience is None:
            errors = []
            if charge is None :
                errors.append('Charge paramater not provided')
            if  years_of_experience is None:
                errors.append('Years of experience not provided')
            raise ValidationError({"error":', '.join(errors)})

        # validate the charge
        try:
            charge = Decimal(charge)
        except InvalidOperation:
            raise ValidationError({'charge': 'Charge must be a valid decimal number.'})
        
        # validate years_of_experience
        try:
            years_of_experience = int(years_of_experience)
            if years_of_experience < 0:
                raise ValidationError({'years_of_experience': 'Years of experience must be a positive number.'})
        except ValueError:
            raise ValidationError({'years_of_experience': 'Years of experience must be a valid integer.'})

        queryset= super().get_queryset()
        # filter accoring to the charge and teacher's years of experience
        queryset = queryset.filter(
            Q(charge__lte=charge)&
            Q(teachers__years_of_experience__gte=years_of_experience))  

        return queryset



# get the most expensive course
class MostExpensiveCourseAPI(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        # max_charge returns a the aggregation of the queryset
        # the maximum value of the charge field in the model
        max_charge = self.queryset.aggregate(max_price=Max('charge'))['max_price']
        # the max_course filters for the most expensive course
        max_course = self.queryset.filter(charge=max_charge)
        return max_course


    def get(self,request,*args,**kwargs):
        courses = self.get_queryset()
        serializer = self.serializer_class(courses,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

 




# count total number of students in all courses
class TotalStudentsAPI(viewsets.GenericViewSet):
    queryset = Course.objects.all() 
    serializer_class = CourseSerializer
    def list(self,request):
        # using the aggreagate methong and Count method we count all the students fields
        students = self.queryset.aggregate(total_students=Count('students'))['total_students']
        # we send a response as a dictionary
        return Response({'total number of students':students},status=status.HTTP_200_OK)


# count how many students are in each course
class StudentsPerCourseAPI(viewsets.GenericViewSet):
    queryset = Course.objects.all() 
    serializer_class = CourseSerializer
    def list(self,request):
        # we annotate each model instance with the filed students_per_course
        students_enroled = self.queryset.annotate(students_per_course=Count('students'))
        # we create a data dictionary and we loop through the each model instance
        # and we access the student_per_course annotated field
        data = {
            f"course_id: {str(student.course_id)}":f"number_of_students: {student.students_per_course}"
            for student in students_enroled
                }
        # we send the data as a dictionary
        return Response(data,status=status.HTTP_200_OK)




#  lets see all the courses that teach Math ,Chemistry and so on 

class FilterBySubject(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self,request,*args,**kwargs):
        subject_1 = Q(teachers__teaching_subject_1__icontains='history')
        courses = self.queryset.filter(subject_1)
        data = {
            f"{course.course_id}": {'teacher teaching_subject_1':
             [teacher.teaching_subject_1 for teacher in course.teachers.all()]}
            for course in courses
        }

        return Response([data],status=status.HTTP_200_OK)
        
 



# learning how to use conditional expression 
class AnnotatingStudents(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
            subjects = Student.objects.annotate(
                duration_description=Case(
                    When(Q(age__lte=20), then=Value('very young')),
                    When(Q(age__gte=21) & Q(age__lt=40), then=Value('young')),
                    When(age__gt=41, then=Value('old')),
                    default=Value('this is the default'),
                    output_field=CharField(),
                )
            )
            etichets = [{subject.duration_description:subject.age} for subject in subjects]
           
            return Response(etichets, status=status.HTTP_200_OK)


# learning Subquery, outerRef 
class QueryStudentsAPI(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        # Wrap the query in Subquery
        students = Subquery(
            Course.objects.filter(teachers=OuterRef('pk'))
            .order_by('-date_time_scheduled')  
            .values('students__name')[:1]   
        )

        # Annotate teachers with the subquery
        teachers = Teacher.objects.annotate(most_recent_student=students)

        data = [{
                'teacher_name': teacher.name,
                'most_recent_student': teacher.most_recent_student
            }
            for teacher in teachers
            ]

        print(connection.queries)
        print(students)
        return Response(data,status=status.HTTP_200_OK)
    

# check to see if a student in enrolled in a course
class StudentsEnroledAPI(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        courses = Course.objects.filter(students=OuterRef('pk'))
        is_enrolled = Student.objects.annotate(is_enrol=Exists(courses))

        data = [
            {f'Student name - {student.name}': f"Enroled - {student.is_enrol}"}
            for student in is_enrolled
            ]
  
        return Response(data,status=status.HTTP_200_OK)