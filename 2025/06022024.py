import pretty_midi
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from midiutil import MIDIFile

def midi_to_note_sequence(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    notes = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            notes.append([note.start, note.end, note.pitch, note.velocity])
    return np.array(notes)

def prepare_sequences(note_sequence, sequence_length=50):
    input_sequences = []
    output_sequences = []
    for i in range(len(note_sequence) - sequence_length):
        input_sequences.append(note_sequence[i:i + sequence_length])
        output_sequences.append(note_sequence[i + sequence_length])
    return np.array(input_sequences), np.array(output_sequences)

def build_model(sequence_length):
    model = Sequential([
        LSTM(128, input_shape=(sequence_length, 4), return_sequences=True),
        Dropout(0.2),
        LSTM(128),
        Dropout(0.2),
        Dense(4, activation='linear')
    ])
    model.compile(loss='mse', optimizer='adam')
    return model

def generate_sequence(model, seed_sequence, length=100):
    generated_sequence = []
    current_sequence = seed_sequence
    for _ in range(length):
        prediction = model.predict(current_sequence[np.newaxis, :, :])[0]
        generated_sequence.append(prediction)
        current_sequence = np.vstack([current_sequence[1:], prediction])
    return np.array(generated_sequence)

def sequence_to_midi(sequence, output_file='output.mid'):
    midi = MIDIFile(1)
    track = 0
    time = 0
    midi.addTrackName(track, time, "Generated Track")
    midi.addTempo(track, time, 120)
    for note in sequence:
        start, end, pitch, velocity = note
        midi.addNote(track, 0, int(pitch), start, end - start, int(velocity))
    with open(output_file, "wb") as output_file:
        midi.writeFile(output_file)

# Example usage
midi_file = 'path/to/midi/file.mid'
note_sequence = midi_to_note_sequence(midi_file)
sequence_length = 50
X, y = prepare_sequences(note_sequence, sequence_length)
model = build_model(sequence_length)
model.fit(X, y, epochs=100, batch_size=64, validation_split=0.2)
seed_sequence = note_sequence[:sequence_length]
generated_sequence = generate_sequence(model, seed_sequence)
sequence_to_midi(generated_sequence)
