from django import forms
from .models import UpdatePost


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = UpdatePost
        fields = ["title", "category", "content", "source_link"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Example: Interest rate risk in bond portfolios",
            }),
            "category": forms.Select(attrs={
                "class": "form-select",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write a policy tip, risk update, stock note or finance news summary.",
            }),
            "source_link": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Optional article or source link",
            }),
        }