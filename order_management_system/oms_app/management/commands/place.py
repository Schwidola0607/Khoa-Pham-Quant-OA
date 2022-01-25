from django.core.management.base import BaseCommand, CommandError, CommandParser
from oms_app.models import Order


class Command(BaseCommand):
    help = "Make an order"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("user", type=str, nargs=1, help="username")
        parser.add_argument("ticker", type=str, nargs=1, help="stock's name")
        parser.add_argument("quantity", type=int, nargs=1, help="how much shares")
        parser.add_argument(
            "order type",
            type=str,
            nargs=1,
            help="mar for market order or lim for limit order",
        )
        parser.add_argument("action", type=str, nargs=1, help="buy or sell")
        parser.add_argument("price", type=int, nargs="?", default=0, help="price")

    def handle(self, *args, **options):
        ord = Order(
            user=options["user"][0],
            ticker=options["ticker"][0].upper(),
            quantity=options["quantity"][0],
            order_type=options["order type"][0].lower(),
            action=options["action"][0].lower(),
            price=options["price"],
        )
        ord.save()
        self.stdout.write(f"{ord.placed_confirm()}\n")
        self.stdout.write(f"{ord.process()}\n")
        # TODO: process transactions for market order here
