from django.shortcuts import render, redirect, get_object_or_404
from .models import Tutorial, TutorialSeries, TutorialCategory, Friend, Photo, UserMessage
# Create your views here.
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib import messages
from .forms import (NewUserForm,
                    EditProfileForm,
                    EditUserInfo,
                    LoginForm,
                    UserAvatarForm,
                    UploadCourses,
                    AddNewCategory,
                    AddNewSeries,
                    GithubLogin,
                    UserContact)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def homepage(request):
    return render(request=request,
                  template_name='main/index.html',
                  context={"categories": TutorialCategory.objects.all,
                           "tutorials": Tutorial.objects.all})


def categories(request):
    return render(request=request,
                  template_name='main/categories.html',
                  context={"categories": TutorialCategory.objects.all})


def about(request):
    return render(request, 'main/about.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})

    form = NewUserForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logout Successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})


def single_slug(request, single_slug):
    # first check to see if the url is in categories.
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest(
                "tutorial_published")
            series_urls[m] = part_one.tutorial_slug

        return render(request=request,
                      template_name='main/series.html',
                      context={"tutorial_series": matching_series, "part_ones": series_urls})

    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]

    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
        tutorials_from_series = Tutorial.objects.filter(
            tutorial_series__series=this_tutorial.tutorial_series).order_by('tutorial_published')
        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)

        return render(request=request,
                      template_name='main/tutorial.html',
                      context={"tutorial": this_tutorial,
                               "sidebar": tutorials_from_series,
                               "this_tut_idx": this_tutorial_idx,
                               "user": request.user})


def account(request):
    current_user = request.user
    current_user_profile = request.user.userprofile
    avatar = request.user.photo
    users = User.objects.all()
    try:
        friend = Friend.objects.get(current_user=current_user)
        friends = friend.users.all()
    except Friend.DoesNotExist:
        friends = []
    if request.method == 'POST':
        form = GithubLogin(data=request.POST, instance=request.user.github)
        if form.is_valid():
            form.save()
        args = {"user": current_user,
                "profile": current_user_profile,
                "users": users,
                "friends": friends,
                "avatar": avatar,
                "github": current_user.github,
                "tutorials": Tutorial.objects.filter(tutorial_uploader_id=request.user.pk).order_by(
                    "-tutorial_published"),
                }
        return render(request=request,
                      template_name='main/account.html',
                      context=args)

    else:
        form = GithubLogin(instance=request.user.github)
        args = {"user": current_user,
                "profile": current_user_profile,
                "users": users,
                "friends": friends,
                "avatar": avatar,
                "github": current_user.github,
                "form": form,
                "tutorials": Tutorial.objects.filter(tutorial_uploader_id=request.user.pk).order_by(
                    "-tutorial_published"),
                }
        return render(request=request,
                      template_name='main/account.html',
                      context=args)


# def profile(request, username):
#     current_user = request.user
#     current_user_profile = request.user.userprofile
#     users = User.objects.all()
#     args = {"user": current_user,
#             "profile": current_user_profile,
#             "users": users}
#     return render(request=request,
#                   template_name='main/profile.html',
#                   context=args)


def account_edit(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("main:account")
    else:
        form = EditProfileForm(instance=request.user)
        args = {"form": form}
        return render(request,
                      template_name="main/account_edit.html",
                      context=args)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=request.user)
            return redirect("main:account")
        else:
            return redirect("main:change_password")

    else:
        form = PasswordChangeForm(user=request.user)
        args = {"form": form}
        return render(request,
                      template_name="main/change_password.html",
                      context=args)


