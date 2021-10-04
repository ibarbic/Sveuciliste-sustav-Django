from users.models import CustomUser, Predmeti, Uloge, Upisi
from django.contrib import admin

admin.site.register(CustomUser)
admin.site.register(Uloge)
admin.site.register(Predmeti)
admin.site.register(Upisi)
