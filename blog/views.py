import json

from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from blog.forms import CommentForm, ClientInfoForm, CustomUserCreationForm
from blog.models import Blog, Category
from itertools import groupby
from django.utils.timezone import localtime


# Create your views here.
def index(request, tag=None):
    if not tag:
        blogs = Blog.objects.order_by("-created")
    else:
        blogs = Blog.objects.filter(category__name__icontains=tag).order_by("-created")

    group_year = {}
    for key, group in groupby(blogs, lambda post: localtime(post.created).year):
        group_year[key] = list(group)

    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    group_month = {}
    for key, group in groupby(blogs, lambda post: localtime(post.created).month):
        group_month[month_names.get(key, 'Unknown')] = list(group)

    categories = Category.objects.all()

    form = CommentForm()

    context = {
        "grouped_blogs_month": group_month,
        "grouped_blogs_year": group_year,
        "categories": categories,
        "form": form,
        "count": {"year": len(group_year), "month": len(group_month), "blog": blogs.count()}
    }

    return render(request, "blog/index.html", context=context)


def home(request):
    if request.method == "POST":
        form = ClientInfoForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.save()
            return redirect('home')
    else:
        form = ClientInfoForm()
    context = {
        'form': form
    }
    return render(request, 'home/home.html', context=context)


def add_comment_to_post(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return redirect('/')
    else:
        form = CommentForm()
    return render(request, 'blog/index.html', context={"form": form})


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_done.html'
    success_url = '/accounts/password_reset/done/'  # URL to redirect after password reset request


def register(request):
    if request.method == "GET":
        return render(
            request, "blog/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))
