from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing/', include('landing.urls'))
]

if not settings.PRE_LAUNCH_MODE:
    urlpatterns += [
        path('accounts/', include('django.contrib.auth.urls')),
        path('register/', views.SignUpView.as_view(), name="register"),
        path('', include('app.urls')),
        path('form_generator/', include('form_generator.urls'))
    ]
