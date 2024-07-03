from django.contrib import admin

from .models import ScoredData

# Register your models here.


class ScoreDataAdmin(admin.ModelAdmin):
    list_display = (
        "Type",
        "DriveTrain",
        "EngineSize",
        "Cylinders",
        "Horsepower",
        "MPG_City",
        "Weight",
        "Wheelbase",
        "P_MSRP",
        "Created_At",
    )


admin.site.register(ScoredData, ScoreDataAdmin)
