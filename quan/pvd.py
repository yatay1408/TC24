import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pvd_lib

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        
        self.embed_label = tk.Label(root, text="Embed Message:")
        self.embed_label.grid(row=0, column=0, pady=5)
        
        self.embed_btn = tk.Button(root, text="Embed", command=self.embed)
        self.embed_btn.grid(row=0, column=1, pady=5)
        
        self.extract_label = tk.Label(root, text="Extract Message:")
        self.extract_label.grid(row=1, column=0, pady=5)
        
        self.extract_btn = tk.Button(root, text="Extract", command=self.extract)
        self.extract_btn.grid(row=1, column=1, pady=5)
        
    def select_file(self):
        file_path = filedialog.askopenfilename()
        return file_path
        
    def embed(self):
        ref_img_path = self.select_file()
        if ref_img_path:
            s_file_path = self.select_file()
            if s_file_path:
                op_img_path = filedialog.asksaveasfilename(defaultextension=".png")
                if op_img_path:
                    pvd = pvd_lib.pvd_lib()
                    pvd.embed_data(ref_img_path, s_file_path, op_img_path)
                    tk.messagebox.showinfo("Embedding Complete", "Message embedded successfully!")
                    
    def extract(self):
        ref_img_path = self.select_file()
        if ref_img_path:
            s_file_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if s_file_path:
                pvd_img_path = self.select_file()
                if pvd_img_path:
                    pvd = pvd_lib.pvd_lib()
                    pvd.extract_data(ref_img_path, s_file_path, pvd_img_path)
                    tk.messagebox.showinfo("Extraction Complete", "Message extracted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
