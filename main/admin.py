from django.contrib import admin
from .models import Tutorial, TutorialCategory, TutorialSeries, UserProfile, Friend, Github
from tinymce.widgets import TinyMCE
from django.db import models


# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {'fields': ["tutorial_title", "tutorial_published"]}),
        ("URL", {'fields': ["tutorial_slug"]}),
        ("Series", {'fields': ["tutorial_series"]}),
        ("Content", {"fields": ["tutorial_content", "file"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_info", "website", "city", "phone")

    def user_info(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by("-phone", "user")
        return queryset


admin.site.register(TutorialSeries)
admin.site.register(TutorialCategory)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Friend)
admin.site.register(Github)
