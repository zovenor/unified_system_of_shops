from main.models import Shop, ShopChain


def get_shops_around(your_location, radius=0.5):
    your_lat = your_location[0]
    your_lng = your_location[1]
    __degree__ = 111.134861111

    list_of_ids = []

    for el in Shop.objects.all():

        lat, lng = el.lat, el.lng

        distance = ((your_lng - lng) ** 2 + (your_lat - lat) ** 2) ** (1.0 / 2) * __degree__

        if distance < radius:
            list_of_ids.append(el.id)
    return Shop.objects.filter(id__in=list_of_ids)


def products_in_chain_of_shops(chain_id):
    if not ShopChain.objects.filter(id=chain_id).exists():
        # Chain is not found!
        return None
    return Shop.objects.filter(chain=ShopChain.objects.get(id=chain_id))
