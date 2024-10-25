import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Chào mừng",
    page_icon="✍",
)



logo = Image.open("hvktmm.png")
col1, col2, col3 = st.columns(3)
col2.image(logo, width=250)

st.write(f"# Chào mừng đến với hệ thống ")

st.sidebar.success("Lựa chọn dịch vụ cần sử dụng")

st.markdown(
        """
        Đây là đồ án tốt nghiệp của Học viên TC24

        **👈 Lựa chọn các dịch vụ từ thanh trượt** để sử dụng các dịch vụ tương ứng.
    """
    )
 


