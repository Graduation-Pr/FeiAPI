from .models import User, DoctorProfile, PatientProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone_number', 'gender', 'city', 'government', 'birth_date')
    readonly_fields = ('image_display',)  # Make image display read-only

    def image_display(self, obj):
        if obj.image:
            return '<img src="{0}" style="max-height:100px; max-width:100px;" />'.format(obj.image.url)
        else:
            return 'No Image'

    image_display.allow_tags = True
    image_display.short_description = 'Image'


admin.site.register(User, UserAdmin)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)