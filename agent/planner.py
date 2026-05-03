from openai import OpenAI
import json

client = OpenAI()

VALID_TOOLS = {"get_order", "cancel_order", "refund"}


SYSTEM_PROMPT = """
You are an order management agent.

Your job is to decide the next action based on the current state.
The order_id is always "123".

Available tools:
- get_order(order_id)
- cancel_order(order_id)
- refund(order_id)

Rules:
- If no order info → call get_order
- If already refunded → finish
- If not cancelled → cancel first
- If refundable → refund
- Never repeat actions unnecessarily
 - Always include required arguments
- order_id MUST always be "123"

Output ONLY valid JSON:
Either:
{ "tool": "...", "args": {...} }

OR:
{ "done": true }

"""

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
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role":"user", "content": f"State: {state}"}
        ],
        temperature=0
    )

    print (response)

    content = response.choices[0].message.content

    try:
        action = safe_parse(content)
        return action
    except Exception:
        print("LLM output parsing failed:", content)
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

                