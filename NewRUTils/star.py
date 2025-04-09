import numpy as np
import random
import hashlib
import multiprocessing

# Define the 12 notes in the chromatic scale
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

scales = {
    "C MAJOR": ["C", "D", "E", "F", "G", "A", "B", "C"],
    "C# MAJOR": ["C#", "D#", "E#", "F#", "G#", "A#", "B#", "C#"],
    "D MAJOR": ["D", "E", "F#", "G", "A", "B", "C#", "D"],
    "D# MAJOR": ["D#", "E#", "F##", "G#", "A#", "B#", "C##", "D#"],
    "E MAJOR": ["E", "F#", "G#", "A", "B", "C#", "D#", "E"],
    "F MAJOR": ["F", "G", "A", "A#", "C", "D", "E", "F"],
    "F# MAJOR": ["F#", "G#", "A#", "B", "C#", "D#", "E#", "F#"],
    "G MAJOR": ["G", "A", "B", "C", "D", "E", "F#", "G"],
    "G# MAJOR": ["G#", "A#", "B#", "C#", "D#", "E#", "F##", "G#"],
    "A MAJOR": ["A", "B", "C#", "D", "E", "F#", "G#", "A"],
    "A# MAJOR": ["A#", "B#", "C##", "D#", "E#", "F##", "G##", "A#"],
    "B MAJOR": ["B", "C#", "D#", "E", "F#", "G#", "A#", "B"],

    "C MINOR": ["C", "D", "E♭", "F", "G", "A♭", "B♭", "C"],
    "C# MINOR": ["C#", "D#", "E", "F#", "G#", "A", "B", "C#"],
    "D MINOR": ["D", "E", "F", "G", "A", "A♭", "C", "D"],
    "D# MINOR": ["D#", "E#", "F#", "G#", "A#", "B", "C#", "D#"],
    "E MINOR": ["E", "F#", "G", "A", "B", "C", "D", "E"],
    "F MINOR": ["F", "G", "A♭", "A", "C", "D♭", "E♭", "F"],
    "F# MINOR": ["F#", "G#", "A", "B", "C#", "D", "E", "F#"],
    "G MINOR": ["G", "A", "B♭", "C", "D", "E♭", "F", "G"],
    "G# MINOR": ["G#", "A#", "B", "C#", "D#", "E", "F#", "G#"],
    "A MINOR": ["A", "B", "C", "D", "E", "F", "G", "A"],
    "A# MINOR": ["A#", "B#", "C#", "D#", "E#", "F#", "G#", "A#"],
    "B MINOR": ["B", "C#", "D", "E", "F#", "G", "A", "B"]
}


time_value_durations = {
    "whole_note": 4,                # 4 beats
    "dotted_whole_note": 6,         # 1.5x the duration of a whole note
    "half_note": 2,                 # 2 beats
    "dotted_half_note": 3,          # 1.5x the duration of a half note
    "quarter_note": 1,              # 1 beat
    "dotted_quarter_note": 1.5,     # 1.5x the duration of a quarter note
    "eighth_note": 0.5,             # Half a beat
    "dotted_eighth_note": 0.75,     # 1.5x the duration of an eighth note
    "sixteenth_note": 0.25,         # Quarter of a beat
    "dotted_sixteenth_note": 0.375, # 1.5x the duration of a sixteenth note
    "thirty_second_note": 0.125,    # Eighth of a beat
    "dotted_thirty_second_note": 0.1875, # 1.5x the duration of a thirty-second note
    "sixty_fourth_note": 0.0625,    # Sixteenth of a beat
    "dotted_sixty_fourth_note": 0.09375, # 1.5x the duration of a sixty-fourth note
    "one_hundred_twenty_eighth_note": 0.03125, # 1/32 of a beat
    "dotted_one_hundred_twenty_eighth_note": 0.046875, # 1.5x the duration of a 128th note
    "two_hundred_fifty_sixth_note": 0.015625, # 1/64 of a beat
    "dotted_two_hundred_fifty_sixth_note": 0.0234375 # 1.5x the duration of a 256th note
}

