# Week 7/security_analyzer.py
import tkinter as tk
from tkinter import messagebox, ttk
import collections

# Week 7 standard evaluation S-Box
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

class SecurityAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Cipher Security Analyzer")
        self.root.geometry("680x580")
        self.root.configure(bg="#1E1E24")
        
        # Style layout configuration
        style = ttk.Style()
        style.theme_use("clam")
        
        # Main Window Header
        title_lbl = tk.Label(
            root, text="CHALLENGE TASK: SECURITY ANALYZER", 
            font=("Courier New", 16, "bold"), fg="#00FF66", bg="#1E1E24"
        )
        title_lbl.pack(pady=12)
        
        # Control Input Frame
        input_frame = tk.LabelFrame(root, text=" Diagnostic Settings ", fg="#FFFFFF", bg="#1E1E24", font=("Arial", 10, "bold"))
        input_frame.pack(fill="x", padx=15, pady=5)
        
        tk.Label(input_frame, text="Plaintext Byte (Hex, e.g., 4A):", fg="#A0A0A0", bg="#1E1E24").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.pt_entry = tk.Entry(input_frame, width=10, font=("Arial", 10), bg="#2D2D34", fg="#FFFFFF", insertbackground="white")
        self.pt_entry.insert(0, "4A")
        self.pt_entry.grid(row=0, column=1, padx=5, pady=8)
        
        tk.Label(input_frame, text="Key Token (Hex, e.g., F5):", fg="#A0A0A0", bg="#1E1E24").grid(row=0, column=2, padx=5, pady=8, sticky="w")
        self.key_entry = tk.Entry(input_frame, width=10, font=("Arial", 10), bg="#2D2D34", fg="#FFFFFF", insertbackground="white")
        self.key_entry.insert(0, "F5")
        self.key_entry.grid(row=0, column=3, padx=5, pady=8)
        
        # Action Trigger Button
        run_btn = tk.Button(
            root, text="⚡ RUN COMPREHENSIVE ANALYSIS", font=("Arial", 11, "bold"),
            bg="#00FF66", fg="#1E1E24", activebackground="#00CC52", command=self.execute_analysis
        )
        run_btn.pack(pady=10, fill="x", padx=15)
        
        # Display Console Area
        log_frame = tk.LabelFrame(root, text=" Security Metrics & Statistical Report ", fg="#FFFFFF", bg="#1E1E24", font=("Arial", 10, "bold"))
        log_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.log_display = tk.Text(log_frame, bg="#0A0A0F", fg="#00FF66", font=("Courier New", 10), wrap="none", insertbackground="white")
        self.log_display.pack(fill="both", expand=True, padx=5, pady=5)

    def run_spn_round(self, data, key):
        """Helper to run a structural byte cipher round execution."""
        mixed = data ^ key
        high = S_BOX[(mixed >> 4) & 0x0F]
        low = S_BOX[mixed & 0x0F]
        return (high << 4) | low

    def execute_analysis(self):
        try:
            pt = int(self.pt_entry.get(), 16) & 0xFF
            key = int(self.key_entry.get(), 16) & 0xFF
        except ValueError:
            messagebox.showerror("Input Error", "Please provide valid 8-bit Hex codes.")
            return
            
        self.log_display.delete("1.0", tk.END)
        
        # 1. Evaluate Avalanche Effect Testing
        base_cipher = self.run_spn_round(pt, key)
        flipped_pt = pt ^ 0x01 # Flip exactly one bit in input text
        flipped_cipher = self.run_spn_round(flipped_pt, key)
        
        bit_diff = base_cipher ^ flipped_cipher
        bits_changed = bin(bit_diff).count('1')
        avalanche_percentage = (bits_changed / 8.0) * 100
        
        # 2. Complete Global Difference Analysis
        input_diff = 0x02
        pt2 = pt ^ input_diff
        ct1 = self.run_spn_round(pt, key)
        ct2 = self.run_spn_round(pt2, key)
        output_diff = ct1 ^ ct2
        
        # 3. Frequency Distribution Mapping Profile
        diff_pool = []
        for x in range(256):
            diff_pool.append(self.run_spn_round(x, key) ^ self.run_spn_round(x ^ 0x01, key))
        freq_map = collections.Counter(diff_pool)
        
        # 4. Display Results Automatically & Report Summary Formatting
        self.log_display.insert(tk.END, "=================================================================\n")
        self.log_display.insert(tk.END, "              BLOCK CIPHER SECURITY ANALYSIS REPORT              \n")
        self.log_display.insert(tk.END, "=================================================================\n\n")
        
        self.log_display.insert(tk.END, f"[+] AVALANCHE EFFECT METRICS:\n")
        self.log_display.insert(tk.END, f"    - Original Cipher Text  : {hex(base_cipher).upper()} ({bin(base_cipher)[2:].zfill(8)})\n")
        self.log_display.insert(tk.END, f"    - Flipped Plaintext (1b): {hex(flipped_pt).upper()} ({bin(flipped_pt)[2:].zfill(8)})\n")
        self.log_display.insert(tk.END, f"    - Flipped Cipher Text   : {hex(flipped_cipher).upper()} ({bin(flipped_cipher)[2:].zfill(8)})\n")
        self.log_display.insert(tk.END, f"    - Total Bits Mutated    : {bits_changed} out of 8 bits\n")
        self.log_display.insert(tk.END, f"    - Avalanche Strength    : {avalanche_percentage:.2f}%\n\n")
        
        self.log_display.insert(tk.END, f"[+] XOR DIFFERENCE ANALYSIS:\n")
        self.log_display.insert(tk.END, f"    - Controlled Input ΔX   : {hex(input_diff).upper()}\n")
        self.log_display.insert(tk.END, f"    - Resulting Output ΔY   : {hex(output_diff).upper()}\n\n")
        
        self.log_display.insert(tk.END, f"[+] FREQUENCY DISTRIBUTION TOP SAMPLES (Text Graphical):\n")
        for diff_val, count in freq_map.most_common(3):
            bar = "■" * (count // 4)
            self.log_display.insert(tk.END, f"    - Out Diff {hex(diff_val).upper():<5} : Count: {count:<3} {bar}\n")
            
        self.log_display.insert(tk.END, "\n=================================================================\n")
        self.log_display.insert(tk.END, " ✔️ SECURITY EVALUATION TASK COMPLETED SUCCESSFULY\n")
        self.log_display.insert(tk.END, "=================================================================\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityAnalyzerApp(root)
    root.mainloop()