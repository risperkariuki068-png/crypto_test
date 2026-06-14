# week6/aes_simulator.py
import tkinter as tk
from tkinter import messagebox

# Standard AES-inspired 4-bit S-Box mapping table
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

# Inverse S-Box mapping table for decryption logic
INV_S_BOX = {v: k for k, v in S_BOX.items()}

# P-Box permutation index vectors
P_BOX = [2, 0, 3, 1]
INV_P_BOX = [1, 3, 0, 2]  # Unscrambles the P-Box positions

def substitute_byte(state_byte, inv=False):
    box = INV_S_BOX if inv else S_BOX
    left = box[(state_byte >> 4) & 0x0F]
    right = box[state_byte & 0x0F]
    return (left << 4) | right

def permute_byte(state_byte, inv=False):
    box = INV_P_BOX if inv else P_BOX
    def run_pbox(nibble):
        bin_str = bin(nibble)[2:].zfill(4)
        permuted = [''] * 4
        for orig, target in enumerate(box):
            permuted[target] = bin_str[orig]
        return int("".join(permuted), 2)
    return (run_pbox((state_byte >> 4) & 0x0F) << 4) | run_pbox(state_byte & 0x0F)

def run_cipher(input_byte, keys, rounds, decrypt=False):
    state = input_byte
    if not decrypt:
        # Encryption Pipeline
        for r in range(rounds):
            state ^= keys[r]  # Key Mixing
            state = substitute_byte(state)  # Substitution
            if r < rounds - 1:
                state = permute_byte(state)  # Permutation
        state ^= keys[-1]
    else:
        # Decryption Pipeline (Run exactly in reverse)
        state ^= keys[-1]
        for r in range(rounds - 1, -1, -1):
            if r < rounds - 1:
                state = permute_byte(state, inv=True)
            state = substitute_byte(state, inv=True)
            state ^= keys[r]
    return state

class AESSimulatorApp:
    def __init__(self,root):
        # Setting up the main window properties
        self.root = root
        self.root.title("Mini AES-Inspired Simulator")
        self.root.geometry("480x520")
        self.root.configure(bg="#1e1e2e")
        
        # Title Label
        tk.Label(root, text="AES-Inspired Encryption Simulator", font=("Arial", 14, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack(pady=10)
        
        # Inputs Section Frame
        frame = tk.Frame(root, bg="#1e1e2e")
        frame.pack(pady=10)
        
        tk.Label(frame, text="Plaintext / Ciphertext Byte (Hex, e.g., 4A):", fg="#a6adc8", bg="#1e1e2e").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_input = tk.Entry(frame, width=10, font=("Courier", 12))
        self.txt_input.insert(0, "4A")
        self.txt_input.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Custom 8-Bit Key (Hex, e.g., F5):", fg="#a6adc8", bg="#1e1e2e").grid(row=1, column=0, sticky="w", pady=5)
        self.txt_key = tk.Entry(frame, width=10, font=("Courier", 12))
        self.txt_key.insert(0, "F5")
        self.txt_key.grid(row=1, column=1, pady=5, padx=10)
        
        # Operation Control Buttons
        btn_frame = tk.Frame(root, bg="#1e1e2e")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Encrypt 🔒", command=lambda: self.process(decrypt=False), bg="#a6e3a1", fg="#11111b", font=("Arial", 11, "bold"), width=12).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Decrypt 🔓", command=lambda: self.process(decrypt=True), bg="#f38ba8", fg="#11111b", font=("Arial", 11, "bold"), width=12).grid(row=0, column=1, padx=10)
        
        # Execution Trace Output Log
        tk.Label(root, text="Execution Trace / Security Analysis Log:", fg="#a6adc8", bg="#1e1e2e").pack(anchor="w", padx=25)
        self.log_display = tk.Text(root, width=52, height=15, bg="#11111b", fg="#a6e3a1", font=("Courier", 10), bd=0, padx=10, pady=10)
        self.log_display.pack(pady=5)
        
    def process(self, decrypt):
        try:
            val = int(self.txt_input.get().strip(), 16)
            master_key = int(self.txt_key.get().strip(), 16)
        except ValueError:
            messagebox.showerror("Format Error", "Please verify inputs are valid hexadecimal values!")
            return
            
        ROUNDS = 2
        # Round Key Generation Schedule
        round_keys = [master_key, (master_key ^ 0xAA) & 0xFF, (master_key ^ 0x55) & 0xFF]
        
        self.log_display.delete("1.0", tk.END)
        mode_str = "DECRYPTION" if decrypt else "ENCRYPTION"
        self.log_display.insert(tk.END, f"=== STARTING {mode_str} PROCESS ===\n")
        self.log_display.insert(tk.END, f"Input Data State : {hex(val).upper()} ({bin(val)[2:].zfill(8)})\n")
        self.log_display.insert(tk.END, f"Master Key State : {hex(master_key).upper()}\n")
        self.log_display.insert(tk.END, "-" * 40 + "\n")
        
        result = run_cipher(val, round_keys, ROUNDS, decrypt=decrypt)
        
        self.log_display.insert(tk.END, f"[✔️] Key Mixing applied...\n")
        self.log_display.insert(tk.END, f"[✔️] Non-Linear Substitution (S-Box) executed...\n")
        self.log_display.insert(tk.END, f"[✔️] Bit-Level Permutation (P-Box) completed...\n")
        self.log_display.insert(tk.END, "-" * 40 + "\n")
        self.log_display.insert(tk.END, f"FINAL OUTPUT: {hex(result).upper()} ({bin(result)[2:].zfill(8)})\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AESSimulatorApp(root)
    root.mainloop()