from midiutil import MIDIFile

# Create a MIDI file with 1 track
midi = MIDIFile(1)

# Track, Channel, Time settings
track = 0
time = 0  # Starting at the beginning
midi.addTrackName(track, time, "16-bar MIDI Track")
midi.addTempo(track, time, 120)  # Set tempo (BPM)

# Instrument setup (0 is Acoustic Grand Piano)
midi.addProgramChange(track, channel=0, time=0, program=0)

# Helper: C Major scale notes (MIDI values)
c_major_scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C, D, E, F, G, A, B, C

# Generate 16 bars of quarter notes
note_duration = 1  # Each note lasts 1 beat (quarter note)
bars = 16

for bar in range(bars):
    for beat in range(4):  # 4 quarter notes per bar (4/4 time)
        note = c_major_scale[(bar * 4 + beat) % len(c_major_scale)]  # Cycle through scale
        velocity = 80  # Consistent velocity for all notes
        midi.addNote(track, channel=0, pitch=note, time=time, duration=note_duration, volume=velocity)
        time += note_duration  # Move to the next beat

# Save to file
with open("16_bar_quarter_notes.mid", "wb") as output_file:
    midi.writeFile(output_file)

print("16-bar MIDI file with quarter notes generated successfully.")