chords = {
    # Triads
    'Major': np.array([0, 4, 7]),
    'Minor': np.array([0, 3, 7]),
    'Diminished': np.array([0, 3, 6]),
    'Augmented': np.array([0, 4, 8]),
    
    # 7th Chords
    'Major 7th': np.array([0, 4, 7, 11]),
    'Minor 7th': np.array([0, 3, 7, 10]),
    'Dominant 7th': np.array([0, 4, 7, 10]),
    'Diminished 7th': np.array([0, 3, 6, 9]),
    'Half-Diminished 7th': np.array([0, 3, 6, 10]),
    'Augmented 7th': np.array([0, 4, 8, 10]),

    # Extended Chords
    '9th': np.array([0, 4, 7, 10, 14]),
    'Major 9th': np.array([0, 4, 7, 11, 14]),
    'Minor 9th': np.array([0, 3, 7, 10, 14]),
    '11th': np.array([0, 4, 7, 10, 14, 17]),
    '13th': np.array([0, 4, 7, 10, 14, 21]),

    # Suspended Chords
    'Suspended 2nd (sus2)': np.array([0, 2, 7]),
    'Suspended 4th (sus4)': np.array([0, 5, 7]),
    
    # Added Note Chords
    '6th': np.array([0, 4, 7, 9]),
    'Minor 6th': np.array([0, 3, 7, 9]),
    'Add 9': np.array([0, 4, 7, 14]),
    'Minor Add 9': np.array([0, 3, 7, 14]),

    # Altered Chords
    '7th Flat 5': np.array([0, 4, 6, 10]),
    '7th Sharp 5': np.array([0, 4, 8, 10]),
    'Major 7th Sharp 5': np.array([0, 4, 8, 11]),
    'Minor 7th Flat 5': np.array([0, 3, 6, 10]),
}


inversions = {
    "Major": {
        "Inversion 0": np.array([0, 4, 7]),
        "Inversion 1": np.array([4, 7, 12]),
        "Inversion 2": np.array([7, 12, 16])
    },
    "Minor": {
        "Inversion 0": np.array([0, 3, 7]),
        "Inversion 1": np.array([3, 7, 12]),
        "Inversion 2": np.array([7, 12, 15])
    },
    "Diminished": {
        "Inversion 0": np.array([0, 3, 6]),
        "Inversion 1": np.array([3, 6, 12]),
        "Inversion 2": np.array([6, 12, 15])
    },
    "Augmented": {
        "Inversion 0": np.array([0, 4, 8]),
        "Inversion 1": np.array([4, 8, 12]),
        "Inversion 2": np.array([8, 12, 16])
    },
    "Major 7th": {
        "Inversion 0": np.array([0, 4, 7, 11]),
        "Inversion 1": np.array([4, 7, 11, 12]),
        "Inversion 2": np.array([7, 11, 12, 16]),
        "Inversion 3": np.array([11, 12, 16, 19])
    },
    "Minor 7th": {
        "Inversion 0": np.array([0, 3, 7, 10]),
        "Inversion 1": np.array([3, 7, 10, 12]),
        "Inversion 2": np.array([7, 10, 12, 15]),
        "Inversion 3": np.array([10, 12, 15, 19])
    },
    "9 sus": {
        "Inversion 0": np.array([0, 2, 7, 10]),
        "Inversion 1": np.array([2, 7, 10, 12]),
        "Inversion 2": np.array([7, 10, 12, 14]),
        "Inversion 3": np.array([10, 12, 14, 19])
    },
    "6": {
        "Major 6": {
            "Inversion 0": np.array([0, 4, 7, 9]),
            "Inversion 1": np.array([4, 7, 9, 12]),
            "Inversion 2": np.array([7, 9, 12, 16]),
            "Inversion 3": np.array([9, 12, 16, 19])
        },
        "Minor 6": {
            "Inversion 0": np.array([0, 3, 7, 9]),
            "Inversion 1": np.array([3, 7, 9, 12]),
            "Inversion 2": np.array([7, 9, 12, 15]),
            "Inversion 3": np.array([9, 12, 15, 19])
        }
    },
    "5": {
        "Inversion 0": np.array([0, 7]),
        "Inversion 1": np.array([7, 12]),
        "Inversion 2": np.array([12, 19])
    }
}

print(chords)
note_probabilities = [1/12] * 12  # Equal probabilities for twelve-tone row

# Define possible chords in a key (simplified for illustration) with probabilities

chord_probabilities = [0.20, 0.15, 0.15, 0.15, 0.20, 0.10, 0.05]  # Example probabilities

# Define possible note durations with probabilities
durations = ['quarter', 'eighth', 'half', 'whole']
duration_probabilities = [0.4, 0.3, 0.2, 0.1]  # Example probabilities



