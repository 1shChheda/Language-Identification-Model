import tkinter as tk
import customtkinter
import pickle

# Load the necessary elements from model_files
cv = pickle.load(open("./model_files/transform.pkl", "rb"))
model = pickle.load(open("./model_files/model.pkl", "rb"))
le = pickle.load(open("./model_files/label_encoder.pkl", "rb"))
ac = pickle.load(open("./model_files/model_accuracy.pkl", "rb"))

# Define the predict function
def predict(text):
    x = cv.transform([text]).toarray()
    lang = model.predict(x)
    lang = le.inverse_transform(lang)
    return lang[0]

# GUI code
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

class LanguagePredictorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Language Predictor")

        self.label = tk.Label(master, text="Enter Text to predict Language:")
        self.label.pack()

        self.text_box = tk.Text(master, height=10, width=50, font=("Helvetica", 16))
        self.text_box.pack()

        self.button = customtkinter.CTkButton(master, text="Predict", command=self.predict_language)
        self.button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()
        progressbar = customtkinter.CTkProgressBar(master=root)
        progressbar.pack(padx=20, pady=10)
        progressbar.set(ac)
        self.result_label.config(text=f"Model Accuracy: {ac * 100}%")

    def predict_language(self):
        text = self.text_box.get("1.0", "end-1c")
        predicted_language = predict(text)
        self.result_label.config(text=f"Predicted language: {predicted_language}\nModel Accuracy: {ac * 100}%")

root = customtkinter.CTk()
my_gui = LanguagePredictorGUI(root)
root.mainloop()