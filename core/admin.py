from django.contrib import admin
from .models import SiteSettings, Review, ChatbotEntry, PricingPlan, PricingFeature, ShopCard, VideoLink

admin.site.site_header = "MoyaOps — Panel de contenido"
admin.site.site_title  = "MoyaOps Admin"
admin.site.index_title = "Gestión del sitio web"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero", {
            "fields": ("hero_badge", "hero_subtitle"),
        }),
        ("Estadísticas (Sección Países)", {
            "fields": ("countries_count", "technicians_count", "orders_count"),
        }),
        ("Contacto y URLs", {
            "fields": ("support_email", "app_url"),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ("author_name", "star_rating", "shop_name", "visible", "order")
    list_editable = ("visible", "order")
    list_filter   = ("visible", "star_rating")
    ordering      = ("order",)


class PricingFeatureInline(admin.TabularInline):
    model  = PricingFeature
    extra  = 3
    fields = ("text", "is_included", "order")
    ordering = ("order",)


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display  = ("name", "monthly_price", "annual_monthly_price", "annual_total", "is_featured", "is_coming_soon", "order")
    list_editable = ("monthly_price", "annual_monthly_price", "annual_total", "is_featured", "is_coming_soon", "order")
    inlines       = [PricingFeatureInline]
    ordering      = ("order",)


@admin.register(ChatbotEntry)
class ChatbotEntryAdmin(admin.ModelAdmin):
    list_display  = ("emoji", "label", "trigger_keywords", "active", "order")
    list_editable = ("active", "order")
    ordering      = ("order",)
    fields        = ("emoji", "label", "trigger_keywords", "response", "active", "order")


@admin.register(ShopCard)
class ShopCardAdmin(admin.ModelAdmin):
    list_display  = ("name", "address", "rating", "review_count", "services", "visible", "order")
    list_editable = ("visible", "order")
    ordering      = ("order",)


@admin.register(VideoLink)
class VideoLinkAdmin(admin.ModelAdmin):
    list_display  = ("title", "youtube_url", "visible", "order")
    list_editable = ("visible", "order")
    ordering      = ("order",)
