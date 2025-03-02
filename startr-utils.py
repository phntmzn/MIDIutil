import os
from pathlib import Path
from midiutil import MIDIFile
from datetime import datetime

# Set correct path for external volume
desktop_path = Path("/volumes/bR")

# Ask the user for a folder name
user_folder_name = input("Enter a name for the drum samples folder (or press Enter to use a timestamp): ").strip()

# If the user doesn't provide a name, use a timestamp
if not user_folder_name:
    user_folder_name = f"drum_samples_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

# Create the base folder
base_folder = desktop_path / user_folder_name
os.makedirs(base_folder, exist_ok=True)

# Constants
BARS = 32
TEMPO = 156
BEATS_PER_BAR = 4
TOTAL_BEATS = BARS * BEATS_PER_BAR  # 32 bars * 4 beats per bar = 128 beats

# MIDI note mappings
HIHAT_NOTE = 60  # Closed Hi-Hat
SNARE_NOTE = 60  # Acoustic Snare
KICK_NOTE = 60  # Bass Drum

def create_drum_midi(filename, pattern, tempo=TEMPO, channel=1):
    """Creates a drum MIDI file with the given pattern on channel 1."""
    midi = MIDIFile(1)  # One track
    track = 0
    midi.addTrackName(track, 0, filename.stem)
    midi.addTempo(track, 0, tempo)

    for note, time in pattern:
        midi.addNote(track, channel=channel, pitch=note, time=time, duration=0.25, volume=100)

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

# Create 10 folders inside the user-defined folder
for i in range(1, 11):
    folder_name = base_folder / f"bR PARTICIPATION {i}"
    os.makedirs(folder_name, exist_ok=True)

    # Generate patterns
    hihat_pattern = [(HIHAT_NOTE, t * 0.5) for t in range(TOTAL_BEATS * 2)]  # 8th notes
    snare_pattern = [(SNARE_NOTE, t * BEATS_PER_BAR + 2) for t in range(BARS)]  # Beat 3 of every bar
    kick_pattern = [(KICK_NOTE, t * BEATS_PER_BAR) for t in range(0, BARS, 4)]  # Every 4 bars (bar 1, 5, 9, ...)

    # Create MIDI files, all set to channel 1
    create_drum_midi(folder_name / "hihat.mid", hihat_pattern, channel=1)
    create_drum_midi(folder_name / "snare.mid", snare_pattern, channel=1)
    create_drum_midi(folder_name / "kick.mid", kick_pattern, channel=1)

print(f"10 folders with hi-hat, snare, and kick patterns at {TEMPO} BPM created in {base_folder}.")
