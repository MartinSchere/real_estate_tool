from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.FormListView.as_view(), name="form_generator"),
    path('form/', include([
        path('create/', views.FormCreateView, name="form_create"),
        path('fill/<uuid:pk>/', views.FormFillView.as_view(), name="form_fill"),
        path('edit/<uuid:pk>/', views.FormView.as_view(), name="form_edit"),
        path('delete/<uuid:pk>/', views.FormDeleteView.as_view(), name="form_delete"),
        path('thanks', views.ThanksView, name="thanks"),
        path('field/delete/<int:pk>/',
             views.FieldDeleteView.as_view(), name="field_delete")
    ])),
]
