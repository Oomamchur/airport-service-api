from django.contrib import admin

from airport_service.models import (
    Crew,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Order,
    Ticket,
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class Order(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Crew)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Flight)
admin.site.register(Ticket)
