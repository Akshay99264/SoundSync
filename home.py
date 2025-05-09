import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import librosa
import librosa.display
from preprocessingAudio import preprocess_audio
from PESQ import PESQ
from MSE import MSE
from STOI import STOI
from Details import find_details
from extractSpeech import extractSpeech
from WER_CER import WER, CER


class AudioComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Comparison Tool")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

        close_button = tk.Button(root, text="X", command=root.destroy, font=("Arial", 16))
        close_button.place(x=8, y=8)

        self.file1 = None
        self.file2 = None

        # Grid layout for root
        self.root.columnconfigure(0, weight=3)  # Left panel
        self.root.columnconfigure(1, weight=7)  # Right panel
        self.root.rowconfigure(0, weight=1)

        # LEFT FRAME
        self.left_frame = ttk.Frame(self.root, padding=15)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Configure two rows inside left_frame
        self.left_frame.rowconfigure(0, weight=1)   # Small weight for control panel
        self.left_frame.rowconfigure(1, weight=4)   # Larger weight for text display
        self.left_frame.columnconfigure(0, weight=1)

        # CONTROL PANEL (Top small part)
        self.control_frame = ttk.Frame(self.left_frame)
        self.control_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))


        # TEXT DISPLAY PANEL (Bottom big part)
        self.output_frame = ttk.Frame(self.left_frame)
        self.output_frame.grid(row=1, column=0, sticky="nsew")

        # Right Frame (already created)
        self.right_frame = ttk.Frame(self.root, padding=15)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        # Configure grid: 2 rows
        self.right_frame.rowconfigure(0, weight=1)  # Top row with 2 sections
        self.right_frame.rowconfigure(1, weight=1)  # Bottom row with 1 section

        # Configure columns for row 0
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=1)

        # Add two frames to row 0 (split horizontally)
        self.top_left = ttk.Frame(self.right_frame, borderwidth=1, relief="solid")
        self.top_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.top_right = ttk.Frame(self.right_frame, borderwidth=1, relief="solid")
        self.top_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Add tow frame to row 1 spanning both columns
        self.bottom_left = ttk.Frame(self.right_frame, borderwidth=1, relief="solid")
        self.bottom_left.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)   # Right Frame (70%) divided into 3 rows
        
        self.bottom_right = ttk.Frame(self.right_frame, borderwidth=1, relief="solid")
        self.bottom_right.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)   # Right Frame (70%) divided into 3 rows

        # self.right_frame = ttk.Frame(self.root, padding=15)
        # self.right_frame.grid(row=0, column=2, sticky="nsew")
        # self.right_frame.rowconfigure(0, weight=2)  # waveform 1 (25%)
        # self.right_frame.rowconfigure(1, weight=2)  # waveform 2 (25%)
        # self.right_frame.columnconfigure(0, weight=2)
        # self.right_frame.columnconfigure(1, weight=2)

        # # Canvas for Waveform 1
        # self.fig1, self.ax1 = plt.subplots(figsize=(6, 2))
        # self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.right_frame)
        # self.canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # # Canvas for Waveform 2
        # self.fig2, self.ax2 = plt.subplots(figsize=(6, 2))
        # self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.right_frame)
        # self.canvas2.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        # Audio Details Area
        # First audio detail box (left)
        self.audio_detail_box_1 = tk.Text(self.right_frame, height=10, wrap='word', font=("Courier", 10))
        self.audio_detail_box_1.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=(10, 0))
        self.audio_detail_box_1.insert("1.0", "Audio 1 details will appear here...\n")
        self.audio_detail_box_1.config(state='disabled')

        # Second audio detail box (right)
        self.audio_detail_box_2 = tk.Text(self.right_frame, height=10, wrap='word', font=("Courier", 10))
        self.audio_detail_box_2.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=(10, 0))
        self.audio_detail_box_2.insert("1.0", "Audio 2 details will appear here...\n")
        self.audio_detail_box_2.config(state='disabled')


        # Result area (text box)
        self.result_box = tk.Text(self.right_frame, height=10, wrap='word', font=("Courier", 10))
        self.result_box.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.result_box.insert("1.0", "Results will appear here after comparison...\n")
        self.result_box.config(state='disabled')

        # Area for notes (text box)
        self.notes_text = tk.Text(self.output_frame, height=10, wrap='word', font=("Courier", 16, "bold"), background="Red")
        self.notes_text.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.notes_text.pack(expand=True, fill='both')
        self.notes_text.insert("1.0", "Important notes\n")
        self.notes_text.config(state='disabled')


        #Area for details section (text box)
        self.parameter_detail_box = tk.Text(self.right_frame, height=10, wrap='word', font=("Courier", 12, "bold"), background="pink")
        self.parameter_detail_box.grid(row=1, column=1, sticky="nsew", pady=(10, 0))
        self.parameter_detail_box.insert("1.0", "Important notes\n")
        self.parameter_detail_box.config(state='disabled')

        self.displayNotes()

        ttk.Label(self.control_frame, text="Audio File 1:", font=("Arial", 10, "bold")).pack(anchor='w', pady=(0, 5))
        ttk.Button(self.control_frame, text="Browse File 1", command=self.load_file1).pack(fill='x', pady=5)

        ttk.Label(self.control_frame, text="Audio File 2:", font=("Arial", 10, "bold")).pack(anchor='w', pady=(15, 5))
        ttk.Button(self.control_frame, text="Browse File 2", command=self.load_file2).pack(fill='x', pady=5)

        ttk.Label(self.control_frame, text="Select Parameter:", font=("Arial", 10, "bold")).pack(anchor='w', pady=(20, 5))
        self.parameters = [
            "All",
            "PESQ (Perceptual Evaluation of Speech Quality)",
            "MSE (Mean Square Error)",
            "STOI (Short-Time Objective Intelligibility)",
            "WER (Word Error Rate), CER (Character Error Rate)"
        ]
        self.selected_param = tk.StringVar(value=self.parameters[0])
        self.dropdown = ttk.Combobox(self.control_frame, values=self.parameters, textvariable=self.selected_param, state="readonly", width=30)
        self.dropdown.pack(fill='x', pady=5)

        ttk.Button(self.control_frame, text="Compare", command=self.compare).pack(fill='x', pady=(30, 5))

    def load_file1(self):
        self.file1 = filedialog.askopenfilename(
            title="Select Audio File 1",
            filetypes=[("Audio Files", "*.wav *.mp3 *.flac"), ("All Files", "*.*")]
        )
        if self.file1:
            self.file1 = preprocess_audio(self.file1)
            file1_details = find_details(self.file1)
            self.displayDetails1(file1_details)
            print(type(file1_details))
            return file1_details
            #self.plot_waveform(self.file1, self.ax1, self.canvas1, "Waveform: File 1")

    def load_file2(self):
        self.file2 = filedialog.askopenfilename(
            title="Select Audio File 2",
            filetypes=[("Audio Files", "*.wav *.mp3 *.flac"), ("All Files", "*.*")]
        )
        if self.file2:
            self.file2 = preprocess_audio(self.file2)
            file2_details = find_details(self.file2)
            self.displayDetails2(file2_details)
            #self.plot_waveform(self.file2, self.ax2, self.canvas2, "Waveform: File 2")

    # def plot_waveform(self, file_path, ax, canvas, title):
    #     try:
    #         y, sr = librosa.load(file_path, sr=None)
    #         ax.clear()
    #         librosa.display.waveshow(y, sr=sr, ax=ax, color='steelblue')
    #         ax.set_title(title)
    #         ax.set_xlabel("Time")
    #         ax.set_ylabel("Amplitude")
    #         canvas.draw()
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Error loading audio: {e}")
            
    def displayDetails1(self, file_details):
        self.audio_detail_box_1.config(state='normal')
        self.audio_detail_box_1.delete("1.0", tk.END)
        self.audio_detail_box_1.insert("1.0", f"Audio 1 details after processing:\n\n")
        for k, v in file_details.items():
            print(k, v)
            self.audio_detail_box_1.insert(tk.END, f"{k}: {v}\n")
        self.audio_detail_box_1.config(state='disabled')
    
    def displayDetails2(self, file_details):
        self.audio_detail_box_2.config(state='normal')
        self.audio_detail_box_2.delete("1.0", tk.END)
        self.audio_detail_box_2.insert("1.0", f"Audio_file 2 details after processing:\n\n")
        for k, v in file_details.items():
            self.audio_detail_box_2.insert(tk.END, f"{k}: {v}\n")
        self.audio_detail_box_2.config(state='disabled')
    
    def displayString(self, input_string, box_details, n):
        box_details.config(state='normal')
        box_details.delete("1.0", tk.END)
        box_details.insert("1.0", f"Audio {n} script will appear here. It will take some time please wait:\n\n")
        box_details.insert(tk.END, input_string)
        box_details.config(state='disabled')

    def displayNotes(self):
        notes = []
        notes.append("Max audio length 25sec")
        notes.append("WER and CER use the Whisper AI model and may take some time to compute, so please be patient.")
        notes.append("WER and CER use Whisper for speech extraction, which may occasionally produce incorrect output.")
        notes.append("Audio details are shown after converting the file to a format suitable for PESQ and other metrics.")
        self.notes_text.config(state='normal')
        self.notes_text.delete("1.0",tk.END)
        self.notes_text.insert("1.0","Important instruction to use this webapp\n\n")
        i = 1
        for rule in notes:
            self.notes_text.insert(tk.END, f"{i}:{rule}\n")
            i = i+1
        self.notes_text.config(state='disabled')

    def displayParameterDetails(self, parameter):
        param_details = {"PESQ (Perceptual Evaluation of Speech Quality)":"Objective metric that predicts the perceived quality of speech by comparing the original and degraded audio; scores range from 1 (bad) to 4.5 (excellent).",
            "MSE (Mean Square Error)":"Measures the average squared difference between original and processed audio signals; lower values indicate higher similarity.",
            "STOI (Short-Time Objective Intelligibility)":"Evaluates how intelligible speech is by estimating the correlation of short-time temporal envelopes; scores range from 0 (unintelligible) to 1 (perfect intelligibility).",
            "WER (Word Error Rate), CER (Character Error Rate)":"WER measures the percentage of incorrectly transcribed words, and CER does the same at the character level; both are used in speech recognition evaluation—lower values are better"
        }
        self.parameter_detail_box.config(state='normal')
        self.parameter_detail_box.delete("1.0",tk.END)
        self.parameter_detail_box.insert("1.0","Details of Paramter\n\n")
        if parameter == "All":
            i = 1
            for k, v in param_details.items():
                self.parameter_detail_box.insert(tk.END,f"{i}-{k}:{v}\n")
                i = i+1
        elif parameter == "PESQ (Perceptual Evaluation of Speech Quality)":
            self.parameter_detail_box.insert(tk.END,f"{parameter}:{param_details[parameter]}\n")
        elif parameter == "MSE (Mean Square Error)":
            self.parameter_detail_box.insert(tk.END,f"{parameter}:{param_details[parameter]}\n")
        elif parameter == "STOI (Short-Time Objective Intelligibility)":
            self.parameter_detail_box.insert(tk.END,f"{parameter}:{param_details[parameter]}\n")
        elif parameter == "WER (Word Error Rate), CER (Character Error Rate)":
            self.parameter_detail_box.insert(tk.END,f"{parameter}:{param_details[parameter]}\n")
        else:
            self.parameter_detail_box.insert(tk.END,"Invalid paramter")

        self.parameter_detail_box.config(state='disabled')
            
        


    def compare(self):
        if not self.file1 or not self.file2:
            messagebox.showerror("Missing File", "Please select both audio files.")
            return
        param = self.selected_param.get()
        results = self.compare_audio(self.file1, self.file2, param)

        self.result_box.config(state='normal')
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert("1.0", f"Comparison Results ({param}):\n\n")
        for k, v in results.items():
            self.result_box.insert(tk.END, f"{k}: {v}\n")
        self.result_box.config(state='disabled')

    def compare_audio(self, file1, file2, parameter):
        self.displayParameterDetails(parameter)
        if parameter == "All":
            pesq_score = PESQ(file1, file2)
            mse_score = MSE(file1, file2)
            stoi_score = STOI(file1, file2)
            extracted_string_1 , extracted_string_2 = extractSpeech(file1, file2)
            #extracted_string_2 = extractSpeech(file2)
            self.displayString(extracted_string_1, self.audio_detail_box_1, 1)
            self.displayString(extracted_string_2,self.audio_detail_box_2, 2)
            wer_score, quality = WER(extracted_string_1, extracted_string_2)
            cer_score = CER(extracted_string_1, extracted_string_2)
            return {
                "PESQ score": pesq_score,
                "MSE score": mse_score,
                "STOI score": stoi_score,
                "WER Score": wer_score,
                "CER Score": cer_score,
                "Quality": quality
            }
        elif parameter == "PESQ (Perceptual Evaluation of Speech Quality)":
            pesq_score = PESQ(file1, file2)
            return {"PESQ score" : pesq_score}
        elif parameter == "MSE (Mean Square Error)":
            mse_score = MSE(file1, file2)
            if mse_score == 'N/A':
                return {"MSE Score": "Error calculating MSE"}
            return {"MSE": mse_score}
        elif parameter == "STOI (Short-Time Objective Intelligibility)":
            stoi_score = STOI(file1, file2)
            return {"STOI": stoi_score}
        elif parameter == "WER (Word Error Rate), CER (Character Error Rate)":
            extracted_string_1 = extractSpeech(file1)
            extracted_string_2 = extractSpeech(file2)
            self.displayString(extracted_string_1, self.audio_detail_box_1, 1)
            self.displayString(extracted_string_2,self.audio_detail_box_2, 2)
            wer_score, quality = WER(extracted_string_1, extracted_string_2)
            cer_score = CER(extracted_string_1, extracted_string_2)
            return {"WER Score": wer_score,
                    "CER Score": cer_score,
                    "Quality": quality}
        else:
            return {"Error": "Unknown parameter"}


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioComparerApp(root)
    root.mainloop()
