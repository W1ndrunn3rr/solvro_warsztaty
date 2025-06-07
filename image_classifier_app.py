import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image, ImageTk
import os

class ImageClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solvro - warsztaty")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')

        self.model_path = "model.pth"
        self.model = None
        self.current_image = None
        self.current_image_path = None
        
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        self.setup_ui()
        self.load_model()
    
    def setup_ui(self):
        title_label = tk.Label(self.root, text="Solvro - warsztaty", 
                              font=("Arial", 18, "bold"), 
                              bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)
        
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)
    
        self.upload_btn = tk.Button(button_frame, text="Wgraj Solvrusia", 
                                   command=self.upload_image,
                                   font=("Arial", 12), 
                                   bg='#4CAF50', fg='white',
                                   padx=20, pady=10)
        self.upload_btn.pack(side=tk.LEFT, padx=10)
        
        self.predict_btn = tk.Button(button_frame, text="Sprawdź Solvrusia", 
                                    command=self.predict_image,
                                    font=("Arial", 12), 
                                    bg='#2196F3', fg='white',
                                    padx=20, pady=10,
                                    state=tk.DISABLED)
        self.predict_btn.pack(side=tk.LEFT, padx=10)
        
        # Frame dla obrazka
        self.image_frame = tk.Frame(self.root, bg='#f0f0f0', relief=tk.SUNKEN, bd=2)
        self.image_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Label dla obrazka
        self.image_label = tk.Label(self.image_frame, 
                                   text="Wybierz Solvrusia do klasyfikacji",
                                   font=("Arial", 12),
                                   bg='#f0f0f0', fg='#666666')
        self.image_label.pack(expand=True)
        
        # Status label
        self.status_label = tk.Label(self.root, text="", 
                                    font=("Arial", 10),
                                    bg='#f0f0f0', fg='#666666')
        self.status_label.pack(pady=10)
    
    def load_model(self):
        try:
            self.status_label.config(text="Ładowanie modelu...")
            self.root.update()
 
            if not os.path.exists(self.model_path):
                messagebox.showerror("Błąd", f"Nie znaleziono pliku modelu: {self.model_path}")
                return
            
            self.model = torch.hub.load('pytorch/vision:v0.10.0', 'googlenet', pretrained=True)
            self.model.fc = nn.Linear(self.model.fc.in_features, 2)
            
            self.model.load_state_dict(torch.load(self.model_path, map_location='cpu'))
            self.model.eval()
            
            self.status_label.config(text="Model załadowany pomyślnie")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się załadować modelu: {str(e)}")
            self.status_label.config(text="Błąd ładowania modelu")
    
    def upload_image(self):
        file_types = [
            ('Obrazy', '*.jpg *.jpeg *.png *.bmp *.tiff *.tif'),
            ('JPEG', '*.jpg *.jpeg'),
            ('PNG', '*.png'),
            ('Wszystkie pliki', '*.*')
        ]
        
        file_path = filedialog.askopenfilename(
            title="Wybierz obraz",
            filetypes=file_types
        )
        
        if file_path:
            try:
                image = Image.open(file_path)
                self.current_image_path = file_path
                
                display_image = image.copy()
                display_image.thumbnail((300, 300), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(display_image)
                
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo 
                
                self.predict_btn.config(state=tk.NORMAL)
                
                self.status_label.config(text=f"Załadowano: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się załadować obrazu: {str(e)}")
    
    def predict_image(self):
        """Przewiduje klasę obrazu"""
        if not self.current_image_path or not self.model:
            messagebox.showwarning("Uwaga", "Najpierw wgraj obraz i upewnij się, że model jest załadowany")
            return
        
        try:
            self.status_label.config(text="Przetwarzanie...")
            self.root.update()
            
            image = Image.open(self.current_image_path)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            input_tensor = self.transform(image).unsqueeze(0)
            
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                predicted_class = torch.argmax(outputs, dim=1).item() 
                confidence = probabilities[0][predicted_class].item()
            
            result_message = f"Przewidywana klasa: {"SOLVRUŚ" if predicted_class else "NIE-SOLVRUŚ"} \nPewność: {confidence:.2%}"
            messagebox.showinfo("Wynik Przewidywania", result_message)
            
            self.status_label.config(text=f"Przewidywanie: klasa {predicted_class} (pewność: {confidence:.2%})")
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas przewidywania: {str(e)}")
            self.status_label.config(text="Błąd przewidywania")

def main():
    root = tk.Tk()
    app = ImageClassifierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
