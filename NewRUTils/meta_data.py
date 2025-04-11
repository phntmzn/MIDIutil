#----------------------------------------------------------------------------
# Ask the user for the song metadata inputs
#---------------------------------------------------------------------------
song_name = input("Enter the song name: ")
project = input("Enter the project name: ")
composers = input("Enter the composers (comma separated): ").split(",")
bpm = int(input("Enter the BPM (beats per minute): "))
key = input("Enter the key (e.g., C Major): ")
time_signature = input("Enter the time signature (e.g., 4/4): ")
bars = int(input("Enter the number of bars: "))
beats_per_bar = int(input("Enter the number of beats per bar: "))


#-----------------------------------------------------------
# Ask user for number of songs to be generated
#------------------------------------------------------------
num_songs = int(input("Enter the number of songs to be generated: "))




# Display the song metadata
print("\nSong Metadata:")
print(f"Song Name: {song_name}")
print(f"Project: {project}")
print(f"Composers: {', '.join(composers)}")
print(f"BPM: {bpm}")
print(f"Key: {key}")
print(f"Time Signature: {time_signature}")
print(f"Bars: {bars}")
print(f"Beats per Bar: {beats_per_bar}")
print(f"Hi-hat Pattern: {hihat_pattern}")
print("Instrument: Closed Hi-hat (MIDI Note: 42, Description: A sharp, metallic sound produced by striking the closed hi-hat cymbals)")
