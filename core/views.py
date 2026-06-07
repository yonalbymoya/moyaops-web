import json
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views import View

from .models import SiteSettings, Review, ChatbotEntry, PricingPlan, ShopCard


class IndexView(View):
    def get(self, request):
        cfg     = SiteSettings.get()
        reviews = list(Review.objects.filter(visible=True)[:5])
        shops   = list(ShopCard.objects.filter(visible=True)[:5])
        plans   = list(PricingPlan.objects.prefetch_related("features").all())

        chatbot_entries = ChatbotEntry.objects.filter(active=True)
        chatbot_json = json.dumps([
            {
                "emoji":    e.emoji,
                "label":    e.label,
                "keywords": e.keywords_list(),
                "response": e.response,
            }
            for e in chatbot_entries
        ], ensure_ascii=False)

        pricing_json = json.dumps([
            {
                "name":    p.name,
                "monthly": p.monthly_price_display,
                "annual":  p.annual_monthly_display,
                "total":   str(p.annual_total) if p.annual_total else "",
            }
            for p in plans if not p.is_coming_soon
        ], ensure_ascii=False)

        return TemplateResponse(request, "core/index.html", {
            "cfg":          cfg,
            "reviews":      reviews,
            "shops":        shops,
            "pricing_plans": plans,
            "chatbot_json": chatbot_json,
            "pricing_json": pricing_json,
        })


class ReviewsAPIView(View):
    def get(self, request):
        data = [
            {
                "author_name":  r.author_name,
                "initials":     r.initials,
                "avatar_color": r.avatar_color,
                "star_rating":  r.star_rating,
                "text":         r.text,
                "shop_name":    r.shop_name,
            }
            for r in Review.objects.filter(visible=True)
        ]
        return JsonResponse(data, safe=False)


class ChatbotAPIView(View):
    def get(self, request):
        data = [
            {
                "emoji":    e.emoji,
                "label":    e.label,
                "keywords": e.keywords_list(),
                "response": e.response,
            }
            for e in ChatbotEntry.objects.filter(active=True)
        ]
        return JsonResponse(data, safe=False)
