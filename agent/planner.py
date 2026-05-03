from openai import OpenAI
import json

client = OpenAI()

VALID_TOOLS = {"get_order", "cancel_order", "refund"}


SYSTEM_PROMPT = """
You are an order management agent.

You MUST follow this lifecycle strictly:

1. If no order exists → call get_order
2. If status is 'delivered' → call cancel_order
3. If status is 'cancelled' AND refundable is true → call refund
4. If status is 'refunded' → finish

STRICT RULES:
- Never refund before cancelling
- Never cancel after refund
- Never repeat the same action unnecessarily
- Always use order_id = "123"
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Fetch order details",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancel an order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "refund",
            "description": "Refund an order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    }
]

def plan(state):
    # if "order" not in state:
    #     return {"tool": "get_order", "args": {"order_id": "123"}}
    
    # if state["order"]["status"] not in [ "cancelled", "refunded"]:
    #     return {"tool": "cancel_order", "args": {"order_id": "123"}}
    
    # if state["order"].get("refundable"):
    #     return {"tool": "refund", "args": {"order_id": "123"}}
    
    # return {"done": True}

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": f"{SYSTEM_PROMPT}"
             },
            {
                "role":"user", 
                "content": f"Current state: {state}. Order_id is always 123."
            }
        ],
        tools = TOOLS,
        tool_choice="auto"
    )

    print (response)

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]

        return {
            "tool": tool_call.function.name,
            "args": json.loads(tool_call.function.arguments)
        }
    
    return {"done": True}


        

    
def safe_parse(content):
    try:
        action = json.loads(content)

        # validate tool
        if "tool" in action:
            if action["tool"] not in VALID_TOOLS:
                raise ValueError("Invalid tool")

            # validate args
            if "order_id" not in action.get("args", {}):
                action["args"]["order_id"] = "123"  # fallback

        return action
    except Exception:
        return {"done": True}

                