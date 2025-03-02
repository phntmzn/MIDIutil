import os
from pathlib import Path
from midiutil import MIDIFile

# Get the desktop path
desktop_path = Path.home() / "Desktop"

# Constants
BARS = 32  # Increased to 32 bars
TEMPO = 156
BEATS_PER_BAR = 4
TOTAL_BEATS = BARS * BEATS_PER_BAR  # 32 bars * 4 beats per bar = 128 beats

# MIDI note mappings
HIHAT_NOTE = 42  # Closed Hi-Hat
SNARE_NOTE = 38  # Acoustic Snare
KICK_NOTE = 36  # Bass Drum

def create_drum_midi(filename, pattern, tempo=TEMPO, channel=1):
    """Creates a drum MIDI file with the given pattern on channel 1."""
    midi = MIDIFile(1)  # One track
    track = 0
    midi.addTrackName(track, 0, filename.stem)
    midi.addTempo(track, 0, tempo)

    for note, time in pattern:
        midi.addNote(track, channel=channel, pitch=note, time=time, duration=0.5, volume=100)

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

# Create 10 folders on the desktop and generate MIDI files in each
base_folder = desktop_path / "drum_samples"
os.makedirs(base_folder, exist_ok=True)

for i in range(1, 11):
    folder_name = base_folder / f"folder_{i}"
    os.makedirs(folder_name, exist_ok=True)

    # Generate patterns
    hihat_pattern = [(HIHAT_NOTE, t * 0.5) for t in range(TOTAL_BEATS * 2)]  # 8th notes
    snare_pattern = [(SNARE_NOTE, t) for t in range(2, TOTAL_BEATS, 3)]  # Every third beat
    kick_pattern = [(KICK_NOTE, t * BEATS_PER_BAR) for t in range(0, BARS, 4)]  # Every 4 bars (bar 1, 5, 9, ...)

    # Create MIDI files, all set to channel 1
    create_drum_midi(folder_name / "hihat.mid", hihat_pattern, channel=1)
    create_drum_midi(folder_name / "snare.mid", snare_pattern, channel=1)
    create_drum_midi(folder_name / "kick.mid", kick_pattern, channel=1)

print(f"10 folders with hi-hat, snare, and kick patterns at {TEMPO} BPM on channel 1 created on the Desktop.")
