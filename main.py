
from agent.worker import execute
from agent.planner import plan
from state.store import load_state, save_state

def main():

    state = load_state()
    print("Loaded state:", state)
    last_error = None

    max_steps = 10
    steps = 0

    VALID_ACTIONS = {
        None: ["get_order"],          # no state yet
        "delivered": ["cancel_order"],
        "cancelled": ["refund"],
        "refunded": []                # terminal
    }   

    while True:

        steps += 1
        if steps > max_steps:
            print("Safety break: too many steps")
            break
        
        action = plan(state, last_error)

        if "done" in action:
            print("Final state:", state)
            break

        status = state.get("order", {}).get("status")

        allowed_actions = VALID_ACTIONS.get(status, [])

        invalid_reason = None

        # ---- FSM VALIDATION ----
        if action["tool"] not in allowed_actions:
            invalid_reason = f"{action['tool']} not allowed in state '{status}'"

        if invalid_reason:
            print(f"Guard: {invalid_reason}")
            last_error = invalid_reason
            continue



        # ---- EXECUTION ----
        result = execute(action)

        # ---- STATE UPDATE ----
        if "order" not in state:
            state["order"] = {}

        state["order"].update(result)

        # ---- SAVE MEMORY ----
        save_state(state)

        print("STATE:", state)

        last_error = None
            

if __name__ ==  "__main__":
    main()