from django.db import models
import uuid 
from datetime import date
from django.core.validators import MinValueValidator

class Subjects(models.TextChoices):
    ENGLISH =  'English'
    MATHEMATICS =  'Mathematics'
    PHYSICS =  'Physics'
    GEOGRAPHY =  'Geography'
    FRENCH =  'French'
    CHEMISTRY =  'Chemistry'
    HISTORY =  'History'


# creating the teacher model
class Teacher(models.Model):
    teacher_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    name = models.TextField(max_length=40,null=False)
    beginning_teaching = models.DateField(null=False)
    teaching_subject_1 = models.CharField(max_length=100,default='')
    teaching_subject_2 = models.CharField(max_length=100,default='')
    teaching_subject_3 = models.CharField(max_length=100,default='')
    # beginning_teaching = models.DateField(null=False)
    # years_of_experience = models.PositiveIntegerField(default=0)  # Store years of experience in the DB
    @property
    def years_of_experience(self):
        today = date.today()
        delta = today - self.beginning_teaching
        return delta.days // 365 
    def __str__(self):
        return self.name
    # def save(self, *args, **kwargs):
    #     # Recalculate the years_of_experience whenever the model is saved
    #     today = date.today()
    #     delta = today - self.beginning_teaching
    #     self.years_of_experience = delta.days // 365  # Store the years of experience in the DB

    #     super().save(*args, **kwargs)


# creating the student model
class Student(models.Model):
    student_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=40,null=False)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18)])
    interested_in = models.CharField(max_length=100,blank=False)
    email = models.EmailField(blank=False)


# creating the coruse model
class Course(models.Model):
    course_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    date_time_scheduled = models.DateTimeField(null=False)
    duration = models.TimeField(null=False)
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)
    charge = models.DecimalField(max_digits=5,decimal_places=2,default=0)