from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Review

# Apply summernote to all TextField in model.
class ReviewAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(Review, ReviewAdmin)