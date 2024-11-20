from . import orders, order_details, recipes, sandwiches, resources, reviews, payments, promotions

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
