import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from collections import Counter
import math

# Professional Color Scheme
COLORS = {
    'primary_bg': '#1a1d2e',
    'secondary_bg': '#16213e',
    'accent_blue': '#0f4c75',
    'accent_teal': '#3282b8',
    'light_bg': '#f5f7fa',
    'text_dark': '#2c3e50',
    'text_light': '#ecf0f1',
    'success': '#27ae60',
    'warning': '#f39c12',
    'highlight': '#3498db',
    'border': '#dfe6e9',
    'step_bg': '#e8f4f8',
    'header_bg': '#34495e',
    'tree_node': '#5dade2',
    'tree_line': '#34495e'
}

class ShannonFanoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shannon-Fano Coding Visualizer")
        self.root.geometry("1400x800")
        self.root.configure(bg=COLORS['primary_bg'])

        self.symbols = []
        self.codes = {}
        self.steps_data = []

        self.create_layout()

    def create_layout(self):
        main_container = tk.Frame(self.root, bg=COLORS['primary_bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # LEFT PANEL
        left_panel = tk.Frame(main_container, bg=COLORS['secondary_bg'], relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=0, ipadx=20, ipady=20)

        left_header = tk.Label(left_panel, text="INPUT SECTION",
                              font=('Segoe UI', 16, 'bold'),
                              bg=COLORS['header_bg'], fg=COLORS['text_light'],
                              pady=10)
        left_header.pack(fill=tk.X, padx=5, pady=(5, 15))

        msg_label = tk.Label(left_panel, text="Enter Message:",
                            font=('Segoe UI', 12, 'bold'),
                            bg=COLORS['secondary_bg'], fg=COLORS['text_light'])
        msg_label.pack(anchor=tk.W, padx=15, pady=(10, 5))

        self.message_entry = tk.Text(left_panel, height=8, width=35,
                                     font=('Consolas', 11),
                                     bg='#ffffff', fg=COLORS['text_dark'],
                                     relief=tk.SOLID, borderwidth=1,
                                     wrap=tk.WORD)
        self.message_entry.pack(padx=15, pady=5)

        info_frame = tk.LabelFrame(left_panel, text="Algorithm Steps",
                                  font=('Segoe UI', 10, 'bold'),
                                  bg=COLORS['secondary_bg'], fg=COLORS['text_light'],
                                  relief=tk.GROOVE, borderwidth=2)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        info_text = "1. Calculate frequencies\n2. Compute probabilities\n3. Sort by probability\n4. Divide into equal groups\n5. Assign binary codes\n6. Generate final codes\n7. Encode message"
        info_display = tk.Label(info_frame, text=info_text,
                               font=('Segoe UI', 10),
                               bg=COLORS['secondary_bg'], fg=COLORS['text_light'],
                               justify=tk.LEFT, anchor=tk.W)
        info_display.pack(padx=10, pady=10, fill=tk.BOTH)

        self.generate_btn = tk.Button(left_panel, text="⚡ GENERATE CODES",
                                     command=self.generate_shannon_codes,
                                     font=('Segoe UI', 13, 'bold'),
                                     bg=COLORS['success'], fg='white',
                                     activebackground=COLORS['highlight'],
                                     relief=tk.RAISED, borderwidth=3,
                                     padx=20, pady=12, cursor='hand2')
        self.generate_btn.pack(pady=20, padx=15)

        clear_btn = tk.Button(left_panel, text="🗑 Clear All",
                             command=self.clear_all,
                             font=('Segoe UI', 10),
                             bg=COLORS['warning'], fg='white',
                             relief=tk.RAISED, borderwidth=2,
                             padx=15, pady=8)
        clear_btn.pack(pady=(0, 15), padx=15)

        # RIGHT PANEL
        right_panel = tk.Frame(main_container, bg=COLORS['light_bg'],
                              relief=tk.RAISED, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        right_header = tk.Label(right_panel, text="VISUALIZATION & RESULTS",
                               font=('Segoe UI', 16, 'bold'),
                               bg=COLORS['header_bg'], fg=COLORS['text_light'],
                               pady=10)
        right_header.pack(fill=tk.X, padx=5, pady=(5, 10))

        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'))

        # Tab 1: Step-by-step visualization
        self.steps_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.steps_frame, text='📊 Step-by-Step Process')

        self.steps_canvas = tk.Canvas(self.steps_frame, bg='white')
        steps_scrollbar = tk.Scrollbar(self.steps_frame, orient=tk.VERTICAL, command=self.steps_canvas.yview)
        self.steps_canvas.configure(yscrollcommand=steps_scrollbar.set)
        steps_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.steps_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.steps_inner_frame = tk.Frame(self.steps_canvas, bg='white')
        self.steps_canvas.create_window((0, 0), window=self.steps_inner_frame, anchor=tk.NW)

        # Tab 2: Tree visualization
        self.tree_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.tree_frame, text='🌳 Tree Diagram')

        self.tree_canvas = tk.Canvas(self.tree_frame, bg='white', scrollregion=(0, 0, 1000, 800))
        tree_scroll_y = tk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree_canvas.yview)
        tree_scroll_x = tk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree_canvas.xview)
        self.tree_canvas.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)

        # Tab 3: Final results
        self.results_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.results_frame, text='✅ Final Results')
        self.results_text = scrolledtext.ScrolledText(
            self.results_frame, font=('Consolas', 11),
            bg='#f8f9fa', fg=COLORS['text_dark'],
            relief=tk.FLAT, borderwidth=0, padx=15, pady=15)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def shannon_fano_recursive(self, symbols_probs, prefix=''):
        if len(symbols_probs) == 1:
            symbol, prob = symbols_probs[0]
            self.codes[symbol] = prefix if prefix else '0'
            return

        total = sum(prob for _, prob in symbols_probs)
        cumsum = 0
        split_idx = 0
        min_diff = float('inf')
        for i in range(len(symbols_probs) - 1):
            cumsum += symbols_probs[i][1]
            diff = abs(cumsum - (total - cumsum))
            if diff < min_diff:
                min_diff = diff
                split_idx = i + 1

        left_group = symbols_probs[:split_idx]
        right_group = symbols_probs[split_idx:]

        step_info = {
            'left': left_group,
            'right': right_group,
            'prefix': prefix
        }
        self.steps_data.append(step_info)

        self.shannon_fano_recursive(left_group, prefix + '0')
        self.shannon_fano_recursive(right_group, prefix + '1')

    def generate_shannon_codes(self):
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Input Error", "Please enter a message!")
            return
        self.codes = {}
        self.steps_data = []
        freq_counter = Counter(message)
        total_chars = len(message)
        self.symbols = [(char, count/total_chars, count) for char, count in freq_counter.items()]
        self.symbols.sort(key=lambda x: x[1], reverse=True)
        symbols_probs = [(char, prob) for char, prob, _ in self.symbols]
        self.shannon_fano_recursive(symbols_probs)
        self.display_steps()
        self.draw_tree()
        self.display_final_results(message)

    def display_steps(self):
        for widget in self.steps_inner_frame.winfo_children():
            widget.destroy()

        header = tk.Label(self.steps_inner_frame,
                         text="Shannon-Fano Encoding Process",
                         font=('Segoe UI', 14, 'bold'),
                         bg='white', fg=COLORS['text_dark'])
        header.pack(pady=10)

        step1_frame = tk.LabelFrame(self.steps_inner_frame,
                                   text="Step 1: Symbol Frequencies & Probabilities",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=COLORS['step_bg'], fg=COLORS['text_dark'],
                                   relief=tk.RIDGE, borderwidth=2)
        step1_frame.pack(fill=tk.X, padx=20, pady=10)

        table_text = "Symbol | Frequency | Probability\n" + "-"*50 + "\n"
        for char, prob, count in self.symbols:
            display_char = repr(char) if char in [' ', '\n', '\t'] else char
            table_text += f"  {display_char:^6} | {count:^9} | {prob:^10.4f}\n"
        table_label = tk.Label(step1_frame, text=table_text,
                              font=('Consolas', 10), bg=COLORS['step_bg'],
                              fg=COLORS['text_dark'], justify=tk.LEFT)
        table_label.pack(padx=15, pady=10, anchor=tk.W)

        step2_frame = tk.LabelFrame(self.steps_inner_frame,
                                   text="Step 2: Recursive Division & Code Assignment",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=COLORS['step_bg'], fg=COLORS['text_dark'],
                                   relief=tk.RIDGE, borderwidth=2)
        step2_frame.pack(fill=tk.X, padx=20, pady=10)

        for i, step in enumerate(self.steps_data, 1):
            step_info = f"Division {i}:\n"
            step_info += f"  Left (0):  {[s for s, p in step['left']]}\n"
            step_info += f"  Right (1): {[s for s, p in step['right']]}\n"
            step_label = tk.Label(step2_frame, text=step_info,
                                 font=('Consolas', 9), bg='white',
                                 fg=COLORS['text_dark'], justify=tk.LEFT,
                                 relief=tk.SOLID, borderwidth=1)
            step_label.pack(padx=10, pady=5, fill=tk.X)

        step3_frame = tk.LabelFrame(self.steps_inner_frame,
                                   text="Step 3: Generated Codes",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=COLORS['step_bg'], fg=COLORS['text_dark'],
                                   relief=tk.RIDGE, borderwidth=2)
        step3_frame.pack(fill=tk.X, padx=20, pady=10)
        codes_text = "Symbol | Shannon-Fano Code | Length\n" + "-"*50 + "\n"
        for char in sorted(self.codes.keys()):
            display_char = repr(char) if char in [' ', '\n', '\t'] else char
            codes_text += f"  {display_char:^6} | {self.codes[char]:^17} | {len(self.codes[char]):^6}\n"
        codes_label = tk.Label(step3_frame, text=codes_text,
                              font=('Consolas', 10), bg='white',
                              fg=COLORS['success'], justify=tk.LEFT,
                              relief=tk.SOLID, borderwidth=1)
        codes_label.pack(padx=15, pady=10)

        self.steps_inner_frame.update_idletasks()
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))

    def draw_tree(self):
        self.tree_canvas.delete("all")
        if not self.codes:
            return
        max_depth = max(len(code) for code in self.codes.values())
        num_leaves = len(self.codes)
        width = max(800, num_leaves * 80)
        height = max(600, max_depth * 100 + 100)
        self.tree_canvas.configure(scrollregion=(0, 0, width, height))
        start_x = width // 2
        start_y = 50
        self.draw_node(start_x, start_y, "Root", COLORS['highlight'])
        self.draw_tree_recursive(start_x, start_y, width // 4, 100, '',
                                 [(char, prob) for char, prob, _ in self.symbols])

    def draw_tree_recursive(self, x, y, dx, dy, prefix, symbols_probs):
        if len(symbols_probs) == 1:
            char, _ = symbols_probs[0]
            display_char = repr(char) if char in [' ', '\n', '\t'] else char
            label = f"{display_char}\n{self.codes[char]}"
            self.draw_node(x, y, label, COLORS['success'])
            return
        total = sum(prob for _, prob in symbols_probs)
        cumsum = 0
        split_idx = 0
        min_diff = float('inf')
        for i in range(len(symbols_probs) - 1):
            cumsum += symbols_probs[i][1]
            diff = abs(cumsum - (total - cumsum))
            if diff < min_diff:
                min_diff = diff
                split_idx = i + 1
        left_group = symbols_probs[:split_idx]
        right_group = symbols_probs[split_idx:]
        left_x = x - dx
        left_y = y + dy
        self.tree_canvas.create_line(x, y + 20, left_x, left_y - 20,
                                     fill=COLORS['tree_line'], width=2, arrow=tk.LAST)
        self.tree_canvas.create_text((x + left_x) // 2, (y + left_y) // 2,
                                     text='0', font=('Segoe UI', 10, 'bold'),
                                     fill=COLORS['success'])
        self.draw_tree_recursive(left_x, left_y, dx // 2, dy, prefix + '0', left_group)
        right_x = x + dx
        right_y = y + dy
        self.tree_canvas.create_line(x, y + 20, right_x, right_y - 20,
                                     fill=COLORS['tree_line'], width=2, arrow=tk.LAST)
        self.tree_canvas.create_text((x + right_x) // 2, (y + right_y) // 2,
                                     text='1', font=('Segoe UI', 10, 'bold'),
                                     fill=COLORS['warning'])
        self.draw_tree_recursive(right_x, right_y, dx // 2, dy, prefix + '1', right_group)

    def draw_node(self, x, y, text, color):
        radius = 25
        self.tree_canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                     fill=color, outline=COLORS['text_dark'], width=2)
        self.tree_canvas.create_text(x, y, text=text, font=('Segoe UI', 9, 'bold'),
                                     fill='white', width=40)

    def display_final_results(self, message):
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, "="*70 + "\n", 'header')
        self.results_text.insert(tk.END, "SHANNON-FANO ENCODING RESULTS\n", 'header')
        self.results_text.insert(tk.END, "="*70 + "\n\n", 'header')
        self.results_text.insert(tk.END, "Original Message:\n", 'bold')
        self.results_text.insert(tk.END, f"{message}\n\n", 'normal')
        self.results_text.insert(tk.END, "Code Table:\n", 'bold')
        self.results_text.insert(tk.END, "-"*70 + "\n", 'normal')
        self.results_text.insert(tk.END, f"{'Symbol':<10} {'Code':<20} {'Length':<10}\n", 'bold')
        self.results_text.insert(tk.END, "-"*70 + "\n", 'normal')
        for char in sorted(self.codes.keys()):
            display_char = repr(char) if char in [' ', '\n', '\t'] else char
            self.results_text.insert(tk.END,
                f"{display_char:<10} {self.codes[char]:<20} {len(self.codes[char]):<10}\n",
                'normal')
        encoded = ''.join(self.codes[char] for char in message)
        self.results_text.insert(tk.END, "\n" + "="*70 + "\n", 'normal')
        self.results_text.insert(tk.END, "Encoded Message:\n", 'bold')
        self.results_text.insert(tk.END, f"{encoded}\n\n", 'code')
        original_bits = len(message) * 8
        compressed_bits = len(encoded)
        compression_ratio = (1 - compressed_bits / original_bits) * 100
        avg_length = sum(len(self.codes[c]) for c in message) / len(message)
        probs = [prob for _, prob, _ in self.symbols]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        self.results_text.insert(tk.END, "Statistics:\n", 'bold')
        self.results_text.insert(tk.END, "-"*70 + "\n", 'normal')
        self.results_text.insert(tk.END, f"Original size:        {original_bits} bits\n", 'normal')
        self.results_text.insert(tk.END, f"Compressed size:      {compressed_bits} bits\n", 'normal')
        self.results_text.insert(tk.END, f"Compression ratio:    {compression_ratio:.2f}%\n", 'normal')
        self.results_text.insert(tk.END, f"Average code length:  {avg_length:.3f} bits\n", 'normal')
        self.results_text.insert(tk.END, f"Entropy:              {entropy:.3f} bits\n", 'normal')
        self.results_text.insert(tk.END, f"Efficiency:           {(entropy/avg_length)*100:.2f}%\n", 'normal')
        self.results_text.tag_config('header', font=('Segoe UI', 13, 'bold'),
                                     foreground=COLORS['highlight'])
        self.results_text.tag_config('bold', font=('Segoe UI', 11, 'bold'),
                                     foreground=COLORS['text_dark'])
        self.results_text.tag_config('normal', font=('Consolas', 10),
                                     foreground=COLORS['text_dark'])
        self.results_text.tag_config('code', font=('Consolas', 10),
                                     foreground=COLORS['success'], background='#e8f8f5')

    def clear_all(self):
        self.message_entry.delete("1.0", tk.END)
        self.codes = {}
        self.steps_data = []
        for widget in self.steps_inner_frame.winfo_children():
            widget.destroy()
        self.tree_canvas.delete("all")
        self.results_text.delete('1.0', tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShannonFanoGUI(root)
    root.mainloop()
