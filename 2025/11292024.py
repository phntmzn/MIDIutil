from midiutil import MIDIFile


class MIDIComposer:
    def __init__(self, num_tracks=1, tempo=120):
        """
        Base class for creating MIDI files.
        """
        self.num_tracks = num_tracks
        self.tempo = tempo
        self.midi = MIDIFile(num_tracks)
        for track in range(num_tracks):
            self.midi.addTempo(track, 0, tempo)

    def add_note(self, track, channel, pitch, time, duration, volume):
        """
        Add a single note to the MIDI file.
        """
        self.midi.addNote(track, channel, pitch, time, duration, volume)

    def save(self, filename):
        """
        Save the MIDI file to the specified filename.
        """
        with open(filename, "wb") as output_file:
            self.midi.writeFile(output_file)


class AdvancedMIDIComposer(MIDIComposer):
    def __init__(self, num_tracks=1, tempo=120, time_signature=(4, 4)):
        """
        Extends MIDIComposer with time signature and advanced note management.
        """
        super().__init__(num_tracks, tempo)
        self.time_signature = time_signature
        self.chord_library = {
            "C_major": [60, 64, 67],
            "G_major": [67, 71, 74],
            "F_major": [65, 69, 72]
        }

    def add_chord(self, track, channel, chord_name, time, duration, volume):
        """
        Add a chord to the specified track.
        """
        chord_notes = self.chord_library.get(chord_name)
        if not chord_notes:
            raise ValueError(f"Chord '{chord_name}' is not in the library.")
        for note in chord_notes:
            self.add_note(track, channel, note, time, duration, volume)

    def generate_arpeggio(self, track, channel, chord_name, start_time, duration, interval, volume):
        """
        Generate an arpeggio by playing the notes of a chord in sequence.
        """
        chord_notes = self.chord_library.get(chord_name)
        if not chord_notes:
            raise ValueError(f"Chord '{chord_name}' is not in the library.")
        for i, note in enumerate(chord_notes):
            self.add_note(track, channel, note, start_time + i * interval, duration, volume)


class MIDIProject:
    def __init__(self):
        """
        Manages multiple MIDI compositions in a single project.
        """
        self.compositions = []

    def add_composition(self, composer):
        """
        Add a MIDIComposer or AdvancedMIDIComposer instance to the project.
        """
        if not isinstance(composer, MIDIComposer):
            raise TypeError("Only instances of MIDIComposer or its subclasses are allowed.")
        self.compositions.append(composer)

    def save_all(self, directory):
        """
        Save all compositions in the project to the specified directory.
        """
        for i, composer in enumerate(self.compositions):
            composer.save(f"{directory}/composition_{i + 1}.mid")


# Example Usage
if __name__ == "__main__":
    # Create an advanced composer
    composer = AdvancedMIDIComposer(num_tracks=2, tempo=120)

    # Add a single note
    composer.add_note(track=0, channel=0, pitch=60, time=0, duration=1, volume=100)  # C4

    # Add chords
    composer.add_chord(track=0, channel=0, chord_name="C_major", time=1, duration=1, volume=100)
    composer.add_chord(track=1, channel=0, chord_name="G_major", time=2, duration=1, volume=100)

    # Generate an arpeggio
    composer.generate_arpeggio(track=0, channel=0, chord_name="F_major", start_time=3, duration=0.5, interval=0.5, volume=100)

    # Save the single composition
    composer.save("advanced_composition.mid")

    # Create a MIDI project and save multiple compositions
    project = MIDIProject()
    project.add_composition(composer)

    # Add another composition
    another_composer = AdvancedMIDIComposer(num_tracks=1, tempo=90)
    another_composer.add_chord(track=0, channel=0, chord_name="C_major", time=0, duration=2, volume=80)
    project.add_composition(another_composer)

    # Save all compositions
    project.save_all("midi_project")
