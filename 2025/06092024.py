import numpy as np
import random
import hashlib
import multiprocessing
from midiutil import MIDIFile

# Define possible notes in a scale (C major) with probabilities
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note_to_midi = {'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65, 'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71}
note_probabilities = [1/12] * 12  # Equal probabilities for twelve-tone row

# Define possible chords in a key (simplified for illustration) with probabilities
chords = ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim']
chord_probabilities = [0.20, 0.15, 0.15, 0.15, 0.20, 0.10, 0.05]  # Example probabilities

# Define possible note durations with probabilities
durations = ['quarter', 'eighth', 'half', 'whole']
duration_probabilities = [0.4, 0.3, 0.2, 0.1]  # Example probabilities

# Generate twelve-tone row using numpy's random.choice with probabilities
def generate_twelve_tone_row():
    return np.random.choice(notes, size=12, replace=False).tolist()

# Create twelve-tone matrix
def create_twelve_tone_matrix(row):
    matrix = np.zeros((12, 12), dtype=object)
    for i in range(12):
        matrix[i] = row[i:] + row[:i]
    return matrix

# Generate chord progressions using numpy's random.choice with probabilities
def generate_chord_progression(length):
    return np.random.choice(chords, size=length, p=chord_probabilities).tolist()

# Generate rhythmic patterns using numpy's random.choice with probabilities
def generate_rhythmic_pattern(length):
    return np.random.choice(durations, size=length, p=duration_probabilities).tolist()

# Apply transformations
def transpose(sequence, interval):
    note_map = {note: i for i, note in enumerate(notes)}
    transpose_map = {i: notes[(i + interval) % len(notes)] for i in range(len(notes))}
    return [transpose_map[note_map[note]] for note in sequence]

def invert(sequence):
    note_map = {note: i for i, note in enumerate(notes)}
    max_interval = max(note_map.values())
    invert_map = {i: notes[max_interval - i] for i in range(len(notes))}
    return [invert_map[note_map[note]] for note in sequence]

def retrograde(sequence):
    return sequence[::-1]

# DFA class for pattern matching
class DFA:
    def __init__(self, pattern):
        self.pattern = pattern
        self.states = self.build_states(pattern)

    def build_states(self, pattern):
        states = [{} for _ in range(len(pattern) + 1)]
        for i in range(len(pattern)):
            for c in set(pattern):
                k = min(len(pattern), i + 1)
                while k > 0 and pattern[:k] != pattern[i - k + 1:i + 1]:
                    k -= 1
                states[i][c] = k
        return states

    def search(self, text):
        state = 0
        matches = []
        for i in range(len(text)):
            state = self.states[state].get(text[i], 0)
            if state == len(self.pattern):
                matches.append(i - len(self.pattern) + 1)
        return matches

# Define state and FSM classes
class State:
    def __init__(self, name, transitions=None):
        self.name = name
        self.transitions = transitions or {}

class FSM:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def transition(self, direction):
        if direction in self.current_state.transitions:
            self.current_state = self.current_state.transitions[direction]
        else:
            raise ValueError(f"No transition for direction {direction} in state {self.current_state.name}")

    def get_current_state(self):
        return self.current_state.name

# Define the circle of fifths
circle_of_fifths = [
    'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F'
]

# Create states and transitions for FSM
states = {note: State(note) for note in circle_of_fifths}

for i, note in enumerate(circle_of_fifths):
    next_note = circle_of_fifths[(i + 1) % len(circle_of_fifths)]
    prev_note = circle_of_fifths[(i - 1) % len(circle_of_fifths)]
    states[note].transitions = {
        'clockwise': states[next_note],
        'counterclockwise': states[prev_note]
    }

# Initialize FSM
initial_state = states['C']
fsm = FSM(initial_state)

# Example usage of FSM
def navigate_circle_of_fifths(fsm, steps, direction):
    path = [fsm.get_current_state()]
    for _ in range(steps):
        fsm.transition(direction)
        path.append(fsm.get_current_state())
    return path

# Define patterns for DFA
melody_pattern = ['C', 'E', 'G']
melody_dfa = DFA(melody_pattern)

chord_pattern = ['C', 'G', 'Am']
chord_dfa = DFA(chord_pattern)

rhythm_pattern = ['quarter', 'eighth', 'quarter']
rhythm_dfa = DFA(rhythm_pattern)

# Define PFA class
class PFA:
    def __init__(self, states, transition_probabilities, initial_state):
        self.states = states
        self.transition_probabilities = transition_probabilities
        self.current_state = initial_state

    def transition(self):
        probabilities = self.transition_probabilities[self.current_state]
        self.current_state = np.random.choice(self.states, p=probabilities)

