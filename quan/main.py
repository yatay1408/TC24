import random
import glob
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pvd_lib
import codecs
import os
import time
class SteganographyApp:
    def __init__(self, root):
            self.root = root
            self.root.title("Giấu tin với hình ảnh ngẫu nhiên")
            self.root.geometry("800x600")

            #label
            self.giautin_label = tk.Label(root, text="Nhập thông điệp ngẫu nhiên", fg = "black", font = ("Times New Roman", 14, "bold"))
            self.giautin_label.place(x = 10, y = 10)

            #button
            self.giautin_btn = tk.Button(root, text="Giấu tin", command=self.giautin, font = ("Times New Roman", 14))
            self.giautin_btn.place(x = 360, y = 260, width = 81, height = 31)
            
            self.chonanh_btn = tk.Button(root, text="Chọn ảnh", command=self.chonanh, font = ("Times New Roman", 12))
            self.chonanh_btn.place(x = 360, y = 310, width = 81, height = 31)

            self.giaima_btn = tk.Button(root, text="Giải mã", command=self.giaima, font = ("Times New Roman", 14))
            self.giaima_btn.place(x = 360, y = 360, width = 81, height = 31)

            #textbox
            self.thongdiep = tk.Text(root, font = ("Times New Roman", 14))
            self.thongdiep.place(x = 10, y = 50, width = 781, height = 111)
            
            self.anh = tk.Text(root)
            self.anh.place(x = 10, y = 190, width = 341, height = 331)

            self.thongdieptrave = tk.Text(root, font = ("Times New Roman", 14))
            self.thongdieptrave.place(x = 450, y = 190, width = 341, height = 331)
    global anhgoc_path
    anhgoc_path = "Image"
    def giautin(self):   
                #đường dẫn ảnh
                anhma_path = "EncImage"
                #lấy ngẫu nhiên ảnh
                danh_sach_anh = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]
                so_ngau_nhien = random.randint(1, 7)
                ten_anh = danh_sach_anh[so_ngau_nhien - 1]
                anhgoc = os.path.join(anhgoc_path, ten_anh)
                anhma = os.path.join(anhma_path, ten_anh)
            #lấy thông điệp
                message = self.thongdiep.get("1.0","end")
            #lưu dạng txt
                with open("message.txt", "w", encoding='utf-8') as file:
                    file.write(message)
        
                #mã pvd
                start = time.time()
                pvd = pvd_lib.pvd_lib()
                pvd.embed_data(anhgoc, "message.txt", anhma)
                timema= (time.time() - start)

                #in kết quả
                print(timema)
                tk.messagebox.showinfo("Thông báo!","Giấu tin thành công")
                os.startfile(anhma)
                os.remove("message.txt")
             
    def chonanh(self):
          #chọn ảnh
        global image_path
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if image_path:
            # Clear the existing content in the `self.anh` text box
            self.anh.delete(1.0, tk.END)

            # Load the image and resize it to fit within the frame
            image = Image.open(image_path)
            width, height = self.anh.winfo_width(), self.anh.winfo_height()
            aspect_ratio = min(width / image.width, height / image.height)
            new_width = int(image.width * aspect_ratio)
            new_height = int(image.height * aspect_ratio)
            image = image.resize((new_width, new_height))

            # Create a PhotoImage from the resized image
            photo = ImageTk.PhotoImage(image)

            # Create a Label widget to display the image
            image_label = tk.Label(self.anh, image=photo)
            image_label.image = photo

            # Place the Label widget within the `self.anh` text box
            self.anh.window_create(tk.END, window=image_label)
    
    def giaima(self):
        self.thongdieptrave.delete("1.0", tk.END)
        ten_anh = os.path.basename(image_path)
        anhgoc = os.path.join(anhgoc_path, ten_anh)
        pvd = pvd_lib.pvd_lib()
        start = time.time()
        pvd.extract_data(anhgoc, "thongdiepgiai.txt", image_path)
        timegiai= (time.time() - start)
        print(timegiai)
        with open("thongdiepgiai.txt", "r",  encoding='utf-8') as file:
                content = file.read()
        self.thongdieptrave.insert("1.0", content)
        os.remove("thongdiepgiai.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()




