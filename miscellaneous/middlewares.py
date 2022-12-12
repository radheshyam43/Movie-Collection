from django.db import transaction

from .models import KeyValueStore


def RequestCounterMiddleware(get_response):

    def middleware(request):
        # we update request count by acquiring request_count row
        # and update it.
        # Due to concurrency, we use select_for_update query

        request_count_object = KeyValueStore.objects.select_for_update().get(key='request_count')
        with transaction.atomic():
            new_request_count = int(request_count_object.value) + 1
            request_count_object.value = str(new_request_count)
            request_count_object.save()

        response = get_response(request)

        return response

    return middleware
