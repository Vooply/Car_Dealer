from django.views.generic import FormView
from django.urls import reverse

from apps.photos.forms import ImageForm
from apps.photos.models import Photo


class UpdateImageView(FormView):
    model = Photo
    form_class = ImageForm
    template_name = 'image-update.html'

    def get_success_url(self):
        return reverse('success')

    def form_valid(self, form):
        form.instance.dealer = self.request.user
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UpdateImageView, self).get_form_kwargs()
        kwargs['dealer_id'] = self.request.user.pk
        return kwargs
