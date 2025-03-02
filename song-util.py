import os
from midiutil import MIDIFile

# Function to create a single MIDI file with C5 note on channel 0
def create_drum_midi(filename, duration=1, tempo=156):
    midi = MIDIFile(1)
    track = 0
    midi.addTrackName(track, 0, filename)
    midi.addTempo(track, 0, tempo)
    midi.addNote(track, channel=0, pitch=72, time=0, duration=duration, volume=100)  # C5 note
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

# Create 10 folders and generate MIDI files in each
base_folder = "drum_samples"
os.makedirs(base_folder, exist_ok=True)

for i in range(1, 11):
    folder_name = os.path.join(base_folder, f"folder_{i}")
    os.makedirs(folder_name, exist_ok=True)
    
    # Create MIDI files for snare, kick, and hihat with C5 note at 156 BPM on channel 0
    create_drum_midi(os.path.join(folder_name, "snare.mid"))
    create_drum_midi(os.path.join(folder_name, "kick.mid"))
    create_drum_midi(os.path.join(folder_name, "hihat.mid"))

print(f"10 folders with snare.mid, kick.mid, and hihat.mid using C5 at 156 BPM on channel 0 created in '{base_folder}'.")
