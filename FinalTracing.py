# Pablo Oliva Quintana
# Date: 12/08/2024

# The parse_ntm_file function reads and parses the .csv file defining NTM's structure. It
# extracts: machine's name, states, input and tape alphabets, start/accept/
# reject states, and transition rules. The transitions are stored as dictionaries for easy lookup 
# during the simulation. The output is a structured dictionary that represents the NTM configuration.

import csv
from collections import deque

# Parses the NTM CSV file and returns its configuration

def parse_ntm_file(file_name):
    """Parses the NTM CSV file and returns the machine's configuration."""
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)

    # Extract machine properties and transition rules into a dictionary
        
    machine = {
        "name": lines[0][0],  # Machine name
        "states": lines[1],   # List of states
        "input_alphabet": lines[2],  # Input alphabet
        "tape_alphabet": lines[3],   # Tape alphabet
        "start_state": lines[4][0],  # Start state
        "accept_state": lines[5][0], # Accept state
        "reject_state": lines[6][0], # Reject state
        "transitions": []            # List of transitions
    }
    
    # Parse transitions from the file and append them to the machine dictionary

    for line in lines[7:]:
        machine["transitions"].append({
            "current_state": line[0],
            "input_symbol": line[1],
            "next_state": line[2],
            "write_symbol": line[3],
            "move_direction": line[4]
        })
    
    return machine

# The following class represents a single state of the NTM during execution.
# It models the computation's current state, the tape contents, and the head's position.

class Configuration:
    def __init__(self, left, state, right):
        self.left = left    # Tape contents to the left of the head
        self.state = state  # Current state
        self.right = right  # Tape contents under and to the right of the head
    
    def __repr__(self):
        return f"({self.left}, {self.state}, {self.right})"

# The simulate_ntm function computes the simulation of the NTM. It uses a Breadth-First-Search
# algorithm, implementing a queue to explore all possible paths nondeterministically.
    
def simulate_ntm(ntm, input_string, max_depth=50):
    """Simulates the NTM using BFS."""
    # Initialize the queue with the starting configuration

    queue = deque([Configuration("", ntm["start_state"], input_string)])
    steps = 0  # Number of steps taken
    explored = []  # To store visited configurations (this will measure nondeterminism)
    
    while queue and steps < max_depth:

        current_level = len(queue)  # Number of configurations at the current depth

        for _ in range(current_level):
            config = queue.popleft()  # Dequeue the current configuration
            explored.append(config)   # Append it to the list of explored configurations
            
            # Check if the current configuration reaches the accept or reject state

            if config.state == ntm["accept_state"]:
                print(f"String accepted in {steps} steps!")
                return explored
            elif config.state == ntm["reject_state"]:
                continue
            
            # Process transitions to generate new configurations
            for transition in ntm["transitions"]:
                
                # Check if the current configuration matches the transition's conditions
                if config.state == transition["current_state"] and (config.right or "_")[0] == transition["input_symbol"]:
                    
                    # Update the configuration based on the transition rules
                    new_left = config.left + (config.right[0] if config.right else "_")  # Move the symbol under the head to the left tape
                    new_state = transition["next_state"]  # Transition to the next state
                    new_right = (config.right[1:] if len(config.right) > 1 else "") + "_"  # Update the right tape after moving the head
                    
                    if transition["move_direction"] == "L":  # Handle head movement to the left
                        new_left, new_right = new_left[:-1], new_left[-1] + new_right
                    # Append the new configuration to the queue for further exploration
                    queue.append(Configuration(new_left, new_state, new_right))
        
        steps += 1  # Increment the depth level to track the number of transitions

    # If the maximum depth is reached, print a timeout message
    print(f"Execution stopped after {steps} steps (max depth reached).")
    return explored

# The calculate_nondeterminism function computes the degree of nondeterminism
# by dividing the total number of configurations explored by the number of unique states visited.

def calculate_nondeterminism(explored):
    return len(explored) / len(set(config.state for config in explored))

# The output_results function formats and outputs the results of the simulation.
# It prints the NTM's name, the total configurations explored, the degree of nondeterminism,
# and the sequence of configurations leading to the result.

def output_results(explored, ntm):
    print(f"NTM: {ntm['name']}")  # Print machine's name
    print(f"Total configurations explored: {len(explored)}")  # Print the total configurations explored
    nondeterminism = calculate_nondeterminism(explored)  # Calculate and display the degree of nondeterminism
    print(f"Degree of Nondeterminism: {nondeterminism:.2f}")
    for i, config in enumerate(explored):  
        print(f"Step {i + 1}: {config}")


ntm_config = parse_ntm_file('a_plus.csv')  
explored_configs = simulate_ntm(ntm_config, "aaa")  
output_results(explored_configs, ntm_config)  