from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import pandas as pd
import numpy as np
from .models import Student, Marks
from django.db.models import Avg, Sum

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file')
            return redirect('upload_csv')
        
        try:
            df = pd.read_csv(csv_file)
            required_columns = ['Roll No', 'Name', 'Math', 'Science', 'English']
            if not all(col in df.columns for col in required_columns):
                messages.error(request, 'CSV must contain: Roll No, Name, Math, Science, English')
                return redirect('upload_csv')

            for _, row in df.iterrows():
                student, created = Student.objects.get_or_create(
                    roll_no=row['Roll No'],
                    defaults={'name': row['Name']}
                )

                # Create or update marks for each subject
                subjects = {'Math': row['Math'], 'Science': row['Science'], 'English': row['English']}
                for subject, score in subjects.items():
                    Marks.objects.update_or_create(
                        student=student,
                        subject=subject,
                        defaults={'score': score}
                    )

            messages.success(request, 'Data uploaded successfully!')
            return redirect('analyze')
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
            return redirect('upload_csv')

    return render(request, 'marks/upload_csv.html')

def analyze_marks(request):
    # Get all marks data
    marks_data = Marks.objects.all()
    
    # Calculate class averages per subject
    subject_averages = marks_data.values('subject').annotate(
        average=Avg('score')
    ).order_by('subject')

    # Get top 3 students based on total marks
    top_students = Student.objects.annotate(
        total_marks=Sum('marks__score')
    ).order_by('-total_marks')[:3]

    # Find weakest subject for each student
    students = Student.objects.all()
    student_weakest = []
    for student in students:
        student_marks = student.marks.all()
        if student_marks.exists():
            weakest_subject = student_marks.order_by('score').first()
            student_weakest.append({
                'student': student,
                'subject': weakest_subject.subject,
                'score': weakest_subject.score
            })

    # Prepare data for Chart.js
    subjects = [avg['subject'] for avg in subject_averages]
    averages = [float(avg['average']) for avg in subject_averages]

    context = {
        'subject_averages': subject_averages,
        'top_students': top_students,
        'student_weakest': student_weakest,
        'chart_subjects': subjects,
        'chart_averages': averages,
    }

    return render(request, 'marks/analyze.html', context) 