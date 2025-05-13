#-------------------------------------------------------------------------------------
# Converts a MIDI file (.mid) into Python code using midiutil.
# The generated code programmatically reconstructs the MIDI contents.
# Output is saved as "generated_midi_code.py".
#-------------------------------------------------------------------------------------

from mido import MidiFile, tempo2bpm
from collections import defaultdict

def midi_to_midiutil_code(midi_path):
    mid = MidiFile(midi_path)
    tempo_map = {0: 120}
    output_lines = [
        "from midiutil import MIDIFile",
        "",
        f"mf = MIDIFile({len(mid.tracks)})",
    ]

    for i, track in enumerate(mid.tracks):
        time = 0
        note_starts = defaultdict(list)

        output_lines.append(f"\n# Track {i}")
        output_lines.append(f'mf.addTrackName({i}, 0, "Track_{i}")')

        for msg in track:
            time += msg.time
            if msg.type == 'set_tempo':
                bpm = int(tempo2bpm(msg.tempo))
                tempo_map[i] = bpm
                output_lines.append(f"mf.addTempo({i}, {round(time, 3)}, {bpm})")
            elif msg.type == 'note_on' and msg.velocity > 0:
                note_starts[msg.note].append((time, msg.velocity))
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if note_starts[msg.note]:
                    start_time, velocity = note_starts[msg.note].pop(0)
                    duration = max(time - start_time, 0.01)
                    output_lines.append(
                        f"mf.addNote({i}, 0, {msg.note}, {round(start_time, 3)}, {round(duration, 3)}, {velocity})"
                    )

    output_lines.append('\nwith open("output.mid", "wb") as f:')
    output_lines.append("    mf.writeFile(f)")

    return "\n".join(output_lines)

# Usage:
code = midi_to_midiutil_code("your_file.mid")
with open("generated_midi_code.py", "w") as f:
    f.write(code)
