import streamlit as st
import time
import yaml
import streamlit_authenticator as stauth
#from audio_recorder_streamlit import audio_recorder
import sys
import os
import pvd_lib

from Crypto.Cipher import AES
import base64

st.set_page_config(
    page_title="Trích xuất thông tin",
    page_icon="📝",
)

if 1==1:
    st.write(f"# Bạn đang sử dụng dịch vụ")
    #load khoá
    #Trích xuất
    anhgoc_path = "Image"
    key = b'ThisIsASecretKey'  # Cố định khóa (16 bytes)
    def decrypt_message_aes(encrypted_message, key):
        padded_message = encrypted_message + '=' * ((4 - len(encrypted_message) % 4) % 4)
        # Giải mã thông điệp
        encrypted_data = base64.b64decode(padded_message)
        iv = encrypted_data[:16]  # Lấy IV từ đầu của thông điệp đã mã hóa
        encrypted_message = encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
        return decrypted_message
    st.header(f"**Mời bạn chọn file ảnh cần trích xuất**")
    image_path = st.file_uploader("**Chọn chữ ký số**", label_visibility="collapsed")
    if image_path:
        ten_anh = image_path.name
        anhgoc = os.path.join(anhgoc_path, ten_anh)
        pvd = pvd_lib.pvd_lib()
        start = time.time()
        pvd.extract_data(anhgoc, "thongdiepgiai.txt", image_path)
        timegiai= (time.time() - start)
        with open("thongdiepgiai.txt", "r",  encoding='utf-8') as file:
                encrypted_content = file.read()
        st.write("Nội dung đã mã hóa:", encrypted_content)
        try:
            decrypted_content = decrypt_message_aes(encrypted_content, key)
            st.header("Thông điệp trích xuất được là")
            st.code(decrypted_content)
        except Exception as e:
            st.error(f"Lỗi khi giải mã: {str(e)}")  
        os.remove("thongdiepgiai.txt")
