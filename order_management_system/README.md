# Trade Execution System
  - Written in Django for future purposes (web app) and also make use of Django's rich Database API
  - Support basic order placement, order cancellation (limit order only)
  - Bookkeeping make direct use of Django Database API
  - Formatted by [Black](https://pypi.org/project/black/)
## Setup
`pip install -r requirements.txt`

## Usage
Django support a lot of built-in command but we will focus on 3 mains one
  - `python manage.py shell`:   
    * Basically our Bookkeeping API
    * More information [here](https://docs.djangoproject.com/en/4.0/topics/db/queries/)

  - `python manage.py place`
    * My custom built command for easier order placement
    Case insensitive!
    From the help menu
    ```
    Make an order
    positional arguments:
      user                  username
      ticker                stock's name
      quantity              how much shares
      order type            mar for market order or lim for limit order
      action                buy or sell
      price                 price
    ```
  - `python manage.py cancel`
    * My custom built command for order cancellation
    From the help menu
    ```
    Cancel an order

    positional arguments:
    order id              order's id to cancel
    ```

Some examples:
- 
```bash

[in]  python manage.py place Elon AAPL 100 lim bUy 97

[out] Elon successfully placed an order!:
LIMIT_ORDER a7e2b4da-784a-4c24-a22b-9d5c5c613f65 is through
BUY 80 AAPL shares at 97
At 2022-01-12 02:01:02.133134+00:00, expired at 9999-12-31 23:59:59.999999+00:00

[in]  python manage.py place T.Cook AApL 100 Lim seLL 80
[out] T.Cook order Successfully matched!
LIMIT_ORDER 18bca72f-f532-41c3-8e76-77c3532b93bc executed
SELL 10 AAPL shares at 88.5
At 2022-01-12 02:01:23.328507+00:00
portfolio goes to Elon

```

## File Structure
- Main implementation can be found in `models.py` inside class `Order`. 
- Custom commands can be found in `~/order_management_system/oms_app/commands/`