import Foundation
import AudioToolbox

let fileManager = FileManager.default

// Base path (external volume)
let basePath = "/Volumes/bR"

// Ask for folder name or use timestamp
print("Enter a name for the drum samples folder (or press Enter to use a timestamp): ", terminator: "")
let input = readLine() ?? ""
let folderName: String
if input.isEmpty {
    let formatter = DateFormatter()
    formatter.dateFormat = "yyyy-MM-dd_HH-mm-ss"
    folderName = "drum_samples_\(formatter.string(from: Date()))"
} else {
    folderName = input
}

// Final path
let baseFolder = URL(fileURLWithPath: basePath).appendingPathComponent(folderName)
try? fileManager.createDirectory(at: baseFolder, withIntermediateDirectories: true, attributes: nil)

// Constants
let bars = 32
let beatsPerBar = 4
let tempo: Double = 156
let totalBeats = bars * beatsPerBar

let hihatNote: UInt8 = 60
let snareNote: UInt8 = 60
let kickNote: UInt8 = 60

func createDrumMIDI(to url: URL, pattern: [(note: UInt8, time: Float64)]) {
    var sequence: MusicSequence?
    NewMusicSequence(&sequence)
    
    var track: MusicTrack?
    MusicSequenceNewTrack(sequence!, &track)
    
    for (note, time) in pattern {
        var message = MIDINoteMessage(
            channel: 0,
            note: note,
            velocity: 100,
            releaseVelocity: 0,
            duration: 0.25
        )
        MusicTrackNewMIDINoteEvent(track!, time, &message)
    }

    MusicTrackSetProperty(track!, kSequenceTrackProperty_TrackName, "Drum Track" as CFString)
    MusicSequenceSetTempo(sequence!, tempo)
    
    let midiFileURL = url as CFURL
    MusicSequenceFileCreate(sequence!, midiFileURL, .midiType, .eraseFile, 480)
}

// Create folders and generate MIDI
for i in 1...10 {
    let folderURL = baseFolder.appendingPathComponent("bR PARTICIPATION \(i)")
    try? fileManager.createDirectory(at: folderURL, withIntermediateDirectories: true, attributes: nil)
    
    let hihatPattern = (0..<(totalBeats * 2)).map { (hihatNote, Double($0) * 0.5) }
    let snarePattern = (0..<bars).map { (snareNote, Double($0 * beatsPerBar + 2)) }
    let kickPattern = (0..<bars/2).flatMap { t -> [(UInt8, Double)] in
        let base = t * 2 * beatsPerBar
        return [(kickNote, Double(base)), (kickNote, Double(base + 3))]
    }
    
    createDrumMIDI(to: folderURL.appendingPathComponent("hihat.mid"), pattern: hihatPattern)
    createDrumMIDI(to: folderURL.appendingPathComponent("snare.mid"), pattern: snarePattern)
    createDrumMIDI(to: folderURL.appendingPathComponent("kick.mid"), pattern: kickPattern)
}

print("10 folders with hi-hat, snare, and kick MIDI files created at \(baseFolder.path)")