#////////////////////////////////////////////////////////////////////////
#///////////////////// TONE-ROW //////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////// 


# Generate twelve-tone row using numpy's random.choice with probabilities # NO RANDOM!
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




#////////////////////////////////////////////////////////////////////
#/////////////////////// FINITE-STATE-MACHINE CLASS//////////////////
#////////////////////////////////////////////////////////////////////


# Define state and FSM classes
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

# Define states and transitions
generate_melody_state = State('GenerateMelody', {})
generate_chord_state = State('GenerateChord', {})
generate_rhythm_state = State('GenerateRhythm', {})
apply_transformation_state = State('ApplyTransformation', {})

generate_melody_state.transitions = {
    'next': generate_chord_state
}
generate_chord_state.transitions = {
    'next': generate_rhythm_state
}
generate_rhythm_state.transitions = {
    'next': apply_transformation_state
}
apply_transformation_state.transitions = {
    'next': generate_melody_state
}



#//////////////////////////////////////////////////////////////
#                      UNI-GENERATOR                  #
# Generate unique songs using FSM NO MORE RANDOM! ALSO USE DFA
#/////////////////////////////////////////////////////////////
def generate_unique_song(queue, fsm):
    while True:
        if fsm.get_current_state() == 'GenerateMelody':
            twelve_tone_row = generate_twelve_tone_row()
            twelve_tone_matrix = create_twelve_tone_matrix(twelve_tone_row)
            melody = twelve_tone_matrix[0].tolist()
            fsm.transition('next')
        elif fsm.get_current_state() == 'GenerateChord':
            chords = generate_chord_progression(4)
            fsm.transition('next')
        elif fsm.get_current_state() == 'GenerateRhythm':
            rhythm = generate_rhythmic_pattern(12)  # Match the length of the twelve-tone row
            fsm.transition('next')
        elif fsm.get_current_state() == 'ApplyTransformation':
            transformations = [melody, transpose(melody, 2), invert(melody), retrograde(melody)]
            transformed_melody = random.choice(transformations)
            song = {
                'twelve_tone_row': twelve_tone_row,
                'twelve_tone_matrix': twelve_tone_matrix.tolist(),
                'melody': transformed_melody,
                'chords': chords,
                'rhythm': rhythm
            }
            # Create a unique hash for the song to ensure uniqueness
            song_hash = hashlib.sha256(str(song).encode()).hexdigest()
            queue.put((song, song_hash))
            fsm.transition('next')

# Consumer process to print songs and ensure uniqueness
def consumer(queue, target):
    unique_songs = set()
    generated = 0

    while generated < target:
        song, song_hash = queue.get()
        if song_hash not in unique_songs:
            unique_songs.add(song_hash)
            generated += 1
            # Print each song as it is generated
            print(f"Song {generated}:")
            print(f"Twelve-tone row: {song['twelve_tone_row']}")
            print(f"Twelve-tone matrix:")
            for row in song['twelve_tone_matrix']:
                print(row)
            print(f"Melody: {song['melody']}")
            print(f"Chords: {song['chords']}")
            print(f"Rhythm: {song['rhythm']}")
            print("\n")
            if generated % 1_000_000 == 0:  # Print progress every million songs
                print(f"Generated {generated} unique songs")

    print("Finished generating 20 billion unique songs.")


#//////////////////////////////////////////////////////////////
#////////////////////// MULTI-PROCESSING /////////////////////
#/////////////////////////////////////////////////////////////


if __name__ == '__main__':
    target = 20_000_000_000  # 20 billion unique songs
    num_producers = multiprocessing.cpu_count() - 1  # Use all but one core for producers

    queue = multiprocessing.Queue(maxsize=1000)

    # Initialize FSM for each producer
    fsms = [FSM(generate_melody_state) for _ in range(num_producers)]

    # Create producer processes
    producers = [multiprocessing.Process(target=generate_unique_song, args=(queue, fsms[i])) for i in range(num_producers)]

    # Create and start consumer process
    consumer_process = multiprocessing.Process(target=consumer, args=(queue, target))
    consumer_process.start()

    # Start producer processes
    for producer in producers:
        producer.start()

    # Wait for producer processes to finish
    for producer in producers:
        producer.join()

    # Wait for consumer process to finish
    consumer_process.join()