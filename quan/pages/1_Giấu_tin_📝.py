import streamlit as st
import time
import pvd_lib
import os
import random
from Crypto.Cipher import AES
import base64
st.set_page_config(
    page_title="Giấu tin hình ảnh",
    page_icon="📝",
)

if 1==1:
    
    st.write(f"# Bạn đang sử dụng dịch vụ")
    #load khoá
    anhgoc_path = "Image"
     #đường dẫn ảnh
    anhma_path = "EncImage"
    #lấy ngẫu nhiên ảnh
    danh_sach_anh = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]
    so_ngau_nhien = random.randint(1, 7)
    ten_anh = danh_sach_anh[so_ngau_nhien - 1]
    anhgoc = os.path.join(anhgoc_path, ten_anh)
    anhma = os.path.join(anhma_path, ten_anh)
    #ma
    key = b'ThisIsASecretKey'  # Cố định khóa (16 bytes)

    def encrypt_message_aes(message, key):
        # Tạo IV ngẫu nhiên cho mỗi lần mã hóa
        iv = b'0123456789abcdef'  # Sử dụng IV cố định để dễ dàng giải mã
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        # Đưa IV vào đầu thông điệp để giải mã sau này
        return base64.b64encode(iv + encrypted_message).decode('utf-8')



    thongdiep = st.text_input("Nhập thông điệp cần giấu:")
    if thongdiep:
        thongdiep_ma_hoa = encrypt_message_aes(thongdiep, key)

        with open("message.txt", "w", encoding='utf-8') as file:
                    file.write(thongdiep_ma_hoa)
        st.text_area("Thông điệp đã mã hóa:", thongdiep_ma_hoa)

    #mã pvd
        if "message.txt":
            start = time.time()
            pvd = pvd_lib.pvd_lib()
            pvd.embed_data(anhgoc, "message.txt", anhma)
            timema= (time.time() - start)
            os.remove("message.txt")
        #tải ảnh
    #st.header(f"**Chọn file cần ký số**")
    #dulieu = st.file_uploader("**File ký**", label_visibility="collapsed")
        if anhma:
            st.sidebar.success("Giấu tin thành công")
            st.header("Thời gian giấu tin là (s):")
            st.code(timema)
            with open(anhma, mode='rb') as file:
                btn = st.download_button(label='Tải ảnh',
                                            data=file,
                                            file_name=anhma.lstrip("EncImage"))

   