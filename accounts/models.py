from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cursos.models import Curso

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles', default='profiles/default.jpg')
    cursos = models.ManyToManyField(Curso, related_name='enrolled_students', blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def user_created(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@login_required
def enroll_course(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    profile = Profile.objects.get(user=request.user)

    if curso not in profile.cursos.all():
        profile.cursos.add(curso)

    return redirect('detail', slug=curso.slug)

