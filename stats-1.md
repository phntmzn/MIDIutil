To include detailed statistics alongside the parsed MIDI data, you can calculate various metrics such as:
	1.	Number of Notes: Total notes in each track.
	2.	Pitch Range: Minimum and maximum note values.
	3.	Velocity Stats: Average, minimum, and maximum velocities.
	4.	Duration Stats: Average, minimum, and maximum note durations.
	5.	Track Length: Total time in ticks or seconds for each track.

Here’s the updated parser with statistics:

⸻

MIDI Parser with Statistics

from mido import MidiFile

def parse_midi_with_stats(file_path):
    midi = MidiFile(file_path)
    print(f"MIDI file type: {midi.type}")
    print(f"Number of tracks: {len(midi.tracks)}")
    print(f"Ticks per beat: {midi.ticks_per_beat}")
    print("-" * 40)
    
    for i, track in enumerate(midi.tracks):
        print(f"Track {i}: {track.name}")
        print("-" * 20)
        
        note_count = 0
        velocities = []
        durations = []
        pitch_range = [float('inf'), float('-inf')]  # Min and Max pitch
        total_time = 0
        current_time = 0
        note_start_times = {}

        for msg in track:
            if not msg.is_meta:
                current_time += msg.time
                if msg.type == 'note_on' and msg.velocity > 0:
                    note_count += 1
                    velocities.append(msg.velocity)
                    pitch_range[0] = min(pitch_range[0], msg.note)
                    pitch_range[1] = max(pitch_range[1], msg.note)
                    note_start_times[msg.note] = current_time
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in note_start_times:
                        durations.append(current_time - note_start_times.pop(msg.note))
        
        total_time += current_time
        
        # Calculate statistics
        avg_velocity = sum(velocities) / len(velocities) if velocities else 0
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Output statistics
        print(f"  Total notes: {note_count}")
        print(f"  Pitch range: {pitch_range[0]} to {pitch_range[1]}")
        print(f"  Velocity: Min={min(velocities, default=0)}, Max={max(velocities, default=0)}, Avg={avg_velocity:.2f}")
        print(f"  Note durations (ticks): Min={min(durations, default=0)}, Max={max(durations, default=0)}, Avg={avg_duration:.2f}")
        print(f"  Total time (ticks): {total_time}")
        print("-" * 40)

# Example usage
file_path = 'example.mid'  # Replace with your MIDI file path
parse_midi_with_stats(file_path)



⸻

Example Output

For a sample MIDI file (example.mid), the output might look like this:

MIDI file type: 1
Number of tracks: 2
Ticks per beat: 480
----------------------------------------
Track 0: 
--------------------
  Total notes: 0
  Pitch range: inf to -inf
  Velocity: Min=0, Max=0, Avg=0.00
  Note durations (ticks): Min=0, Max=0, Avg=0.00
  Total time (ticks): 0
----------------------------------------
Track 1: 
--------------------
  Total notes: 4
  Pitch range: 60 to 62
  Velocity: Min=64, Max=64, Avg=64.00
  Note durations (ticks): Min=480, Max=480, Avg=480.00
  Total time (ticks): 1920
----------------------------------------



⸻

Detailed Explanation of Stats
	1.	Total Notes:
	•	Number of note_on messages with velocity > 0.
	2.	Pitch Range:
	•	The lowest (min) and highest (max) MIDI note values.
	3.	Velocity Stats:
	•	Calculated for all note_on messages:
	•	Min: Minimum velocity.
	•	Max: Maximum velocity.
	•	Avg: Average velocity.
	4.	Note Durations:
	•	Calculated as the difference between note_on and note_off events or note_on with velocity 0.
	5.	Total Time:
	•	Sum of all msg.time values in the track.

⸻

Variants of Stats

You can extend this script to include:
	•	Track Length in Seconds: Use the tempo to convert ticks to seconds.
	•	Unique Pitches: Count the number of unique pitches played.
	•	Histogram of Notes: Frequency of each pitch in the track.
	•	Time Signature and Tempo Analysis: Extract time signature and tempo changes.

Would you like me to implement one of these extensions or visualize this data?
