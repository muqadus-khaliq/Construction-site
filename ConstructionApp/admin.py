from django.contrib import admin
from .models import Client, Service, Project, Review, Profile, ProjectImage, ProjectVideo
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Admin Panel Customization
admin.site.site_header = 'Construction Website'
admin.site.index_title = 'Construction Admin Dashboard'
admin.site.site_title = 'Construction Admin Panel'

# Client Admin
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'image_preview')
    search_fields = ('name',)
    def image_preview(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" width="50" height="50"  />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Profile Picture'

# Service Admin
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_preview')
    search_fields = ('name',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

# Inline Admin for Project Image
class ProjectImageInline(admin.TabularInline):  # You can use admin.StackedInline as well for a different layout
    model = ProjectImage
    extra = 1  # Number of empty forms to show by default (can be adjusted)
    fields = ('image', 'caption')  # Fields to display in the inline form

# Inline Admin for Project Video
class ProjectVideoInline(admin.TabularInline):
    model = ProjectVideo
    extra = 1  # Number of empty forms to show by default
    fields = ('video', 'caption')  # Fields to display in the inline form
# Project Admin
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'budget', 'start_date', 'end_date', 'get_services', 'image_preview')
    inlines = [ProjectImageInline, ProjectVideoInline]
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'client__name')
    filter_horizontal = ('services',)

    def get_services(self, obj):
        return ", ".join([service.name for service in obj.services.all()])
    get_services.short_description = 'Services'
    
    def image_preview(self, obj):
        images = obj.images.all()  # Get all related ProjectImage instances
        if images:
            image_urls = [f'<img src="{image.image.url}" width="50" height="50" />' for image in images]
            return " ".join(image_urls)  # Join all image previews with space
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Project Images'

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'rating', 'review_text', 'date_submitted')
    list_filter = ('rating', 'date_submitted')
    search_fields = ('client__name', 'review_text')

# Profile Admin (User Extension)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Register Models with Custom Admin
admin.site.unregister(User)  # Unregister default User
admin.site.register(User, CustomUserAdmin)  # Register customized User admin
admin.site.register(Client, ClientAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Review, ReviewAdmin)
