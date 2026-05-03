def get_order(order_id):
    print(f"[TOOL] Fetching order {order_id}")
    return{
        "order_id": order_id,
        "status": "delivered",
        "refundable": True
    }

def cancel_order(order_id):
    print(f"[TOOL] Cancelling order {order_id}")
    return {
        "order_id": order_id,
        "status": "cancelled",
        "refundable": True
    }


def refund(order_id):
    print(f"[TOOL] Refunding order {order_id}")
    return {
        "order_id": order_id,
        "status": "refunded",
        "refundable": False
    }
