# Pablo Oliva Quintana
# Date: 12/08/2024

import csv
from collections import deque

# The parse_ntm_file function reads and parses the .csv file defining NTM's structure. It
# extracts: machine's name, states, input and tape alphabets, start/accept/
# reject states, and transition rules. The transitions are stored as dictionaries for easy lookup 
# during the simulation. The output is a structured dictionary that represents the NTM configuration.

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

# The simulate_ntm function is going to calculate the simulation of the NTM. It uses a Breadth-First-Search
# algorithm, implementing a queue to explore all possible paths in a nondeterministical way.
    
def simulate_ntm(ntm, input_string, max_depth=1000000):
    """Simulates the NTM using BFS."""
    queue = deque([Configuration("", ntm["start_state"], input_string)])
    steps = 0  # Number of steps taken
    explored = []  # To store visited configurations (this will measure nondeterminism)
    
    while queue and steps < max_depth:
        current_level = len(queue)
        for _ in range(current_level):
            config = queue.popleft()
            explored.append(config)
            
            # Check if the current configuration reaches the accept state
            if config.state == ntm["accept_state"]:
                return explored, "accept", steps
            
            # Check if the current configuration reaches the reject state
            if config.state == ntm["reject_state"]:
                return explored, "reject", steps
            
            # Process transitions
            for transition in ntm["transitions"]:
                if config.state == transition["current_state"] and (config.right or "_")[0] == transition["input_symbol"]:
                    # Update the configuration based on the transition rules
                    new_left = config.left + (config.right[0] if config.right else "_")
                    new_state = transition["next_state"]
                    new_right = (config.right[1:] if len(config.right) > 1 else "") + "_"
                    if transition["move_direction"] == "L":
                        new_left, new_right = new_left[:-1], new_left[-1] + new_right
                    
                    # Enqueue the new configuration
                    queue.append(Configuration(new_left, new_state, new_right))
        
        steps += 1  # Increment depth level

    return explored, "timed out", steps

# Calculates the degree of nondeterminism
def calculate_nondeterminism(explored, depth):
    return len(explored) / depth if depth > 0 else 0

# Outputs the results of the simulation
def output_results(ntm, input_string, explored, result, depth, output_file="output.txt"):
    with open(output_file, 'w') as f:
        # Write simulation summary to file
        f.write(f"--- Simulation Summary ---\n")
        f.write(f"Machine: {ntm['name']}\n")
        f.write(f"Input String: {input_string}\n")
        f.write(f"Result: {result}\n")
        f.write(f"Depth: {depth}\n")
        f.write(f"Configurations Explored: {len(explored)}\n")
        nondeterminism = calculate_nondeterminism(explored, depth)
        f.write(f"Average Non-Determinism: {nondeterminism:.2f}\n")
        f.write("\nDetailed Steps:\n")
        for i, config in enumerate(explored):
            f.write(f"Step {i + 1}: {config}\n")
    
    # Print simulation summary to console
    print(f"--- Simulation Summary ---")
    print(f"Machine: {ntm['name']}")
    print(f"Input String: {input_string}")
    print(f"Result: {result}")
    print(f"Depth: {depth}")
    print(f"Configurations Explored: {len(explored)}")
    print(f"Average Non-Determinism: {nondeterminism:.2f}")
    print("\nDetailed Steps:")
    for i, config in enumerate(explored):
        print(f"Step {i + 1}: {config}")

# Example Usage
ntm_config = parse_ntm_file('ends_with_bb_PabloOlivaQuintana.csv')  # Change file name to test different machines
inputted_string = "aaa"  # Change input string to test different inputs
explored_configs, result, depth = simulate_ntm(ntm_config, inputted_string)  
output_results(ntm_config, inputted_string, explored_configs, result, depth, output_file="simulation_output.txt")