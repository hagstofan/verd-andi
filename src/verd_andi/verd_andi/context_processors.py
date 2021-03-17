from django.conf import settings


def display_name(request):
    return {
            'DISPLAY_NAME': settings.DISPLAY_NAME,
            'TEXT_NAME': settings.TEXT_NAME
           }