# Define states and transition probabilities for PFA
pfa_states = ['GenerateMelody', 'GenerateChord', 'GenerateRhythm', 'ApplyTransformation']
pfa_transition_probabilities = {
    'GenerateMelody': [0.0, 1.0, 0.0, 0.0],
    'GenerateChord': [0.0, 0.0, 1.0, 0.0],
    'GenerateRhythm': [0.0, 0.0, 0.0, 1.0],
    'ApplyTransformation': [1.0, 0.0, 0.0, 0.0]
}
initial_state = 'GenerateMelody'

pfa = PFA(pfa_states, pfa_transition_probabilities, initial_state)

# Define HMM class
class HMM:
    def __init__(self, states, start_probabilities, transition_probabilities, emission_probabilities):
        self.states = states
        self.start_probabilities = start_probabilities
        self.transition_probabilities = transition_probabilities
        self.emission_probabilities = emission_probabilities
        self.current_state = np.random.choice(self.states, p=self.start_probabilities)

    def step(self):
        self.current_state = np.random.choice(self.states, p=self.transition_probabilities[self.current_state])
        return np.random.choice(notes, p=self.emission_probabilities[self.current_state])

# Define states, start probabilities, transition probabilities, and emission probabilities for HMM
hmm_states = ['State1', 'State2']
hmm_start_probabilities = [0.5, 0.5]
hmm_transition_probabilities = {
    'State1': [0.7, 0.3],
    'State2': [0.4, 0.6]
}
hmm_emission_probabilities = {
    'State1': note_probabilities,
    'State2': note_probabilities
}

hmm = HMM(hmm_states, hmm_start_probabilities, hmm_transition_probabilities, hmm_emission_probabilities)

# Generate unique songs using FSM
def generate_unique_song(queue, fsm, pfa, hmm):
    while True:
        current_state = pfa.current_state
        if current_state == 'GenerateMelody':
            melody = [hmm.step() for _ in range(12)]
            if melody_dfa.search(melody):
                pfa.transition()
        elif current_state == 'GenerateChord':
            chords = generate_chord_progression(4)
            if chord_dfa.search(chords):
                pfa.transition()
        elif current_state == 'GenerateRhythm':
            rhythm = generate_rhythmic_pattern(12)
            if rhythm_dfa.search(rhythm):
                pfa.transition()
        elif current_state == 'ApplyTransformation':
            transformations = [melody, transpose(melody, 2), invert(melody), retrograde(melody)]
            transformed_melody = random.choice(transformations)
            song = {
                'melody': transformed_melody,
                'chords': chords,
                'rhythm': rhythm
            }
            # Create a unique hash for the song to ensure uniqueness
            song_hash = hashlib.sha256(str(song).encode()).hexdigest()
            queue.put((song, song_hash))
            pfa.transition()

# Consumer process to print songs and ensure uniqueness
def consumer(queue, target, path):
    unique_songs = set()
    generated = 0

    while generated < target:
        song, song_hash = queue.get()
        if song_hash not in unique_songs:
            unique_songs.add(song_hash)
            generated += 1
            # Save each song as a MIDI file
            save_midi(song, f"{path}/song_{generated}.mid")
            print(f"Song {generated} saved as MIDI")

def save_midi(song, filename):
    midi = MIDIFile(1)
    track = 0
    time = 0
    channel = 0
    volume = 100

    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 120)

    # Add melody to MIDI
    for i, note in enumerate(song['melody']):
        midi.addNote(track, channel, note_to_midi[note], time + i, 1, volume)

    # Add chords to MIDI
    for i, chord in enumerate(song['chords']):
        chord_notes = [note_to_midi[n] for n in list(chord) if n in note_to_midi]
        for note in chord_notes:
            midi.addNote(track, channel, note, time + i * 4, 4, volume)

    # Add rhythm to MIDI (simple example, not exact timing)
    duration_map = {'quarter': 1, 'eighth': 0.5, 'half': 2, 'whole': 4}
    current_time = time
    for i, duration in enumerate(song['rhythm']):
        midi.addNote(track, channel, 60, current_time, duration_map[duration], volume)  # C4 as placeholder
        current_time += duration_map[duration]

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

if __name__ == '__main__':
    target = 10  # Adjust target for demonstration
    path = "output_path"  # Specify the output path
    num_producers = multiprocessing.cpu_count() - 1  # Use all but one core for producers

    queue = multiprocessing.Queue(maxsize=1000)

    # Initialize FSM for each producer
    fsms = [FSM(generate_melody_state) for _ in range(num_producers)]

    # Create producer processes
    producers = [multiprocessing.Process(target=generate_unique_song, args=(queue, fsms[i], pfa, hmm)) for i in range(num_producers)]

    # Create and start consumer process
    consumer_process = multiprocessing.Process(target=consumer, args=(queue, target, path))
    consumer_process.start()

    # Start producer processes
    for producer in producers:
        producer.start()

    # Wait for producer processes to finish
    for producer in producers:
        producer.join()

    # Wait for consumer process to finish
    consumer_process.join()
