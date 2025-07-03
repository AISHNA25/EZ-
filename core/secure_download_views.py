import secrets
import datetime
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse
from .models import UploadedFile

TOKEN_EXPIRY_SECONDS = 300  # 5 minutes

@login_required
@csrf_exempt
def generate_download_link(request, file_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)
    file = get_object_or_404(UploadedFile, id=file_id)
    # Only allow the user to download their own files or add your own logic
    # For now, allow all logged-in users to generate link
    token = secrets.token_urlsafe(32)
    cache_key = f'download_token_{token}'
    cache.set(cache_key, {
        'user_id': request.user.id,
        'file_id': file.id,
        'created': timezone.now().isoformat()
    }, timeout=TOKEN_EXPIRY_SECONDS)
    download_url = request.build_absolute_uri(reverse('secure_download', args=[token]))
    return JsonResponse({'success': True, 'url': download_url})

@login_required
def secure_download(request, token):
    cache_key = f'download_token_{token}'
    data = cache.get(cache_key)
    if not data:
        return HttpResponseForbidden('Invalid or expired download link.')
    if data['user_id'] != request.user.id:
        return HttpResponseForbidden('This link is not for you.')
    file = get_object_or_404(UploadedFile, id=data['file_id'])
    # Invalidate token after use
    cache.delete(cache_key)
    # Serve file
    response = file.file
    if hasattr(response, 'open'):
        response.open('rb')
    from django.http import FileResponse
    return FileResponse(response, as_attachment=True, filename=file.file.name.split('/')[-1])
