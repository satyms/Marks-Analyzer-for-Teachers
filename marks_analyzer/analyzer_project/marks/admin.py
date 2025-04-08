from django.contrib import admin
from .models import Student, Marks

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no')
    search_fields = ('name', 'roll_no')

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score')
    list_filter = ('subject',)
    search_fields = ('student__name', 'student__roll_no', 'subject') 