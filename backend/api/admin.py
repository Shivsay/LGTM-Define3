from django.contrib import admin
from .models import Aircraft, Flight, Assignment, PreAssignment

admin.site.register(Aircraft)
admin.site.register(Flight)
admin.site.register(Assignment)
admin.site.register(PreAssignment)