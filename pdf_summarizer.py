# pdf_summarizer_demo.py

import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PyPDF2 import PdfReader


# ----------------------------------------------------
# DEMO / FAKE AI SUMMARY ENGINE (lightweight, offline)
# ----------------------------------------------------

def demo_summarizer(text, precision="medium", model="Mistral 7B"):
    """
    This is a lightweight offline summarizer used ONLY for demo.
    It simulates an AI model by selecting sentences based on precision.
    """

    import re

    # Split into sentences using simple regex
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return "No readable text found in the PDF."

    total = len(sentences)

    # Precision determines how much summary we keep
    precision_map = {
        "low": 0.05,     # 5%
        "medium": 0.15,  # 15%
        "high": 0.30     # 30%
    }

    fraction = precision_map.get(precision, 0.15)
    count = max(2, int(total * fraction))
    count = min(total, count)

    # Spread-out selection: pick sentences across the document
    step = max(1, total // count)
    selected = [sentences[i] for i in range(0, total, step)][:count]

    summary = f"Summary using {model} ({precision.title()} Precision):\n\n"
    summary += " ".join(selected)

    return summary


# ----------------------------------------------------
# EXTRACT TEXT FROM PDF
# ----------------------------------------------------

def read_pdf(path):
    """Extract text from a PDF file using PyPDF2."""
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


# ----------------------------------------------------
# MAIN GUI APPLICATION
# ----------------------------------------------------

class PDFSummarizerDemo:

    def __init__(self, root):
        self.root = root
        self.root.title("AI PDF Summarizer")
        self.root.geometry("900x600")

        # Variables
        self.pdf_path = tk.StringVar()
        self.precision = tk.StringVar(value="medium")
        self.model = tk.StringVar(value="Meta-Llama 38B Instruct")
        self.output_path = tk.StringVar()

        self.build_ui()

    # -------------------------------
    # BUILD THE USER INTERFACE
    # -------------------------------
    def build_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.X)

        # PDF File selector
        ttk.Label(frame, text="PDF File:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.pdf_path, width=70).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5)

        # Precision
        pf = ttk.LabelFrame(frame, text="Precision Level")
        pf.grid(row=1, column=0, columnspan=3, pady=10, sticky="w")

        ttk.Radiobutton(pf, text="Low", value="low", variable=self.precision).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(pf, text="Medium", value="medium", variable=self.precision).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(pf, text="High", value="high", variable=self.precision).pack(side=tk.LEFT, padx=10)

        # Model Selection
        mf = ttk.Frame(frame)
        mf.grid(row=2, column=0, columnspan=3, pady=5, sticky="w")

        ttk.Label(mf, text="AI Model: ").pack(side=tk.LEFT)

        model_list = [
            "Meta-Llama 38B Instruct",
            "Mistral 7B Instruct",
            "Gemma 7B Instruct",
        ]

        ttk.Combobox(
            mf,
            values=model_list,
            textvariable=self.model,
            width=30,
            state="readonly"
        ).pack(side=tk.LEFT, padx=10)

        # Summarize Button
        ttk.Button(self.root, text="Summarize", command=self.summarize).pack(pady=10)

        # Output area
        sf = ttk.LabelFrame(self.root, text="Summary Output")
        sf.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_box = tk.Text(sf, wrap=tk.WORD)
        self.output_box.pack(fill=tk.BOTH, expand=True)

    # -------------------------------
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.pdf_path.set(file_path)

    # -------------------------------
    def summarize(self):
        pdf_file = self.pdf_path.get()

        if not pdf_file:
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        # Read PDF
        text = read_pdf(pdf_file)
        if not text:
            messagebox.showerror("Error", "No text found in the PDF.")
            return

        # Generate summary (demo)
        summary = demo_summarizer(
            text,
            precision=self.precision.get(),
            model=self.model.get()
        )

        # Display summary
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, summary)

        # Save summary to a .txt file
        saved_path = self.save_summary(pdf_file, summary)
        self.output_path.set(saved_path)

        messagebox.showinfo("Saved", f"Summary file saved to:\n{saved_path}")

    # -------------------------------
    def save_summary(self, pdf_path, summary):
        folder = os.path.dirname(pdf_path)
        base = os.path.splitext(os.path.basename(pdf_path))[0]

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_file = f"{base}_summary_{timestamp}.txt"

        out_path = os.path.join(folder, output_file)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(summary)

        return out_path


# ----------------------------------------------------
# RUN THE APPLICATION
# ----------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    PDFSummarizerDemo(root)
    root.mainloop()
