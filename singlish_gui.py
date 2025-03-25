import tkinter as tk
from tkinter import ttk, messagebox
from singlish import transliterate
import time

class TransliteratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("English to Sinhala Transliterator")
        self.root.geometry("800x600")
        
        # Add performance optimization variables
        self.last_keypress = 0
        self.debounce_delay = 0.3  # 300ms delay
        self.update_pending = False
        self.last_text = ""  # Store the last English text to avoid redundant updates
        self.update_job = None  # Store the ID of the scheduled update job
        
        # Configure style
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 11))
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Create guidance panel (initially hidden)
        self.guidance_frame = ttk.LabelFrame(main_frame, text="Letter Guide", padding="10")
        self.guidance_visible = False
        
        # Create guidance content with performance optimizations
        guidance_text = tk.Text(main_frame, height=10, width=40, font=('Arial', 11), wrap=tk.WORD)
        guidance_text.insert("1.0", """Common Letter Mappings:

        Vowels:
        a → අ    aa → ආ    A → ඇ    Ae → ඈ
        i → ඉ    ii → ඊ
        u → උ    uu → ඌ
        e → එ    ee → ඒ
        o → ඔ    oo → ඕ

        Consonants:
        k → ක්    g → ග්    ch → ච්
        t → ට්    d → ඩ්    n → න්
        p → ප්    b → බ්    m → ම්
        y → ය්    r → ර්    l → ල්
        w → ව්    s → ස්    h → හ්""")
        guidance_text.config(state='disabled')
        self.guidance_text = guidance_text
        
        # Add toggle button for guidance panel
        self.toggle_btn = ttk.Button(main_frame, text="Show Guide", command=self.toggle_guidance)
        self.toggle_btn.grid(row=0, column=1, sticky=tk.E, pady=(0, 5))
        
        # Create labels
        ttk.Label(main_frame, text="Type English Text:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Label(main_frame, text="සිංහල අකුරු:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        
        # Create text areas with performance optimizations
        # English text area
        english_frame = ttk.Frame(main_frame)
        english_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.english_text = tk.Text(english_frame, height=8, width=60, font=('Arial', 12), wrap=tk.WORD)
        english_scrollbar = ttk.Scrollbar(english_frame, orient=tk.VERTICAL, command=self.english_text.yview)
        self.english_text.configure(yscrollcommand=english_scrollbar.set)
        
        self.english_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        english_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sinhala text area with optimizations
        sinhala_frame = ttk.Frame(main_frame)
        sinhala_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.sinhala_text = tk.Text(sinhala_frame, height=8, width=60, font=('Iskoola Pota', 14), wrap=tk.WORD)
        sinhala_scrollbar = ttk.Scrollbar(sinhala_frame, orient=tk.VERTICAL, command=self.sinhala_text.yview)
        self.sinhala_text.configure(yscrollcommand=sinhala_scrollbar.set)
        
        self.sinhala_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sinhala_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Make Sinhala text area read-only
        self.sinhala_text.config(state='disabled')
        
        # Create buttons frame  
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Add buttons
        ttk.Button(button_frame, text="Clear", command=self.clear_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Copy Sinhala", command=self.copy_sinhala).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Help", command=self.show_help).pack(side=tk.LEFT, padx=5)
        
        # Bind the text change event with debouncing
        self.english_text.bind('<KeyRelease>', self.schedule_update)
        
        # Add help text at the bottom
        help_text = "Type English letters to see Sinhala text. Use capital letters for special characters."
        ttk.Label(main_frame, text=help_text, font=('Arial', 10, 'italic')).grid(
            row=7, column=0, columnspan=2, pady=(10, 0), sticky=tk.W
        )
        
        # Configure text widget options for better performance
        self.english_text.configure(maxundo=0, autoseparators=False, undo=False)
        self.sinhala_text.configure(maxundo=0, autoseparators=False, undo=False)
    
    def schedule_update(self, event=None):
        """Schedule the text update with debouncing"""
        if self.update_job:
            self.root.after_cancel(self.update_job)  # Cancel any pending update
        self.update_job = self.root.after(int(self.debounce_delay * 1000), self.update_text)
    
    def update_text(self):
        """Update the Sinhala text with debouncing"""
        self.update_job = None  # Clear the scheduled job ID
        english = self.english_text.get("1.0", tk.END).strip()
        
        # Only update if the text has changed
        if english != self.last_text:
            self.last_text = english
            sinhala = transliterate(english)
            
            # Update Sinhala text area efficiently
            self.sinhala_text.config(state='normal')
            self.sinhala_text.delete("1.0", tk.END)
            self.sinhala_text.insert("1.0", sinhala)
            self.sinhala_text.config(state='disabled')
    
    def clear_text(self):
        """Clear both text areas efficiently"""
        self.english_text.delete("1.0", tk.END)
        self.sinhala_text.config(state='normal')
        self.sinhala_text.delete("1.0", tk.END)
        self.sinhala_text.config(state='disabled')
        self.last_text = ""  # Reset the last text
        if self.update_job:
            self.root.after_cancel(self.update_job)  # Cancel any pending update
            self.update_job = None
    
    def copy_sinhala(self):
        """Copy Sinhala text to clipboard"""
        sinhala_text = self.sinhala_text.get("1.0", tk.END).strip()
        if sinhala_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(sinhala_text)
            messagebox.showinfo("Success", "Sinhala text copied to clipboard!")
    
    def toggle_guidance(self):
        """Toggle the visibility of the guidance panel efficiently"""
        if self.guidance_visible:
            self.guidance_frame.grid_remove()
            self.toggle_btn.config(text="Show Guide")
            self.guidance_visible = False
        else:
            self.guidance_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
            self.toggle_btn.config(text="Hide Guide")
            self.guidance_visible = True

    def show_help(self):
        """Show help information"""
        help_text = """How to use the Sinhala Transliterator:

1. Basic vowels:
   - a -> අ, aa -> ආ, A -> ඇ, Ae -> ඈ
   - i -> ඉ, ii -> ඊ
   - u -> උ, uu -> ඌ
   - e -> එ, ee -> ඒ
   - o -> ඔ, oo -> ඕ

2. Consonants:
   - k -> ක්, g -> ග්, ch -> ච්
   - t -> ට්, d -> ඩ්
   - n -> න්, p -> ප්, b -> බ්
   - m -> ම්, y -> ය්, r -> ර්
   - l -> ල්, w/v -> ව්, s -> ස්

3. Special combinations:
   - Type 'ga' for ග, 'gi' for ගි
   - Type 'ma' for ම, 'mi' for මි
   - Type 'nda' for ඳ, 'mba' for ඹ

Note: Use capital letters for special characters like 'A' for ඇ."""
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Transliterator Help")
        help_window.geometry("500x600")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, font=('Arial', 12), padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.config(state='disabled')

def main():
    root = tk.Tk()
    app = TransliteratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
