from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from contests.models import Contest

admin.site.register(Contest, SimpleHistoryAdmin)
# Register your models here.
