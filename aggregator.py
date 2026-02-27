from decimal import Decimal

def aggregate_sum(data, field):

    total = Decimal("0")

    for item in data:
        value = item.get(field)
        if value:
            total += Decimal(str(value))

    return float(total)