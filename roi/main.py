import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import random
import string
from blake3 import blake3
from time import perf_counter_ns

# Streamlit app
st.title("Thuật toán Băm Blake3 trên Raspberry Pi")

# Nhập liệu từ người dùng
input_data = st.text_area("Nhập dữ liệu để băm:")

# Nút để băm dữ liệu
if st.button("Băm dữ liệu"):
    if input_data:
        # Thực hiện băm bằng Blake3
        start_time = perf_counter_ns()
        hash_object = blake3()
        hash_object.update(input_data.encode('utf-8'))
        hash_value = hash_object.hexdigest()
        elapsed_time = (perf_counter_ns() - start_time) / 1e6

        # Hiển thị kết quả
        st.success(f"Giá trị băm: {hash_value}")
        st.info(f"Thời gian băm: {elapsed_time:.2f} ns")
    else:
        st.warning("Vui lòng nhập dữ liệu để băm.")

# Nút để test 10 case
if st.button("Test 10 case"):
    lengths = [100 * (10 ** i) for i in range(5)]
    times = []
    for length in lengths:
        test_input = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        start_time = perf_counter_ns()
        hash_object = blake3()
        hash_object.update(test_input.encode('utf-8'))
        hash_object.hexdigest()
        elapsed_time = (perf_counter_ns() - start_time) / 1e6
        times.append(elapsed_time)

    # Tạo bảng thống kê
    df = pd.DataFrame({"Độ dài chuỗi (ký tự)": lengths, "Thời gian băm (ns)": times})
    st.table(df)

    # Vẽ biểu đồ
    fig, ax = plt.subplots()
    ax.plot(lengths, times, marker='o')
    ax.set_xlabel('Độ dài chuỗi (ký tự)')
    ax.set_ylabel('Thời gian băm (ns)')
    ax.set_title('Thời gian băm Blake3 với độ dài chuỗi tăng dần')
    st.pyplot(fig)

# Hướng dẫn thêm
st.markdown("### Hướng dẫn sử dụng:")
st.markdown("1. Nhập chuỗi dữ liệu cần băm vào ô nhập liệu.")
st.markdown("2. Nhấn vào nút 'Băm dữ liệu' để xem giá trị băm sử dụng thuật toán Blake3.")
st.markdown("3. Nhấn vào nút 'Test 10 case' để thực hiện băm 10 chuỗi với độ dài tăng dần và xem thời gian băm.")

# Thông tin về Blake3
st.markdown("### Giới thiệu về Blake3:")
st.markdown("Blake3 là thuật toán băm nhanh, bảo mật và có hiệu năng cao, phù hợp với nhiều mục đích khác nhau như kiểm tra tính toàn vẹn của dữ liệu, chữ ký số, v.v.")


st.markdown("Đây là đồ án của Học viên TC24")
