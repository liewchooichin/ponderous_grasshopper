from django.contrib import admin
from django.utils.text import Truncator

# Register your models here.
from content.models import SeekingAd

@admin.register(SeekingAd)
class SeekingAdAdmin(admin.ModelAdmin):
    """Admin of SeekingAd.
        Truncate the ads content if it is too long.
    """
    # show_ad is a custom method to show_ad
    list_display = ("id", "create_date", "owner",
                    "seeking", "show_ad")
    
    def show_ad(self, obj):
        """Limit the ads to 200 characters"""
        truncated_ads = Truncator(obj.ads).chars(
            num=200, truncate="...", html=False
        )
        return truncated_ads
    
    show_ad.short_description = "Ads"