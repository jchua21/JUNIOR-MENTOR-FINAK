from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, CreateView, UpdateView
from django.contrib.auth import logout
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.contrib.messages.views import SuccessMessageMixin
from cursos.models import Curso
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_message = "Account Created Successfully"
    success_url = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = RegisterForm
    template_name = 'registration/profile.html'
    queryset = User.objects.all()
    success_url = reverse_lazy('my_posts')
    success_message = "Profile Updated Successfully"


class ImageUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile_picture.html'

    def post(self, request, *args, **kwargs):
        img = request.FILES.get('image')
        user = get_object_or_404(User, username=request.user.username)
        user.profile.image = img
        user.save()

@login_required
def enroll_course(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    profile = Profile.objects.get(user=request.user)

    if curso not in profile.cursos.all():
        profile.cursos.add(curso)
        curso.persons += 1  # Incrementar el contador de personas inscritas
        curso.save()

    return redirect('detail', slug=curso.slug)

@login_required
def my_enrolled_courses(request):
    profile = Profile.objects.get(user=request.user)
    enrolled_courses = profile.cursos.all()
    return render(request, 'cursos/my_enrolled_courses.html', {'enrolled_courses': enrolled_courses})

@login_required
def unenroll_course(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    profile = Profile.objects.get(user=request.user)

    if curso in profile.cursos.all():
        profile.cursos.remove(curso)

    return redirect('my_enrolled_courses')
