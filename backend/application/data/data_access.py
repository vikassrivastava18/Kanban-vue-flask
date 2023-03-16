from application.data.models import Card

from main import cache


@cache.cached(timeout=50, key_prefix='get_card_qyery')
def get_card(card_id):
    print("coming!@@#")
    card = Card.query.filter_by(card_id=card_id).first()
    print("cards", card)
    return card
