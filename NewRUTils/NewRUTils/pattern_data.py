import numpy as np



# Constants
TOTAL_BEATS = 32  # 4 beats per bar for a 4/4 pattern
BEATS_PER_BAR = 4
BARS = 32  # Number of bars

# Define MIDI note values for different drum sounds (assuming these are correct values)
HIHAT_NOTE = 42  # Hi-hat (closed) MIDI note number
SNARE_NOTE = 38  # Snare drum MIDI note number
KICK_NOTE = 36  # Kick drum MIDI note number
OPENHAT_NOTE = 60 # OPEN-HAT 
CYMBAL_NOTE = 49 # CYMBAL





#------------------------------------------------------------------------------------------------------------
# Function to create drum patterns

# This function generates a drum pattern based on the specified parameters.
#------------------------------------------------------------------------------------------------------------


def drum_pattern():
    # Create Hi-hat pattern (8th notes) - Hi-hat on every 8th note (every half-beat)
    hihat_pattern = [(HIHAT_NOTE, t * 0.5) for t in range(TOTAL_BEATS * 2)]  # 8th notes in one bar

    # Create Snare pattern - Snare on beat 3 of every bar
    snare_pattern = [(SNARE_NOTE, t * BEATS_PER_BAR + 2) for t in range(BARS)]  # Beat 3 of every bar

    # Create Kick pattern - Kick on beats 1 and 3 of each bar (alternating)
    kick_pattern = [(KICK_NOTE, t * BEATS_PER_BAR + offset) for t in range(0, BARS, 2) for offset in [0, 3]]

    # Create Open-Hat pattern - Open-Hat on Beats 2 1/2, 3, and 3 1/2
    open_hat = [(OPENHAT_NOTE, t * BEATS_PER_BAR + offset) for t in range(BARS) for offset in [2.5, 3, 3.5]]

    # Create Cymbal Pattern - Cymbal on Beat 1 every 8 bars
    cymbal_pattern = [(CYMBAL_NOTE, t * BEATS_PER_BAR) for t in range(0, BARS, 8)]  # Cymbal every 8 bars on Beat 1

    return hihat_pattern, snare_pattern, kick_pattern, open_hat, cymbal_pattern

# Call the function to get the patterns
hihat_pattern, snare_pattern, kick_pattern, open_hat, cymbal_pattern = drum_pattern()

# Combine all patterns
patterns = {
    "Hi-hat": hihat_pattern,
    "Snare": snare_pattern,
    "Kick": kick_pattern,
    "Open Hat": open_hat,
    "Cymbal": cymbal_pattern
}

# Display the patterns for each instrument
print("Hi-hat Pattern (8th Notes):", hihat_pattern)
print("Snare Pattern (Beat 3 of each bar):", snare_pattern)
print("Kick Pattern (Beats 1 and 3 of each bar):", kick_pattern)
print("Open-Hat Pattern:", open_hat)
print("Cymbal Pattern (Every 8 bars on Beat 1):", cymbal_pattern)

# Output the combined patterns in a structured way
for instrument, pattern in patterns.items():
    print(f"{instrument} Pattern: {pattern}")
