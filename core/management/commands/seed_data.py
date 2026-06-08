from django.core.management.base import BaseCommand
from core.models import SiteSettings, Review, ChatbotEntry, PricingPlan, PricingFeature, ShopCard


class Command(BaseCommand):
    help = "Pobla la base de datos con los datos iniciales del sitio"

    def handle(self, *args, **options):
        # SiteSettings
        cfg, _ = SiteSettings.objects.get_or_create(pk=1)
        cfg.hero_badge = "✦ Plataforma SaaS para técnicos"
        cfg.hero_subtitle = "Llega a más clientes, gestiona tu taller y crece con MoyaOps. Tu negocio técnico en la plataforma de confianza."
        cfg.countries_count = 12
        cfg.technicians_count = 500
        cfg.orders_count = 50
        cfg.support_email = "hola@moyaops.com"
        cfg.app_url = "https://app.moyaops.com"
        cfg.save()

        # Reviews
        if not Review.objects.exists():
            reviews = [
                ("Carlos Méndez",  "CM", "#22c55e", "Excelente servicio, me atendieron en menos de una hora. ¡Totalmente recomendados!", "TechRepair Madrid"),
                ("María López",    "ML", "#8b5cf6", "Muy profesionales y honestos. Me mantuvieron informada en todo momento.",           "iRepair Buenos Aires"),
                ("Juan Pérez",     "JP", "#16a34a", "Precios justos y garantía real. Mi PS5 quedó como nueva. Volveré sin duda.",         "GameFix México DF"),
                ("Ana Suárez",     "AS", "#0891b2", "Recuperaron todos mis datos del disco. Pensé que los había perdido para siempre.",   "DataFix Santiago"),
                ("Roberto García", "RG", "#ea580c", "El seguimiento en tiempo real es increíble. Supe en todo momento el estado de mi portátil.", "PC Masters Bogotá"),
            ]
            for i, (name, initials, color, text, shop) in enumerate(reviews):
                Review.objects.create(author_name=name, initials=initials, avatar_color=color, text=text, shop_name=shop, order=i)

        # Chatbot
        if not ChatbotEntry.objects.exists():
            entries = [
                ("🔍", "Buscar técnico",   "buscar,técnico,taller",       '¡Perfecto! Usa la sección "Buscar" para encontrar talleres en tu ciudad. 📍 ¿Desde qué ciudad buscas?'),
                ("📦", "Mi orden",         "orden,estado,reparación",     "Para consultar tu orden escríbenos el código de orden o tu teléfono. 📦 ¿Cuál es tu código?"),
                ("💳", "Ver planes",       "plan,precio,coste",           "Tenemos Básico (€15/mes) y Profesional (€29/mes). Con pago anual ahorras un 14%. 💳 ¿Te ayudo a elegir?"),
                ("🔧", "Soy técnico",      "soy técnico,soy,registrar",   "¡Bienvenido! 🔧 Regístrate en app.moyaops.com — empieza con el plan básico sin tarjeta de crédito."),
                ("🛡️", "Garantía",         "garantía,garantia",           "Todos los servicios incluyen garantía de 30 días en mano de obra y piezas. 🛡️ ¿Tienes un problema?"),
                ("💰", "Métodos de pago",  "pago,pagar,método,tarjeta",   "Aceptamos efectivo, tarjeta y transferencia bancaria. El pago se realiza al retirar el equipo. 💰"),
                ("🚗", "A domicilio",      "domicilio,casa,recogida",     "Ofrecemos servicio a domicilio en zonas seleccionadas. 🚗 ¿En qué ciudad estás?"),
                ("🆘", "Soporte",          "soporte,ayuda,problema",      "Para soporte escríbenos a hola@moyaops.com o por WhatsApp. ¿En qué necesitas ayuda?"),
            ]
            for i, (emoji, label, keywords, response) in enumerate(entries):
                ChatbotEntry.objects.create(emoji=emoji, label=label, trigger_keywords=keywords, response=response, order=i)

        # Pricing
        basico, _ = PricingPlan.objects.update_or_create(
            name="Básico",
            defaults={"monthly_price": "9.00", "annual_monthly_price": "7.90", "annual_total": "94.80", "badge": "🎁 14 días gratis", "order": 0}
        )
        basico.features.all().delete()
        for i, feat in enumerate(["14 días de prueba gratis", "Acceso a todas las funciones", "1 tienda", "Empleados ilimitados", "App móvil incluida", "Soporte incluido"]):
            PricingFeature.objects.create(plan=basico, text=feat, order=i)

        pro, _ = PricingPlan.objects.update_or_create(
            name="Profesional",
            defaults={"monthly_price": "15.00", "annual_monthly_price": "12.90", "annual_total": "154.80", "is_featured": True, "badge": "⭐ Más popular", "order": 1}
        )
        pro.features.all().delete()
        for i, feat in enumerate(["Órdenes ilimitadas", "Tiendas ilimitadas", "Facturación completa + QR", "Inventario y POS", "Reportes avanzados", "WhatsApp integrado", "Soporte prioritario"]):
            PricingFeature.objects.create(plan=pro, text=feat, order=i)

        PricingPlan.objects.update_or_create(name="Empresa", defaults={"is_coming_soon": True, "order": 2})

        # Shops
        if not ShopCard.objects.exists():
            shops = [
                ("TechRepair Madrid",    "Calle Gran Vía 42, Madrid",     "🔧", "#fef9c3", "4.9", 234, "Móviles · Tablets"),
                ("PC Masters Bogotá",    "Av. El Dorado, Bogotá",         "💻", "#dcfce7", "4.8", 187, "Portátiles · PC"),
                ("GameFix México DF",    "Reforma 225, CDMX",             "🎮", "#ede9fe", "4.7", 312, "Consolas · Gaming"),
                ("iRepair Buenos Aires", "Florida 100, Buenos Aires",     "📱", "#fce7f3", "5.0", 98,  "iPhone · Samsung"),
                ("DataFix Santiago",     "Providencia, Santiago de Chile", "🖥️", "#e0f2fe", "4.6", 145, "PCs · Recuperación"),
            ]
            for i, (name, address, emoji, color, rating, reviews, services) in enumerate(shops):
                ShopCard.objects.create(name=name, address=address, avatar_emoji=emoji, avatar_color=color, rating=rating, review_count=reviews, services=services, order=i)

        self.stdout.write(self.style.SUCCESS("✓ Datos iniciales cargados correctamente"))
