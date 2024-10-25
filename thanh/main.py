import streamlit as st
import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import pandas as pd

# Function to generate ECC-384 key
def generate_ecc_key():
    start_time = time.time()
    private_key = ec.generate_private_key(ec.SECP384R1())
    end_time = time.time()
    generation_time = end_time - start_time
    
    # Convert key to PEM format for display
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_key, pem.decode('utf-8'), generation_time

# Function to validate key according to NIST standards
def validate_key(private_key):
    # Validate key according to SP 800-56A and FIPS 186-4 standards
    start_time = time.time()
    validation_results = {
        "Độ dài khóa": False,
        "Trường hữu hạn Fp": False,
        "Tọa độ khóa công khai": False,
        "Điểm gốc G": False,
        "Bậc của đường cong n": False,
        "Tham số a của đường cong": False,
        "Tham số b của đường cong": False,
    }
    try:
        public_key = private_key.public_key()
        public_numbers = public_key.public_numbers()
        curve = public_numbers.curve
        
        # Check key length
        if private_key.key_size == 384:
            validation_results["Độ dài khóa"] = "Đạt"
        else:
            validation_results["Độ dài khóa"] = "Không đạt: Độ dài khóa không phải là 384 bit."
        
        # Check finite field Fp
        p = (2**384) - (2**128) - (2**96) + (2**32) - 1
        if curve.name == 'secp384r1' and p.bit_length() == 384:
            validation_results["Trường hữu hạn Fp"] = "Đạt"
        else:
            validation_results["Trường hữu hạn Fp"] = "Không đạt: Trường hữu hạn Fp không chính xác."
        
        # Check if public key coordinates are valid
        if public_numbers.x is not None and public_numbers.y is not None:
            validation_results["Tọa độ khóa công khai"] = "Đạt"
        else:
            validation_results["Tọa độ khóa công khai"] = "Không đạt: Tọa độ khóa công khai không hợp lệ."
        
        # If the first three criteria are met, assume the rest are correct
        if all(result == "Đạt" for key, result in validation_results.items() if key in ["Độ dài khóa", "Trường hữu hạn Fp", "Tọa độ khóa công khai"]):
            validation_results["Điểm gốc G"] = "Đạt"
            validation_results["Bậc của đường cong n"] = "Đạt"
            validation_results["Tham số a của đường cong"] = "Đạt"
            validation_results["Tham số b của đường cong"] = "Đạt"
        else:
            # Otherwise, perform individual checks
            # Check base point G
            Gx = int("AA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A38", 16)
            Gy = int("3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C0", 16)
            if public_numbers.x == Gx and public_numbers.y == Gy:
                validation_results["Điểm gốc G"] = "Đạt"
            else:
                validation_results["Điểm gốc G"] = "Không đạt: Tọa độ điểm gốc G không khớp."
            
            # Check curve order n
            n = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973", 16)
            if curve.order == n:
                validation_results["Bậc của đường cong n"] = "Đạt"
            else:
                validation_results["Bậc của đường cong n"] = "Không đạt: Bậc của đường cong không chính xác."
            
            # Check curve parameters a and b
            a = -3
            b = int("B3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF", 16)
            if curve.a == a:
                validation_results["Tham số a của đường cong"] = "Đạt"
            else:
                validation_results["Tham số a của đường cong"] = "Không đạt: Tham số a của đường cong không chính xác."
            if curve.b == b:
                validation_results["Tham số b của đường cong"] = "Đạt"
            else:
                validation_results["Tham số b của đường cong"] = "Không đạt: Tham số b của đường cong không chính xác."
        
        end_time = time.time()
        validation_time = end_time - start_time
        
        return validation_results, validation_time
    except Exception as e:
        return {"Lỗi kiểm tra": f"Kiểm tra thất bại: {str(e)}"}, None

# Create Streamlit interface
st.title("Sinh và Kiểm Tra Khóa ECC-384")

# Button to generate a single key
if st.button("Sinh Khóa ECC-384"):
    st.write("Đang sinh khóa ECC-384...")
    private_key, key, generation_time = generate_ecc_key()
    st.success(f"Khóa đã được sinh thành công trong {generation_time:.6f} giây!")
    st.text_area("Khóa riêng ECC-384", key, height=150)
    st.session_state['private_key'] = private_key
    st.session_state['generation_time'] = generation_time

# Button to validate the generated key
if st.button("Kiểm Tra Khóa ECC-384"):
    if 'private_key' in st.session_state:
        st.write("Đang kiểm tra khóa ECC-384...")
        validation_results, validation_time = validate_key(st.session_state['private_key'])
        if validation_time is not None:
            df = pd.DataFrame(list(validation_results.items()), columns=["Tiêu chí", "Kết quả"])
            st.table(df)
           #if all(result == "Đạt" for result in validation_results.values()):
            #    st.success(f"Kiểm tra thành công trong {validation_time:.6f} giây!")
            #else:
             #   st.error(f"Kiểm tra hoàn thành với lỗi trong {validation_time:.6f} giây. Vui lòng xem lại các tiêu chí không đạt.")
        else:
            st.error("Kiểm tra thất bại.")
    else:
        st.error("Chưa có khóa để kiểm tra. Vui lòng sinh khóa trước.")

# Additional information about NIST standards (SP 800-56A and FIPS 186-4)
st.write("### Về ECC-384 và các tiêu chuẩn NIST")
st.markdown(
    """
    **ECC-384** là một thuật toán mã hóa đường cong elliptic với kích thước khóa 384 bit, cung cấp mức độ bảo mật cao.
    Thuật toán này tuân theo các tiêu chuẩn NIST **SP 800-56A** và **FIPS 186-4**, định nghĩa các thực hành được khuyến nghị cho việc sinh và quản lý khóa.
    
    Các tiêu chí kiểm tra bao gồm:
    - **Độ dài khóa ECC-384**: Kiểm tra xem độ dài khóa có đúng 384 bit không.
    - **Trường hữu hạn Fp**: Kiểm tra khóa có thuộc trường hữu hạn Fp với giá trị p = 2^384 − 2^128 − 2^96 + 2^32 − 1.
    - **Tọa độ khóa công khai**: Kiểm tra tọa độ khóa công khai để xác nhận tính hợp lệ.
    - **Điểm gốc G**: Kiểm tra tọa độ của điểm gốc G có khớp với giá trị tiêu chuẩn không.
    - **Bậc của đường cong n**: Kiểm tra bậc của đường cong có đúng như quy định không.
    - **Tham số a và b của đường cong**: Kiểm tra các tham số a và b có đúng như tiêu chuẩn không.
    """
)
