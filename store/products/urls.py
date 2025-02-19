from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("show/", views.showproducts, name="show"),
    path("dash/", views.dash, name='dash'),
    path("edit/<int:pk>/", views.edit, name='edit'),
    path("delete/<int:pk>/", views.delete, name='delete'),
    path("edit1/<int:pk>/", views.edit1, name='edit1'),
    path("delete1/<int:pk>/", views.delete1, name='delete1'),
    path("list/<int:pk>/", views.list_view, name='list_view'),
    path("list/", views.list, name='list'),
    path("", views.home, name='home'),
    path("patients/", views.patients, name='patients'),
    path("patientlist/", views.patientlist, name='patientlist'),
    path("report/<int:pk>/", views.report, name='report'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('chatbot/', views.chatbot, name='chatbot'),  # Updated line
    path('disease_detection/', views.disease_detection, name='disease_detection'),



]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)