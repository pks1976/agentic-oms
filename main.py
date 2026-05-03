
from agent.worker import execute
from agent.planner import plan

def main():

    state = {}

    max_steps = 10
    steps = 0

    while True:

        steps += 1
        if steps > max_steps:
            print("Safety break: too many steps")
            break

        action = plan(state)

        if "done" in action:
            print("Final state:", state)
            break

        result = execute(action)

        if action["tool"] == "get_order":
            state["order"] = result

        else:
            state["order"].update(result)
            

   

  

if __name__ ==  "__main__":
    main()