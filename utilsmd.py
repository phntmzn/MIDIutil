Ah, I see the requirement now! The second chord should start at beat 4 of the first bar but end before beat 3 of the next bar. Here’s how to adjust that:

Explanation of the Fix:
	•	First chord: Lasts for 3 beats (from beat 1 to beat 3).
	•	Second chord: Starts on beat 4 and ends at beat 2 of the next bar (lasting 2 beats).

Updated Code:

from midiutil import MIDIFile

# Create a MIDI file with 1 track
midi = MIDIFile(1)

# Track, Channel, and initial settings
track = 0
time = 0  # Start at the beginning
midi.addTrackName(track, time, "Chords with 3-2 Beat Pattern")
midi.addTempo(track, time, 120)  # Set tempo (BPM)

# Define two simple triads (chords) in C Major
chord1 = [60, 64, 67]  # C major chord: C, E, G
chord2 = [62, 65, 69]  # D minor chord: D, F, A

# Generate chords across 2 bars (4/4 time)
for bar in range(2):
    # First chord: Lasts for 3 beats (from beat 1 to beat 3)
    for note in chord1:
        midi.addNote(track, channel=0, pitch=note, time=time, duration=3, volume=80)
    
    # Move to beat 4 of the bar
    time += 3
    
    # Second chord: Starts at beat 4 and lasts 2 beats (ends before beat 3 of the next bar)
    for note in chord2:
        midi.addNote(track, channel=0, pitch=note, time=time, duration=2, volume=80)
    
    # Move to the start of the next bar
    time += 1  # Beat 1 of the next bar

# Save to file
with open("chord_3_2_beat_pattern.mid", "wb") as output_file:
    midi.writeFile(output_file)

print("MIDI file with 3-2 beat chord pattern generated successfully.")

Key Features:
	•	First chord: Plays from beat 1 to beat 3.
	•	Second chord: Starts on beat 4 and lasts 2 beats (from beat 4 of the current bar to beat 2 of the next bar).
	•	Result: Creates a flowing transition between chords without overlap on beat 3 of the next bar.

Let me know if this fits what you’re looking for!
