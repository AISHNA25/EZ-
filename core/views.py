from django.contrib.auth import logout
from django.shortcuts import redirect

# Custom logout view to terminate session and redirect to login with a message
def custom_logout_view(request):
    logout(request)
    return redirect('login')
from django.contrib import messages
def splash_view(request):
    # If user is authenticated and not operational, show message
    if request.user.is_authenticated:
        if getattr(request.user, 'user_type', None) != 'operational' and not request.user.is_superuser:
            messages.error(request, 'You are not an operational user.')
            return render(request, 'splash.html')
    return render(request, 'splash.html')
# Client dashboard view
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
import os

@login_required
def client_dashboard_view(request):
    if not (getattr(request.user, 'user_type', None) == 'client' or request.user.is_superuser):
        return HttpResponseForbidden('You are not authorized to access this page.')
    files = UploadedFile.objects.all().order_by('-uploaded_at')
    return render(request, 'client_dashboard.html', {'files': files})

# File download view
@login_required
def download_file_view(request, file_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Direct access not allowed. Please use the download button.')
    file_obj = UploadedFile.objects.get(id=file_id)
    if not (getattr(request.user, 'user_type', None) == 'client' or request.user.is_superuser):
        return HttpResponseForbidden('You are not authorized to download this file.')
    file_path = file_obj.file.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
# File upload view for operational users
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .models import UploadedFile
from django.http import HttpResponseForbidden

@login_required
def operational_upload_view(request):
    # Allow superusers or operational users
    if not (getattr(request.user, 'user_type', None) == 'operational' or request.user.is_superuser):
        return HttpResponseForbidden('You are not authorized to access this page.')
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user
            uploaded_file.save()
            return render(request, 'operational_upload.html', {'form': form, 'success': True})
    else:
        form = FileUploadForm()
    return render(request, 'operational_upload.html', {'form': form})
# Home view
from django.http import HttpResponse

from django.shortcuts import redirect
def home_view(request):
    if request.user.is_authenticated:
        if getattr(request.user, 'user_type', None) == 'operational':
            return redirect('operational_upload')
        elif getattr(request.user, 'user_type', None) == 'client':
            return redirect('client_dashboard')
    return render(request, 'home.html')
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login

from django.contrib import messages as dj_messages
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        """
        After successful authentication, redirect user based on user_type and selected user_type.
        """
        user = form.get_user()
        selected_user_type = form.cleaned_data.get('user_type')
        # If user is client but tries to login as operational, show error
        if user.user_type == 'client' and selected_user_type == 'operational':
            dj_messages.error(self.request, 'You are not an operational user.')
            from django.contrib.auth import logout
            logout(self.request)
            return self.render_to_response(self.get_context_data(form=form))
        # If user is operational but tries to login as client, show error
        if user.user_type == 'operational' and selected_user_type == 'client':
            dj_messages.error(self.request, 'You are not a client user.')
            from django.contrib.auth import logout
            logout(self.request)
            return self.render_to_response(self.get_context_data(form=form))
        # Normal login flow
        response = super().form_valid(form)
        if hasattr(user, 'user_type'):
            if user.user_type == 'operational':
                return redirect('operational_upload')
            elif user.user_type == 'client':
                return redirect('client_dashboard')
        return response

# Signup view
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # use your actual login URL name
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'home.html')
