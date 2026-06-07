from decimal import Decimal
from django.db import models


class SiteSettings(models.Model):
    """Singleton — siempre usar pk=1. Gestiona stats globales y contacto."""
    hero_badge      = models.CharField(max_length=150, default="✦ Plataforma SaaS para técnicos")
    hero_subtitle   = models.TextField(default="Llega a más clientes, gestiona tu taller y crece con MoyaOps. Tu negocio técnico en la plataforma de confianza.")
    countries_count     = models.PositiveIntegerField(default=12)
    technicians_count   = models.PositiveIntegerField(default=500)
    orders_count        = models.PositiveIntegerField(default=50, help_text="Se muestra como Xk+ (ej: 50 → 50k+)")
    support_email   = models.EmailField(default="hola@moyaops.com")
    app_url         = models.URLField(default="https://app.moyaops.com")

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self):
        return "Configuración del sitio"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Review(models.Model):
    author_name  = models.CharField(max_length=100, verbose_name="Nombre")
    initials     = models.CharField(max_length=3, verbose_name="Iniciales", help_text="Ej: CM para Carlos Méndez")
    avatar_color = models.CharField(max_length=20, default="#16a34a", verbose_name="Color avatar (hex)")
    star_rating  = models.PositiveSmallIntegerField(default=5, verbose_name="Estrellas (1-5)")
    text         = models.TextField(verbose_name="Texto de la reseña")
    shop_name    = models.CharField(max_length=100, blank=True, verbose_name="Nombre del taller")
    visible      = models.BooleanField(default=True, verbose_name="Visible")
    order        = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ["order"]
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f"{self.author_name} — {self.star_rating}★"

    @property
    def stars_html(self):
        return "★" * self.star_rating


class ChatbotEntry(models.Model):
    emoji             = models.CharField(max_length=10, verbose_name="Emoji")
    label             = models.CharField(max_length=50, verbose_name="Etiqueta del botón")
    trigger_keywords  = models.CharField(
        max_length=300, blank=True,
        verbose_name="Palabras clave",
        help_text="Separadas por comas. Ej: buscar,técnico,taller"
    )
    response          = models.TextField(verbose_name="Respuesta del bot")
    order             = models.PositiveIntegerField(default=0, verbose_name="Orden")
    active            = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        ordering = ["order"]
        verbose_name = "Entrada del chatbot"
        verbose_name_plural = "Entradas del chatbot"

    def __str__(self):
        return f"{self.emoji} {self.label}"

    def keywords_list(self):
        return [k.strip() for k in self.trigger_keywords.split(",") if k.strip()]


class PricingPlan(models.Model):
    name                 = models.CharField(max_length=50, verbose_name="Nombre del plan")
    monthly_price        = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Precio mensual (€)")
    annual_monthly_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Precio mensual con pago anual (€)", help_text="Ej: 12.90")
    annual_total         = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Total anual (€)", help_text="Ej: 154.80")
    is_featured          = models.BooleanField(default=False, verbose_name="Destacado (más popular)")
    is_coming_soon       = models.BooleanField(default=False, verbose_name="Próximamente")
    badge                = models.CharField(max_length=50, blank=True, verbose_name="Badge extra")
    order                = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ["order"]
        verbose_name = "Plan de precios"
        verbose_name_plural = "Planes de precios"

    def __str__(self):
        return self.name

    @property
    def monthly_price_display(self):
        if self.monthly_price is None:
            return ""
        v = self.monthly_price.quantize(Decimal("1"))
        return str(int(v)) if v == int(v) else str(v)

    @property
    def annual_monthly_display(self):
        if self.annual_monthly_price is None:
            return ""
        return str(self.annual_monthly_price)


class PricingFeature(models.Model):
    plan        = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, related_name="features")
    text        = models.CharField(max_length=200, verbose_name="Texto")
    is_included = models.BooleanField(default=True, verbose_name="Incluido")
    order       = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ["order"]
        verbose_name = "Característica del plan"
        verbose_name_plural = "Características del plan"

    def __str__(self):
        return self.text


class ShopCard(models.Model):
    name         = models.CharField(max_length=100, verbose_name="Nombre del taller")
    address      = models.CharField(max_length=200, verbose_name="Dirección")
    avatar_emoji = models.CharField(max_length=10, default="🔧", verbose_name="Emoji avatar")
    avatar_color = models.CharField(max_length=20, default="#e2e8f0", verbose_name="Color fondo avatar (hex)")
    rating       = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Rating (1-5)")
    review_count = models.PositiveIntegerField(verbose_name="Número de reseñas")
    services     = models.CharField(max_length=200, verbose_name="Servicios", help_text="Ej: Móviles · Tablets")
    visible      = models.BooleanField(default=True, verbose_name="Visible")
    order        = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ["order"]
        verbose_name = "Taller destacado"
        verbose_name_plural = "Talleres destacados"

    def __str__(self):
        return self.name


class VideoLink(models.Model):
    title       = models.CharField(max_length=100, verbose_name="Título")
    youtube_url = models.URLField(verbose_name="URL de embed YouTube", help_text="Ej: https://www.youtube.com/embed/VIDEO_ID")
    description = models.CharField(max_length=300, blank=True, verbose_name="Descripción")
    visible     = models.BooleanField(default=True, verbose_name="Visible")
    order       = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        ordering = ["order"]
        verbose_name = "Vídeo"
        verbose_name_plural = "Vídeos"

    def __str__(self):
        return self.title
