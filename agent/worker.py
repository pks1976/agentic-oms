from tools.order_tools import get_order, cancel_order, refund

def execute(action):
    tool = action["tool"]
    args = action["args"]

    if tool == "get_order":
        return get_order(**args)
    elif tool == "cancel_order":
        return cancel_order(**args)
    elif tool == "refund":
        return refund(**args)
    else:
        raise ValueError(f"Unknown tool: {tool}")