from django.contrib import admin

from .models import Question

# 使Question在admin里可以被操作
admin.site.register(Question)
