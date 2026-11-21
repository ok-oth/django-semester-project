from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AssignmentForm
from .models import Assignment

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('assignment_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def assignment_list(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()

    assignments = Assignment.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'assignments/assignment_list.html', {
        'form': form,
        'assignments': assignments,
    })

@login_required
def toggle_complete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    assignment.status = 'COMPLETED' if assignment.status != 'COMPLETED' else 'PENDING'
    assignment.save()
    return redirect('assignment_list')
