from django.db import models

class Student(models.Model):
    StudentID = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    description = models.CharField(max_length=5000)

    def __str__(self):
        return self.name
    
class Tutor(models.Model):
    TutorID = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    description = models.CharField(max_length=5000)
    subjects = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    BookingID = models.CharField(max_length=8, unique=True)
    date = models.DateField()
    numOfStudents = models.IntegerField()
    description = models.CharField(max_length=1000)
    subjects = models.CharField(max_length=300)

    def __str__(self):
        return self.BookingID
    
class Review(models.Model):
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    ReviewID = models.CharField(max_length=8, unique=True)
    rating = models.IntegerField()
    content = models.CharField(max_length=5000)

    def __str__(self):
        return self.ReviewID