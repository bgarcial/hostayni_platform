# https://docs.djangoproject.com/en/1.11/topics/signals/#django.dispatch.Signal


from django.dispatch import Signal

parsed_hashtags = Signal(providing_args=['hashtag_list'])