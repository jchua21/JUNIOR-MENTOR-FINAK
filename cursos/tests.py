from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Comment, Curso, Leccion

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.curso = Curso.objects.create(
            user=self.user,
            title='Curso de Prueba',
            image='cursos/test_image.jpg',
            categories='Test',
            location='Test Location',
            price=100,
            vat=10,
            persons=0,
            details='Detalles del curso'
        )

    def test_comment_str_method(self):
        comment = Comment.objects.create(user=self.user, post=self.curso, text="Este es un comentario de prueba")
        self.assertEqual(str(comment), "Este es un comentario de prueba")

    def test_leccion_str_method(self):
        from .models import Leccion
        leccion = Leccion.objects.create(curso=self.curso, titulo="Lección de Prueba", enlace="https://www.example.com")
        self.assertEqual(str(leccion), f"Lección: {leccion.titulo} - Curso: {leccion.curso}")

    def test_curso_detail_view(self):
        response = self.client.get(reverse('detail', args=[self.curso.slug]))
        self.assertEqual(response.status_code, 200)

    def test_curso_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class CursoCreationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_curso_creation(self):
        curso = Curso.objects.create(
            user=self.user,
            title='Test Curso',
            image='cursos/test.jpg',
            categories='Test Category',
            location='Test Location',
            price=100,
            details='This is a test course.',
        )
        self.assertEqual(curso.title, 'Test Curso')
        self.assertEqual(curso.user, self.user)
        self.assertEqual(Curso.objects.count(), 1)

    def test_curso_enrollment(self):
        curso = Curso.objects.create(
            user=self.user,
            title='Test Curso',
            image='cursos/test.jpg',
            categories='Test Category',
            location='Test Location',
            price=100,
            details='This is a test course.',
        )
        student = User.objects.create_user(username='student', password='studentpassword')
        curso.enroll_user(student)
        self.assertEqual(curso.persons, 1)
        self.assertIn(student, curso.students.all())

    def test_curso_unenrollment(self):
        curso = Curso.objects.create(
            user=self.user,
            title='Test Curso',
            image='cursos/test.jpg',
            categories='Test Category',
            location='Test Location',
            price=100,
            details='This is a test course.',
        )
        student = User.objects.create_user(username='student', password='studentpassword')
        curso.enroll_user(student)
        curso.unenroll_user(student)
        self.assertEqual(curso.persons, 0)
        self.assertNotIn(student, curso.students.all())
