from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
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

    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '').strip()

    assignments = Assignment.objects.filter(user=request.user)
    if status_filter in dict(Assignment.STATUS_CHOICES):
        assignments = assignments.filter(status=status_filter)
    if search_query:
        assignments = assignments.filter(
            Q(title__icontains=search_query)
            | Q(course_code__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    assignments = assignments.order_by('due_date', '-created_at')
    return render(
        request,
        'assignments/assignment_list.html',
        {
            'form': form,
            'assignments': assignments,
            'status_filter': status_filter,
            'search_query': search_query,
        },
    )


@login_required
def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(
        request,
        'assignments/assignment_form.html',
        {'form': form, 'assignment': assignment},
    )


@login_required
def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list')
    return render(
        request,
        'assignments/assignment_confirm_delete.html',
        {'assignment': assignment},
    )


@login_required
def toggle_complete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        assignment.status = 'COMPLETED' if assignment.status != 'COMPLETED' else 'PENDING'
        assignment.save()
    return redirect('assignment_list')
