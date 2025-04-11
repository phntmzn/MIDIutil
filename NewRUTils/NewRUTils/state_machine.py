import multiprocessing
from meta_data import meta_data
from music_data import notes, scales, time_value_durations
from pattern_data import drum_pattern


#----------------------------------------------------------------------------------------------------------
# Finite State Machine

# This code defines a simple finite state machine (FSM) with states and transitions.
#----------------------------------------------------------------------------------------------------------
class State:
    def __init__(self, name, transitions):
        self.name = name
        self.transitions = transitions

class FSM:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def transition(self, input_value):
        if input_value in self.current_state.transitions:
            self.current_state = self.current_state.transitions[input_value]
        else:
            raise ValueError(f"No transition for input {input_value} in state {self.current_state.name}")
            
        def get_current_state(self):
            return self.current_state.name
        
    
        def generate_sequence(queue, fsm):
            while True:
                if fsm.get_current_state() == 'Generate Seq':
                    # Example base case for recursion
                    sequence = [1, 2, 3]  # Replace with actual sequence generation logic
                    queue.put(sequence)
                    break
    
        def _generate_sequence_logic(self):
            # Placeholder for sequence generation logic
            return "Generated Sequence"