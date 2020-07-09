from django.forms import ModelForm

from apps.newsletters.models import NewsLetter


class NewsLetterModelForm(ModelForm):
    class Meta:
        model = NewsLetter
        fields = ["email"]
