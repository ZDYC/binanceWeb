import logging

from decimal import Decimal

from django.db import transaction

from .. models import Order


@transaction.atomic
def create_order(user, account,
                 symbol, quantity, price,
                 side, buy, sell,
                 order_type, time_in_force,
                 stop_price=None, iceberg_qty=None):
    order = Order.objects.create_order(
        user=user,
        account=account,
        symbol=symbol,
        quantity=quantity,
        price=price,
        side=side,
        buy=buy,
        sell=sell,
        order_type=order_type,
        time_in_force=time_in_force,
        stop_price=stop_price,
        iceberg_qty=iceberg_qty)
    return order
