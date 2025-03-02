To save all **FLPs with MIDI Out** efficiently and extract later, here's a structured approach:  

### **Step 1: Bulk Save All FLPs with MIDI Out**  
If you haven't already, ensure all your FLPs are saved in a single location (your online storage). You might want to:
- Use **FL Studio's scripting (Python API)** to automate saving.
- Manually batch save if automation isn’t feasible.

---

### **Step 2: Extract MIDI Data from FLPs Later**  
Since FL Studio project files (`.flp`) store MIDI data in a structured binary format, you need a way to **extract MIDI data**.  

#### **Option 1: Using FL Studio's Export MIDI (Manual)**
1. Open each `.flp` in FL Studio.
2. Navigate to `File → Export → MIDI file`.
3. Save the `.mid` file for external analysis.

This is **tedious** for 20K files.

---

#### **Option 2: Automate Extraction (Python + FL Studio Scripting)**
FL Studio allows scripting through **Python** (via the `FLPy` API). You can write a script to:
1. Open each `.flp` automatically.
2. Export MIDI files from **MIDI Out** channels.
3. Save `.mid` files in a separate folder.

Example script (requires FL Studio scripting):
```python
import flstudio

def export_midi_from_flp(flp_path, output_dir):
    flstudio.load_project(flp_path)
    midi_file = output_dir + "/" + flp_path.split("/")[-1].replace(".flp", ".mid")
    flstudio.export_midi(midi_file)
    print(f"Exported: {midi_file}")

# Run for all FLPs in a directory
import os

flp_dir = "path/to/flps"
output_dir = "path/to/output/midi"

for flp in os.listdir(flp_dir):
    if flp.endswith(".flp"):
        export_midi_from_flp(os.path.join(flp_dir, flp), output_dir)
```
This method **automates MIDI extraction** but requires **FL Studio scripting support**.

---

#### **Option 3: Extract MIDI Data Directly from FLP Files (Without FL Studio)**
Since `.flp` files are structured binary files, we can **parse them directly** and extract MIDI data using Python.

1. Use a library like [`FLP Parser`](https://github.com/giulianodelagala/flp-parser) to read `.flp` files.
2. Extract MIDI Out data and convert it into `.mid` files.

Would you like help setting up a full **FLP-to-MIDI extraction pipeline** without opening FL Studio?
