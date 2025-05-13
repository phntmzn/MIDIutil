import os
import mido
from mido import MidiFile

def generate_midiutil_code(input_file, output_script):
    # Load the input MIDI file
    mid = MidiFile(input_file)
    
    # Initialize the script with imports and MIDIFile initialization
    script_lines = [
        "from midiutil import MIDIFile\n",
        "midi = MIDIFile(numTracks={})\n".format(len(mid.tracks))
    ]
    
    for track_index, track in enumerate(mid.tracks):
        script_lines.append(f"# Track {track_index}: {track.name}\n")
        script_lines.append(f"midi.addTrackName({track_index}, 0, '{track.name}')\n")
        script_lines.append(f"midi.addTempo({track_index}, 0, 120)  # Default tempo\n")
        
        # Track events
        time = 0
        for msg in track:
            time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                script_lines.append(
                    "midi.addNote("
                    f"track={track_index}, channel={msg.channel}, "
                    f"pitch={msg.note}, time={time / mid.ticks_per_beat:.2f}, "
                    "duration=1, volume={})\n".format(msg.velocity)
                )
            elif msg.type == 'set_tempo':
                bpm = mido.tempo2bpm(msg.tempo)
                script_lines.append(
                    f"midi.addTempo({track_index}, {time / mid.ticks_per_beat:.2f}, {bpm})\n"
                )

    # Add code to save the MIDI file
    script_lines.append("\nwith open('output.mid', 'wb') as output:\n")
    script_lines.append("    midi.writeFile(output)\n")
    script_lines.append("print('MIDI file written to output.mid')\n")

    # Write the generated script to a file
    with open(output_script, "w") as script_file:
        script_file.writelines(script_lines)
    print(f"Generated Python script saved as: {output_script}")


def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".mid"):
            input_file = os.path.join(input_folder, file_name)
            output_script = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.py")
            print(f"Processing {input_file}...")
            generate_midiutil_code(input_file, output_script)


# Example usage
input_midi_folder = "/Users/deskadmin/Desktop/MIDI/LZR EXP CMIN 151/"  # Replace with your folder path
output_python_folder = "/Users/deskadmin/Desktop/MIDI/Scripts/"  # Replace with your desired output folder path

process_folder(input_midi_folder, output_python_folder)
