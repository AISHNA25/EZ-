from django.contrib import admin
from .models import User, UploadedFile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('user_type',)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_by', 'uploaded_at')
    search_fields = ('file', 'uploaded_by__username')
