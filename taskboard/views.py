from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ProjectForm, TaskForm
from .models import Project, Task


@login_required(login_url="/login/")
def dashboard(request):
    project_form = ProjectForm()
    task_form = TaskForm(user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_project":
            project_form = ProjectForm(request.POST)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.owner = request.user
                project.save()
                return redirect("dashboard")

        elif action == "create_task":
            task_form = TaskForm(request.POST, user=request.user)
            if task_form.is_valid():
                task_form.save()
                return redirect("dashboard")

        elif action == "update_status":
            task = get_object_or_404(
                Task,
                pk=request.POST.get("task_id"),
                project__owner=request.user,
            )
            new_status = request.POST.get("status")
            if new_status in Task.Status.values:
                task.status = new_status
                task.save(update_fields=["status"])
            return redirect("dashboard")

        elif action == "delete_task":
            task = get_object_or_404(
                Task,
                pk=request.POST.get("task_id"),
                project__owner=request.user,
            )
            task.delete()
            return redirect("dashboard")

        elif action == "delete_project":
            project = get_object_or_404(
                Project,
                pk=request.POST.get("project_id"),
                owner=request.user,
            )
            project.delete()
            return redirect("dashboard")

    projects = Project.objects.filter(owner=request.user).order_by("-created_at")
    all_tasks = Task.objects.filter(project__owner=request.user)
    tasks = all_tasks.select_related("project").order_by("-created_at")

    search_query = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "")

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(project__name__icontains=search_query)
        )

    if selected_status in Task.Status.values:
        tasks = tasks.filter(status=selected_status)

    context = {
        "projects": projects,
        "project_count": projects.count(),
        "total_tasks": all_tasks.count(),
        "done_count": all_tasks.filter(status=Task.Status.DONE).count(),
        "overdue_count": (
            all_tasks.filter(due_date__lt=timezone.localdate())
            .exclude(status=Task.Status.DONE)
            .count()
        ),
        "today": timezone.localdate(),
        "tasks": tasks[:10],
        "project_form": project_form,
        "task_form": task_form,
        "status_choices": Task.Status.choices,
        "search_query": search_query,
        "selected_status": selected_status,
    }
    return render(request, "taskboard/dashboard.html", context)


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "taskboard/signup.html", {"form": form})


@login_required(login_url="/login/")
def edit_task(request, task_id):
    task = get_object_or_404(
        Task,
        pk=task_id,
        project__owner=request.user,
    )

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(
        request,
        "taskboard/edit_task.html",
        {"form": form, "task": task},
    )


@login_required(login_url="/login/")
def edit_project(request, project_id):
    project = get_object_or_404(
        Project,
        pk=project_id,
        owner=request.user,
    )

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "taskboard/edit_project.html",
        {"form": form, "project": project},
    )