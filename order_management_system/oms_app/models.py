import uuid
from django.db import models
from django.db.models.enums import Choices
from django.utils.translation import gettext as _
from datetime import datetime
# Create your models here.
class Order(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  ticker = models.CharField(max_length=200)
  quantity = models.PositiveIntegerField()
  
  class OrderType(models.TextChoices):
    MARKET_ORDER = 'mar',_('Market Order')
    LIMIT_ORDER = 'lim',_('Limit Order')
    def __str__(self):
      return self.label
  
  order_type = models.CharField(
    max_length=3,
    choices=OrderType.choices,
    default=OrderType.MARKET_ORDER  
  )
  
  class Action(models.TextChoices):
    BUY = 'buy'
    SELL = 'sell'
    PENDING = 'pending'
  
  action = models.CharField(
    max_length=10,
    choices=Action.choices,
    default=Action.PENDING,
  )
  
  placed_time = models.DateTimeField(auto_now_add=True)
  expiry = models.DateTimeField(default=datetime.max)
  
  def get_order_type(self):
    """
      helper function to get order type from the enum class OrderType
    """
    return self.OrderType(self.order_type).name
  def get_action(self):
    """
      helper fucntion to get action type from the enum class Action
    """
    return self.Action(self.action).name
  def __str__(self):
    """
      Order to string function
    """
    return (
      f'Order {self.uuid} executed\n' 
      f'{self.get_order_type()} {self.get_action()} {self.quantity} {self.ticker}\n' 
      f'At {self.placed_time}, expired at {self.expiry}'
    )
  def save(self, *args, **kwargs): 
    """
      Overriding save() method for model subclass order
    """
    if (self.order_type != 'mar' and
          self.order_type != 'lim'):
      raise Exception(
        "invalid order type, try 'mar for market' or 'lim' for limit order argument"
      )

    if (self.action != 'buy' and
          self.action != 'sell'):
      raise Exception(
        "invalid action, try 'buy' and 'sell' as argument"
      )
    super().save(*args, **kwargs)  