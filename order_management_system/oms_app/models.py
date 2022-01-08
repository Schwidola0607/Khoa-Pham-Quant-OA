from django.db import models
from django.db.models.enums import Choices
from django.utils.translation import gettext as _
from datetime import datetime
# Create your models here.
class Order(models.Model):
  ticker = models.CharField(max_length=200)
  quantity = models.PositiveIntegerField()
  
  class OrderType(models.TextChoices):
    MARKET_ORDER = 'mar',_('Market Order')
    LIMIT_ORDER = 'lim',_('Limit Order')
  
  order_type = models.CharField(
    max_length=3,
    choices=OrderType.choices,
    default=OrderType.MARKET_ORDER  
  )
  
  class Action(models.TextChoices):
    BUY = 'buy'
    SELL = 'sell'
    PENDING = 'pend'
  
  action = models.CharField(
    max_length=4,
    choices=Action.choices,
    default=Action.PENDING,
  )
  
  placed_time = models.DateTimeField(auto_now_add=True)
  expiry = models.DateTimeField(default=datetime.max)
  def __str__(self):
    return f'{self.order_type}: {self.action} {self.quantity} {self.ticker} at {self.placed_time}, expired at {self.expiry}'