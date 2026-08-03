from django.conf import settings
from django.db import models
from django.urls import reverse


class UpdatePost(models.Model):
    CATEGORY_CHOICES = [
        ("policy", "Policy"),
        ("tip", "Portfolio Tip"),
        ("stock", "Stock"),
        ("risk", "Risk"),
        ("finance_news", "Finance News"),
        ("general", "General"),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="general")
    source_link = models.URLField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("updates:list")