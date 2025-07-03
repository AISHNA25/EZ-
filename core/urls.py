from django.urls import path

from .views import CustomLoginView, signup_view, home_view, operational_upload_view, client_dashboard_view, download_file_view, splash_view
from .secure_download_views import generate_download_link, secure_download

from .views import custom_logout_view

urlpatterns = [
    path('', splash_view, name='splash'),
    path('home/', home_view, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', signup_view, name='signup'),
    path('operational/upload/', operational_upload_view, name='operational_upload'),
    path('client/dashboard/', client_dashboard_view, name='client_dashboard'),
    path('client/download/<int:file_id>/', download_file_view, name='download_file'),
    path('logout/', custom_logout_view, name='logout'),
    path('generate-download-link/<int:file_id>/', generate_download_link, name='generate_download_link'),
    path('secure-download/<str:token>/', secure_download, name='secure_download'),
]



