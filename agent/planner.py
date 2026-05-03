from openai import OpenAI
import json

client = OpenAI()

VALID_TOOLS = {"get_order", "cancel_order", "refund"}


SYSTEM_PROMPT = """
You are an order management agent.


Follow this lifecycle strictly:
1. get_order
2. cancel_order
3. refund
4. done

Rules:
- Never refund before cancelling
- Never cancel after refund
- Never repeat invalid actions
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

def plan(state, error = None):

    messages=[
        {
            "role": "system", 
            "content": f"{SYSTEM_PROMPT}"
            },
        {
            "role":"user", 
            "content": f"Current state: {state}. Order_id is always 123."
        }
    ]

    # Add self-correction signal if previous step failed
    if error:
        messages.append({
            "role": "user",
            "content": f"Previous action was invalid: {error}. Fix your decision."
        })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools = TOOLS,
        tool_choice="auto",
        temperature=0
    )


    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]

        try:
            args = json.loads(tool_call.function.arguments)
        except Exception:
            print("Error parsing tool arguments")
            return {"done": True}

        return {
            "tool": tool_call.function.name,
            "args": args
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

                