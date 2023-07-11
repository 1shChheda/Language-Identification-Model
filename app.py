import tkinter as tk
import customtkinter
import pickle
from tkinter import ttk

cv = pickle.load(open("./model_files/transform.pkl", "rb"))
model = pickle.load(open("./model_files/model.pkl", "rb"))
le = pickle.load(open("./model_files/label_encoder.pkl", "rb"))
ac = pickle.load(open("./model_files/model_accuracy.pkl", "rb"))

def predict(text):
    x = cv.transform([text]).toarray()
    lang = model.predict(x)
    lang = le.inverse_transform(lang)
    return lang[0]

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

class LanguagePredictorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Language Predictor")

        self.label = tk.Label(master, text="Enter Text to Predict Language:", font=("Arial", 14), fg="#333333")
        self.label.pack(pady=10)

        self.text_box = tk.Text(master, height=10, width=50, font=("Arial", 16))
        self.text_box.pack()

        self.button = customtkinter.CTkButton(master, text="Predict", command=self.predict_language, font=("Arial", 14, "bold"))
        self.button.pack(pady=10)

        self.result_frame = ttk.Frame(master)
        self.result_frame.pack()

        self.result_label = tk.Label(self.result_frame, text="", font=("Arial", 16, "italic"), fg="#333333")
        self.result_label.grid()

        self.accuracy_frame = ttk.Frame(master)
        self.accuracy_frame.pack()

        self.accuracy_label = ttk.Label(self.accuracy_frame, text="Model Accuracy: {:.2f}%".format(ac * 100), font=("Arial", 12), foreground="#333333")
        self.accuracy_label.pack(side=tk.LEFT, padx=10)

        self.accuracy_progress = ttk.Progressbar(self.accuracy_frame, length=200, mode="determinate", value=ac * 100)
        self.accuracy_progress.pack(side=tk.LEFT)

        self.master.bind('<Return>', self.predict_language)

    def predict_language(self, event=None):
        text = self.text_box.get("1.0", "end-1c")
        if text.strip() == "":
            self.result_label.grid_remove()
            return
        predicted_language = predict(text)
        self.result_label.config(text=f"Predicted Language: {predicted_language}", font=("Arial", 16, "bold"))
        self.result_label.grid()
        self.text_box.delete("1.0", tk.END)

root = customtkinter.CTk()
my_gui = LanguagePredictorGUI(root)
root.mainloop()