from decimal import Decimal

class MockOrder:
    def __init__(self, shipping, discount, total):
        self.shipping_price = Decimal(shipping)
        self.discount_amount = Decimal(discount)
        self.total_price = Decimal(total)
    
    def get_total_price_method(self):
        # The model method returns items_total + shipping - discount
        # But wait, the model's get_total_price calculates it dynamically from items.
        # The view SAVES the total_price field.
        # The template uses {{ order.get_total_price }} which calls the METHOD by default if it exists?
        # Or does it use the property/field?
        # Django templates resolve callable methods without args.
        pass

# Model Logic:
# get_total_price() -> items_total + shipping - discount

# My template math:
# order.get_total_price|add:order.discount_amount|add:order.shipping_price|add:"-1"|add:"1" ??

# Let's clarify:
# If Template calls get_total_price(): returns (Items + Ship - Disc)
# Subtotal = (Items + Ship - Disc) + Disc - Ship
#          = Items
# But the |add filter in Django strings converts to int/float if possible, but subtraction is tricky.
# |add:"-50" works.
# But adding a Decimal field ...
# And the complex chain...

print("Logic check:")
items = 100
ship = 50
disc = 10
total = items + ship - disc # 140

print(f"Total: {total}")
# Reversing to get Items:
calc_subtotal = total + disc - ship
print(f"Calculated Subtotal: {calc_subtotal}")

# Django template 'add' with negative number for subtraction?
# yes |add:"-50"
# But variable subtraction?
# |add:discount works (140 + 10 = 150)
# |add:shipping_price (needs negative)
# We can't easily negate a variable in Django templates standardly without a custom tag or pre-calculation.

print("ISSUE: Cannot easily negate 'shipping_price' in template to subtract it.")
