def plan(state):
    if "order" not in state:
        return {"tool": "get_order", "args": {"order_id": "123"}}
    
    if state["order"]["status"] not in [ "cancelled", "refunded"]:
        return {"tool": "cancel_order", "args": {"order_id": "123"}}
    
    if state["order"].get("refundable"):
        return {"tool": "refund", "args": {"order_id": "123"}}
    
    return {"done": True}
                