from django import forms

from apps.cars.models import Car
from apps.photos.models import Photo


class ImageForm(forms.ModelForm):
    def __init__(self, dealer_id, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(dealer=dealer_id)

    class Meta:
        model = Photo
        fields = ['image', 'car']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }
