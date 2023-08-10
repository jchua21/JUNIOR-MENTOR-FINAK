from django.urls import path
from .views import CursoListView, CursoDetailView,\
    CursoCreateView, CursoUpdateView, CursoDeleteView,\
    MyPostView, about, courses

urlpatterns = [
    path('', CursoListView.as_view(), name='home'),
    path('about/', about, name = 'about'),
    path('courses/', courses, name = 'courses'),
    path('create/', CursoCreateView.as_view(), name='create'),
    path('<slug:slug>/', CursoDetailView.as_view(), name='detail'),
    path('<slug:slug>/update', CursoUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete', CursoDeleteView.as_view(), name='delete'),
    path('dashboard/myposts/', MyPostView.as_view(), name='my_posts'),
]
