from main.models import Shop
from django.db.models.query import QuerySet


def get_shops_around(your_location):
    your_lat = your_location[0]
    your_lng = your_location[1]
    __degree__ = 111.134861111

    list_of_ids = []

    for el in Shop.objects.all():
        lat = float(el.location.split(',')[0])
        lng = float(el.location.split(',')[1])

        distance = ((your_lng - lng) ** 2 + (your_lat - lat) ** 2) ** (1.0 / 2) * __degree__

        if distance < 0.5:
            list_of_ids.append(el.id)

    print(Shop.objects.filter(id__in=list_of_ids))
    return Shop.objects.filter(id__in=list_of_ids)
