import uuid
from django.core.checks import messages
import pytz

from django.db import models
from django.db.models.enums import Choices
from django.utils.translation import gettext as _
from datetime import datetime
# Price dictionary
Price = {}
class Order(models.Model):
  #TODO shorten the UUID
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
  price = models.PositiveIntegerField(default=0)
  placed_time = models.DateTimeField(auto_now_add=True)
  expiry = models.DateTimeField(default=pytz.utc.localize(datetime.max))
  
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

  def placed_confirm(self):
    """
      Order placement confirmation
    """
    return (
      f'Trade order placed!:\n'
      f'{self.get_order_type()} {self.uuid} is through\n' 
      f'{self.get_action()} {self.quantity}'
      f'{self.ticker} shares at {self.price}\n'
      f'At {self.placed_time}, expired at {self.expiry}'
    )
  def executed_confirm(self, num_shares, price_per_shares):
    """
      Order execution confirmation
    """  
    return (
      f'Successfully matched!\n'
      f'{self.get_order_type()} {self.uuid} executed\n'
      f'{self.get_action()} {num_shares}'
      f'@ {price_per_shares}'
      f'at {datetime.utcnow().replace(tzinfo=pytz.utc)}\n'
    )
  def __str__(self):
    """
      Order class to_string()
    """
    return self.placed_confirm()
  def save(self, *args, **kwargs): 
    """
      Overriding save() method for model subclass order
    """
    if (self.order_type != 'mar' and
          self.order_type != 'lim'):
      raise Exception(
        "Invalid order type, try 'mar for market' or 'lim' for limit order argument"
      )

    if (self.action != 'buy' and
          self.action != 'sell'):
      raise Exception(
        "Invalid action, try 'buy' and 'sell' as argument"
      )
    super().save(*args, **kwargs)  
  
  #TODO finish
  def compat(self, ord):
    """
      Return a tuple of matching compatibility and agreement price between two orders 
    """

    if self.action == ord.action:
      return False

    #if both orders are market order 
    if self.order_type == 'mar' and ord.order_type == 'mar':
      # there is a previous price in the stock market
      if self.ticker in Price:
        return True, Price[self.ticker]
      # there is not
      return False
    
    # istant agreement if only one of the order is market order
    if self.order_type == 'mar':
      return True, ord.price
    if ord.order_type == 'mar':
      return True, self.price
    
    # if both are limit orders, compare buy-max / sell-min price
    if self.action == 'buy':
      return self.price > ord.price
    if self.action == 'sell':
      return self.price < ord.price

  def exchange(self, ord):
    """
      Exchange between two orders
    """
    if self.compat(ord) is False:
      raise Exception(
        f'Wrong argument Order {self.uuid} and {ord.uuid}'
      )
    compatability, price_per_shares = self.compat(ord)
    num_shares = min(self.quantity, ord.quantity)
    self.quantity -= num_shares
    ord.quantity -= num_shares

    return self.executed_confirm(num_shares, price_per_shares)

  def process(self):
    """
      Order's processer function, the oms's automatic broker
    """

    orders = Order.objects.filter(ticker=self.ticker)
    # print(orders)
    message=""
    for order in orders:
      # print(order)
      if self.compat(order) is not False:
        # print("Debugger 1:")
        compatitbility, Price[self.ticker] = self.compat(order)
        message+=self.exchange(order) + '\n'
        if order.quantity == 0:
          order.delete()
        if self.quantity == 0:
          self.delete()
          break
    
    return message  

          
    

        
