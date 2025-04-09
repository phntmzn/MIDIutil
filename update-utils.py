#!/usr/bin/env python3

import os
from pathlib import Path
from midiutil import MIDIFile
import numpy as np

# Set the base folder for saving generated MIDI files
base_folder = Path("generated_midi_files")
os.makedirs(base_folder, exist_ok=True)

# Create 10 folders inside the user-defined folder
folder_paths = []
for i in range(1, 11):
    folder_path = base_folder / f"bR PARTICIPATION {i}"
    os.makedirs(folder_path, exist_ok=True)
    folder_paths.append(folder_path)

# CONSTANTS
BARS = 32
TEMPO = 156
BEATS_PER_BAR = 4
TOTAL_BEATS = BARS * BEATS_PER_BAR

# NOTEMAPPINGS (Note number mappings for different drums)
OH = 59  # Open Hi-hat
HH = 60  # Closed Hi-hat
S = 62   # Snare
K = 64   # Kick

# DRUM PATTERNS
def drumpat():
    # Hi-hat pattern: 8th notes
    hihat_pattern = [(HH, t * 0.5) for t in range(TOTAL_BEATS * 2)] 
    
    # Snare pattern: Beat 3 in each bar
    snare_pattern = [(S, t * BEATS_PER_BAR + 2) for t in range(BARS)] 

    open_hihat = [(OH, t * BEATS_PER_BAR + 2) for t in range(BARS)]
    
    # Kick pattern: Beats 1 and 4 in every even bar
    kick_pattern = [(K, t * BEATS_PER_BAR + offset) for t in range(0, BARS, 2) for offset in [0, 3]]
    
    return hihat_pattern + snare_pattern + kick_pattern

# CHORD MAPPINGS (placeholder for chords)
B1 = np.array([60, 60, 60])  # C Major
B2 = np.array([62, 62, 62])  # D Minor
B3 = np.array([64, 64, 64])  # E Minor
B4 = np.array([65, 67, 69])  # F Major

def crd():
    # Chord progression: Just an example, repeat chords in certain bars
    one = [(B1, c * BEATS_PER_BAR) for c in range(0, BARS, 2)]  # Chord 1 on beats 1, 3, etc.
    two = [(B2, c * BEATS_PER_BAR + 1) for c in range(0, BARS, 3)]  # Chord 2
    three = [(B3, c * BEATS_PER_BAR + 2) for c in range(0, BARS, 4)]  # Chord 3
    four = [(B4, c * BEATS_PER_BAR + 3) for c in range(0, BARS, 5)]  # Chord 4
    
    return one + two + three + four

def create_song_midi(filename, pattern, tempo=156, channel=0):
    """Creates a song MIDI file with the given pattern"""
    midi = MIDIFile(1)  # One Track
    track = 0
    midi.addTrackName(track, 0, filename.stem)
    midi.addTempo(track, 0, tempo)

    for chord, time in pattern:
        # For each chord, add the notes at the given time
        for note in chord:
            midi.addNote(track, channel, pitch=note, time=int(time), duration=1, volume=70)

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

def create_drum_midi(filename, pattern, tempo=156, channel=9):
    """Creates a drum MIDI file with the given pattern."""
    midi = MIDIFile(1)  # One track
    track = 0
    midi.addTrackName(track, 0, filename.stem)
    midi.addTempo(track, 0, tempo)

    for note, time in pattern:
        midi.addNote(track, channel, pitch=note, time=int(time), duration=0.25, volume=100)

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

# Main function to create the MIDI file and save individual drum files
def main():
    # Generate the drum patterns
    drum_pattern = drumpat()
    
    # Save individual drum parts as separate MIDI files inside the folders
    for folder in folder_paths:
        create_drum_midi(folder / "hihat.mid", [(HH, t * 0.5) for t in range(TOTAL_BEATS * 2)], tempo=TEMPO)
        create_drum_midi(folder / "snare.mid", [(S, t * BEATS_PER_BAR + 2) for t in range(BARS)], tempo=TEMPO)
        create_drum_midi(folder / "kick.mid", [(K, t * BEATS_PER_BAR + offset) for t in range(0, BARS, 2) for offset in [0, 3]], tempo=TEMPO)
        
        # Create song MIDI file with chord progression
        song_pattern = crd()  # Use the chord progression from `crd()`
        create_song_midi(folder / "Song.mid", song_pattern, tempo=TEMPO)
    
    # Print success message
    print("Drum MIDI files created successfully in individual folders!")
    print("Song MIDI files created successfully in individual folders!")

if __name__ == "__main__":
    main()
