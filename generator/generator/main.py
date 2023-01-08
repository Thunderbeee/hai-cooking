from action import get_action
from state import get_state
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    print("start generating states: ")
    state = get_state(args)
    print("start generating actions:")
    action, action_summary = get_action(args)
    print("finished! please check files in the 'processed'")

    state.to_csv("./processed/state.csv")
    action.to_csv("./processed/action.csv")
    action_summary.to_csv("./processed/action_summary.csv")

    
