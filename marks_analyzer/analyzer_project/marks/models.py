from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

    class Meta:
        ordering = ['roll_no']

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.CharField(max_length=50)
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}: {self.score}"

    class Meta:
        verbose_name_plural = "Marks"
        unique_together = ['student', 'subject'] 