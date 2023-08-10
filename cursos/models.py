from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .snippets import generate_unique_slug

class Leccion(models.Model):
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=120)
    enlace = models.URLField()

    def __str__(self):
        return f"Lección: {self.titulo} - Curso: {self.curso}"

class Curso(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='cursos/')
    categories = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    price = models.IntegerField()
    vat = models.PositiveIntegerField(default=0)
    persons = models.PositiveIntegerField(default=0)
    details = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    views = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)

    def enroll_user(self, user):
        self.students.add(user)
        self.persons += 1
        self.save()

    def unenroll_user(self, user):
        if user in self.students.all():
            self.students.remove(user)
            self.persons -= 1
            self.save()

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()

    def get_categories(self):
        cats = self.categories.split(',')
        return cats

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Curso, self.title)
        else:  # create
            self.slug = generate_unique_slug(Curso, self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:100]

