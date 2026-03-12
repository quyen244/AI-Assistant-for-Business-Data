import streamlit as st
import pandas as pd
import requests

# Cấu hình trang (Phải đặt ở dòng đầu tiên)
st.set_page_config(page_title="AI Data Insights", page_icon="📊", layout="wide")

# Custom CSS để giao diện trông hiện đại hơn
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .insight-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        border-left: 5px solid #007bff;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            
            /* Màu chữ mặc định cho card (màu xám rất đậm) */
        color: #333333 !important;
    }
            /* Đảm bảo tiêu đề trong card là màu đen */
    .insight-card h4 {
        color: #000000 !important; 
        margin-top: 0;
    }
    
    /* Đảm bảo nội dung trong card là màu đen */
    .insight-card p {
        color: #1a1a1a !important;
        margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: TẢI FILE ---
with st.sidebar:
    st.title("⚙️ Cấu hình")
    uploaded_file = st.file_uploader("Tải lên tệp CSV của bạn", type=["csv"])
    
    if uploaded_file:
        st.success("Tải file thành công!")
        analyze_button = st.button("🚀 Gửi yêu cầu Phân tích")
    else:
        analyze_button = False

# --- MAIN CONTENT ---
st.title("📊 AI-Powered Data Insights Explorer")
st.markdown("---")

if uploaded_file is not None:
    # Đọc dữ liệu
    df = pd.read_csv(uploaded_file)

    # Chia tab: 1 bên xem dữ liệu, 1 bên xem kết quả phân tích
    tab1, tab2 = st.tabs(["📝 Dữ liệu gốc", "💡 Kết quả phân tích"])

    with tab1:
        st.subheader("Bản xem trước dữ liệu")
        st.dataframe(df, use_container_width=True)
        
        # Thêm một vài chỉ số cơ bản cho đẹp
        col1, col2, col3 = st.columns(3)
        col1.metric("Số hàng", df.shape[0])
        col2.metric("Số cột", df.shape[1])
        col3.metric("Dữ liệu trống", df.isna().sum().sum())

    with tab2:
        if analyze_button:
            with st.spinner('Đang kết nối với AI Server để phân tích...'):
                try:
                    # Gửi Request
                    files = {'file': uploaded_file.getvalue()}
                    response = requests.post(
                        "http://127.0.0.1:8000/datasets/insights", # Lưu ý: Sửa https thành http nếu chạy local chưa có SSL
                        files={'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
                    )
                    
                    if response.status_code == 200:
                        res_data = response.json()
                        
                        # Hiển thị Message thành công
                        st.toast(res_data.get("message", "Thành công!"), icon='✅')
                        
                        # Hiển thị Summary bằng một khung Highlight
                        st.subheader("📌 Tóm tắt tổng quan")
                        st.info(res_data.get("summary", "Không có tóm tắt."))

                        # Hiển thị Danh sách Insights theo dạng Card
                        st.subheader("🔍 Chi tiết Insight")
                        insights = res_data.get("insights", [])
                        
                        if insights:
                            for idx, item in enumerate(insights):
                                with st.container():
                                    # Tạo giao diện kiểu card
                                    st.markdown(f"""
                                    <div class="insight-card">
                                        <h4>Insight #{idx+1}</h4>
                                        <p>{item}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.warning("Không tìm thấy insight nào.")
                            
                    else:
                        st.error(f"Lỗi hệ thống: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Không thể kết nối tới server: {e}")
        else:
            st.info("👈 Hãy nhấn nút **'Gửi yêu cầu Phân tích'** ở thanh bên trái để bắt đầu.")

else:
    # Màn hình chờ khi chưa upload file
    st.image("https://img.freepik.com/free-vector/data-extraction-concept-illustration_114360-4766.jpg", width=400)
    st.info("Vui lòng tải lên một tệp CSV từ thanh bên để bắt đầu khám phá dữ liệu.")

        # streamlit run src/frontend/app.py