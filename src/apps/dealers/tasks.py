import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token

from common.celery import app


@app.task()
def refresh_dealer_tokens():
    now = timezone.now()
    tokens = Token.objects.filter(created__lte=now - timedelta(days=7))

    for token in tokens:
        token.key = token.generate_key()
        token.created = now

    Token.objects.bulk_update(tokens, fields=['key', 'created'])
    logging.info('Tokens have been refreshed')


@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % {reverse('verify', kwargs={'uuid': str(user.verification_uuid)})},
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
