import ctypes
from ctypes import util, POINTER, c_void_p, c_uint32, c_char_p

# Load CoreMIDI framework
coremidi = ctypes.CDLL(util.find_library("CoreMIDI"))

# Find MIDI Interface
def find_midi_interface():
    midi_interface = coremidi.MIDIGetNumberOfSources()
    if midi_interface == 0:
        raise Exception("No MIDI interface found.")
    return midi_interface



# Define CoreMIDI types
MIDIClientRef = c_void_p
MIDIPortRef = c_void_p
MIDIEndpointRef = c_void_p
OSStatus = c_uint32

# Define callback prototype
MIDIReadProc = ctypes.CFUNCTYPE(None, c_void_p, POINTER(c_void_p), c_void_p)

# Callback function
@MIDIReadProc
def midi_input_callback(pktlist, read_proc_refcon, src_conn_refcon):
    packet_list = ctypes.cast(pktlist, POINTER(c_void_p))
    packet = ctypes.cast(packet_list.contents, POINTER(c_void_p))
    while packet:
        data = ctypes.string_at(packet.contents + 8, packet.contents[1])
        print(f"Received MIDI message: {list(data)}")
        packet = packet.contents[2]  # Move to the next packet

def main():
    # Create a MIDI client
    client = MIDIClientRef()
    status = coremidi.MIDIClientCreate(b"MyMIDIClient", None, None, ctypes.byref(client))
    if status != 0:
        print("Failed to create MIDI client.")
        return

    # Create an input port
    input_port = MIDIPortRef()
    status = coremidi.MIDIInputPortCreate(client, b"MyInputPort", midi_input_callback, None, ctypes.byref(input_port))
    if status != 0:
        print("Failed to create MIDI input port.")
        return

    # Get the number of MIDI sources
    num_sources = coremidi.MIDIGetNumberOfSources()
    if num_sources == 0:
        print("No MIDI input sources available.")
        return

    print("Available MIDI input sources:")
    for i in range(num_sources):
        source = coremidi.MIDIGetSource(i)
        name = ctypes.create_string_buffer(64)
        coremidi.MIDIObjectGetStringProperty(source, b"kMIDIPropertyName", ctypes.byref(name))
        print(f"{i}: {name.value.decode()}")

    # Select a source
    source_index = int(input("Select a source number to connect: "))
    if source_index < 0 or source_index >= num_sources:
        print("Invalid source index.")
        return

    source = coremidi.MIDIGetSource(source_index)
    status = coremidi.MIDIPortConnectSource(input_port, source, None)
    if status != 0:
        print("Failed to connect to MIDI source.")
        return

    print("Listening for MIDI input. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        coremidi.MIDIClientDispose(client)

if __name__ == "__main__":
    main()