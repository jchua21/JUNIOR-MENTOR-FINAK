from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CursoCreateForm
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Curso, Comment, Leccion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import FormView

class CursoListView(ListView):
    queryset = Curso.objects.all()
    paginate_by = 6
    template_name = 'cursos/curso_list.html'
    context_object_name = 'object_list'
    ordering = 'title'
    model = Curso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_paginated'] = self.paginate_by and context['paginator'].num_pages > 1
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        cat = self.request.GET.get('cat')
        author = self.request.GET.get('author')
        if q:
            queryset = queryset.filter(
                    Q(title__icontains=q) |
                    Q(details__icontains=q)
                    ).distinct()
        if cat:
            queryset = queryset.filter(categories__icontains=cat)

        if author:
            queryset = queryset.filter(user__username=author)
        return queryset

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('unlike')
        post_id2 = request.POST.get('like')
        if post_id is not None:
            post = get_object_or_404(Curso, id=post_id)
            post.likes.remove(request.user)
        if post_id2 is not None:
            post_id2 = request.POST.get('like')
            post = get_object_or_404(Curso, id=post_id2)
            post.likes.add(request.user)
        return redirect('home')


class CursoDetailView(DetailView):
    queryset = Curso.objects.all()

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        c_slug = request.POST.get('slug')
        enroll = request.POST.get('enroll')  # Agrega este campo en tu template

        if comment:
            if c_slug:
                post = get_object_or_404(Curso, slug=c_slug)
                comment = Comment.objects.create(
                        user=request.user, post=post, text=comment)
                comment.save()
                return redirect('detail', c_slug)

        if enroll:  # Si se recibe el campo "enroll"
            curso = get_object_or_404(Curso, slug=c_slug)
            profile = Profile.objects.get(user=request.user)

            if curso not in profile.cursos.all():
                profile.cursos.add(curso)
                curso.persons += 1  # Incrementar el contador de personas inscritas
                curso.save()

            return redirect('detail', c_slug)

        return redirect('detail', c_slug)


class CursoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cursos/curso_form.html'
    form_class = CursoCreateForm
    success_url = reverse_lazy('my_posts')
    success_message = "Curso creado exitosamente"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        # Obtener las lecciones desde el formulario
        lecciones_data = self.request.POST.get('lecciones')
        if lecciones_data:
            lecciones = [leccion.split(',') for leccion in lecciones_data.split(';')]
            for orden, titulo, enlace in lecciones:
                Leccion.objects.create(curso=instance, titulo=titulo, enlace=enlace)

        return super().form_valid(form)

class CursoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = CursoCreateForm
    template_name = 'cursos/curso_form.html'
    success_url = reverse_lazy('my_posts')
    success_message = "Curso actulizado correctamente"

    def get_queryset(self):
        return Curso.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lecciones'] = self.object.leccion_set.all()
        return context

    def form_valid(self, form):
        instance = form.save()

        # Actualizar las lecciones existentes
        lecciones_data = self.request.POST.get('lecciones')
        if lecciones_data:
            lecciones = [leccion.split(',') for leccion in lecciones_data.split(';')]
            existing_lecciones = instance.leccion_set.all()
            for orden, titulo, enlace in lecciones:
                leccion, created = Leccion.objects.get_or_create(curso=instance, titulo=titulo)
                leccion.enlace = enlace
                leccion.save()
                existing_lecciones = existing_lecciones.exclude(pk=leccion.pk)

            # Eliminar lecciones que no están en la lista actualizada
            existing_lecciones.delete()

        return super().form_valid(form)

class CursoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('my_posts')
    success_message = "Curso eliminado correctamente"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Curso.objects.filter(user=self.request.user)


class MyPostView(LoginRequiredMixin, ListView):
    template_name = 'cursos/my_posts.html'

    def get_queryset(self):
        return Curso.objects.filter(user=self.request.user)

def about(request):
    return render(request, "about.html")

def courses(request):
    return render(request, "courses.html")

