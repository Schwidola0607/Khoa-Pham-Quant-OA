from django.core.management.base import BaseCommand, CommandError, CommandParser
from oms_app.models import Order


class Command(BaseCommand):
    help = "Cancel an order"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("order id", type=int, nargs=1, help="order's id to cancel")

    def handle(self, *args, **options):
        order_id = options["order id"][0]
        try:
            ord = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise CommandError(f"Order {order_id} does not exist")
        ord.delete()