def edit_info(request, username):
    if username != request.user.username:
        return redirect("main:login")
    if request.method == 'POST':
        form = EditUserInfo(data=request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('main:account')
    else:
        form = EditUserInfo(instance=request.user.userprofile)
        args = {'form': form}
        return render(request, 'main/edit_user_info.html', args)


# def edit_avatar(request, username):
#     if username != request.user.username:
#         return redirect("main:login")
#     if request.method == 'POST':
#         form = EditAvatar(data=request.POST, instance=request.user.userprofile, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('main:account')
#         else:
#             messages.error(request, "Invalid profile image.")
#             form = EditAvatar(instance=request.user.userprofile, files=request.FILES)
#             args = {'form': form}
#             return render(request,
#                           'main/edit_avatar.html',
#                           context=args)
#     else:
#         form = EditAvatar(instance=request.user.userprofile, files=request.FILES)
#         args = {'form': form}
#         return render(request,
#                       'main/edit_avatar.html',
#                       context=args)


def view_other_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
        profile = user.userprofile
        avatar = user.photo.file
        github = user.github.github_username
    else:
        user = request.user
        profile = user.userprofile
        avatar = user.photo.file
        github = user.github.github_username

    args = {"user": user,
            "profile": profile,
            "avatar": avatar,
            "github": github}
    return render(request, 'main/profile.html', args)


def change_friend(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == "add":
        Friend.make_friend(request.user, new_friend)
        return redirect('main:account')
    elif operation == 'remove':
        Friend.remove_friend(request.user, new_friend)
        return redirect('main:account')


def contact(request):
    user = request.user
    if request.method == "POST":
        form = UserContact(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:homepage")
    else:
        form = UserContact()
    return render(request, 'main/contact.html', {'form': form, "user": user})


def courses(request):
    args = {"tutorials": Tutorial.objects.order_by("-tutorial_published"),
            "categories": TutorialCategory.objects.all(), }
    return render(request, "main/courses.html", args)


def edit_avatar(request, username):
    if request.method == 'POST':
        form = UserAvatarForm(data=request.POST, files=request.FILES, instance=request.user.photo)
        if form.is_valid():
            form.save()
            return redirect('main:account')
    else:
        form = UserAvatarForm()
    return render(request, 'main/edit_avatar.html', {'form': form})


def upload_course(request):
    if request.method == "POST":
        form = UploadCourses(data=request.POST, files=request.FILES)
        # form2 = AddNewSeries(data=request.POST, files=request.FILES, instance=request.user)
        # form1 = AddNewCategory(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            course = form.save(commit=False)
            course.tutorial_slug = str(request.user.username) + course.tutorial_title.strip(' ')
            course.tutorial_published = timezone.now()
            course.tutorial_uploader = request.user
            course.save()
            return redirect("main:account")
    else:
        form = UploadCourses(files=request.FILES)
        return render(request, "main/upload_courses.html", {"form": form})


def add_category(request):
    if request.method == "POST":
        form = AddNewCategory(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            category = form.save(commit=False)
            category.category_slug = category.category.strip(" ")
            category.save()
            return redirect("main:upload")
    else:
        form = AddNewCategory()
        return render(request, "main/add_category.html", {"form": form})


def add_series(request):
    if request.method == "POST":
        form = AddNewSeries(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:upload")
    else:
        form = AddNewSeries()
        return render(request, "main/add_series.html", {"form": form})


def blog(request):
    return render(request, "main/blog.html")


def update_courses(request, id):
    instance = get_object_or_404(Tutorial, pk=id)
    form = UploadCourses(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('main:account')
    return render(request, 'main/upload_courses.html', {'form': form})


def delete(request, id):
    instance = Tutorial.objects.get(pk=id)
    instance.delete()
    return redirect('main:account')


def series(request, pk):
    args = {
        "series": TutorialSeries.objects.filter(series_category_id=pk),
    }
    return render(request, 'main/series.html', args)


def courses_series(request, pk):
    args = {
        "tutorials": Tutorial.objects.filter(tutorial_series_id=pk),
    }
    return render(request, 'main/courses_series.html', args)


def user_message(request):
    args = {
        "messages": UserMessage.objects.all(),
    }
    return render(request, "main/message.html", args)
