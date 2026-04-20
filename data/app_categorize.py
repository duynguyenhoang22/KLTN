import streamlit as st
import pandas as pd
import os

# 1. Cấu hình trang web rộng hơn để có chỗ cho Sidebar
st.set_page_config(page_title="SMS Categorizer", layout="wide")

# ==========================================
# GIAO DIỆN HƯỚNG DẪN (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("📖 Guidelines (V2.0)")
    
    st.markdown("""
    **1. Viễn thông**
    * ✅ **Bao gồm:** Vận hành mạng lưới (Cước, dung lượng Data, nạp thẻ, thông báo trạng thái) VÀ 
    các Dịch vụ giá trị gia tăng (VAS) trừ tiền trực tiếp vào tài khoản di động (Nhạc chờ, Cuộc gọi nhỡ, Dịch vụ nội dung SMS).
    * ❌ **Loại trừ:** Tin nhắn CSKH (chúc mừng/hỏi thăm; tích điểm/đổi quà; sự kiện; khuyến mãi/voucher riêng) từ nhà mạng.

    **2. Cá nhân & OTP**
    * ✅ **Bao gồm:** Chat P2P, OTP từ Mạng xã hội, Game, Ứng dụng công nghệ (Shopee, Grab, Gmail...).
    * ❌ **Loại trừ:** OTP giao dịch tài chính/Ngân hàng.

    **3. Quảng cáo hợp lệ**
    * ✅ **Bao gồm:** Marketing từ Brandname chuẩn, CÓ cú pháp từ chối (VD: Soạn TC gui...).
    * ❌ **Loại trừ:** Tin quảng cáo từ SIM rác (09, 03...).

    **4. Dịch vụ công thật**
    * ✅ **Bao gồm:** Điện, Nước, VNeID, Tin nhắn tuyên truyền/cảnh báo từ Bộ/Ban/Ngành (Bão lụt, Y tế cộng đồng, Ma túy).
    * ❌ **Loại trừ:** Dịch vụ tư nhân giả danh.

    **5. Ngân hàng thật**
    * ✅ **Bao gồm:** OTP Tiền tệ, Biến động số dư, Cảnh báo bảo mật từ Ngân hàng/Ví điện tử.
    * ❌ **Loại trừ:** Tin nhắn nhắc nợ từ App vay tiền/Tín dụng đen.

    **6. Thương mại điện tử**
    * ✅ **Bao gồm:** Trạng thái đơn hàng (Đặt thành công, Hủy, Hoàn tiền) từ sàn TMĐT.
    * ❌ **Loại trừ:** Thông báo shipper đang giao/lấy hàng.

    **7. Y tế**
    * ✅ **Bao gồm:** Lịch khám, nhắc uống thuốc, viện phí từ Bệnh viện/Phòng khám/Nhà thuốc.

    **8. Vận chuyển**
    * ✅ **Bao gồm:** Định vị hàng hóa, mã vận đơn, thông báo từ Shipper (GHTK, Ahamove...).
    
    ---
    **9. Khác (Catch-all)**
    * ⚠️ **Bao gồm:** Tạm thời gom tất cả tin nhắn lừa đảo (Smishing), mạo danh, rác, hoặc tin nhắn mập mờ không khớp với 8 nhóm trên vào đây để chờ Review ở phase sau.
    """)

# ==========================================
# LOGIC CHÍNH BÊN PHẢI (MAIN AREA)
# ==========================================
st.title("🏷️ Công cụ Phân loại Tin nhắn SMS")

csv_files = [
    os.path.join(root, f)
    for root, _, files in os.walk(".")
    for f in files
    if f.endswith(".csv") and not f.endswith("_with_categories.csv")
]
if not csv_files:
    st.warning("Không tìm thấy file data đầu vào (.csv) nào trong thư mục!")
    st.stop()

selected_file = st.selectbox("📂 Chọn file dữ liệu cần phân loại:", csv_files)
OUTPUT_FILE = selected_file.replace(".csv", "_with_categories.csv")

def load_data(input_path, output_path):
    if os.path.exists(output_path):
        return pd.read_csv(output_path)
    df = pd.read_csv(input_path)
    if "category_label" not in df.columns:
        df["category_label"] = None
    return df

if 'current_file' not in st.session_state or st.session_state.current_file != selected_file:
    st.session_state.current_file = selected_file
    st.session_state.df = load_data(selected_file, OUTPUT_FILE)
    
    unlabeled = st.session_state.df[st.session_state.df["category_label"].isna()]
    st.session_state.current_idx = unlabeled.index[0] if not unlabeled.empty else 0

df = st.session_state.df
st.divider()

categories = [
    "Viễn thông", "Cá nhân & OTP", "Quảng cáo hợp lệ", 
    "Dịch vụ công thật", "Ngân hàng thật", "Thương mại điện tử", 
    "Y tế", "Vận chuyển", "Khác"
]

# --- TẠO 2 TABS CHO 2 TÍNH NĂNG KHÁC NHAU ---
tab_label, tab_review = st.tabs(["🏷️ GÁN NHÃN MỚI", "🔍 SOI LỖI & SỬA NHÃN (QA)"])

# ==========================================
# TAB 1: GÁN NHÃN (Logic cũ)
# ==========================================
with tab_label:
    if st.session_state.current_idx < len(df):
        idx = st.session_state.current_idx
        row = df.iloc[idx]
        
        st.progress(idx / len(df))
        st.write(f"**Tiến độ file hiện tại: {idx + 1} / {len(df)} tin nhắn**")
        
        st.success(f"💬 **Nội dung tin nhắn:**\n\n {row['content']}")
        
        st.write("### Phân loại vào nhóm:")
        cols = st.columns(3) 
        
        for i, cat in enumerate(categories):
            with cols[i % 3]:
                if st.button(cat, use_container_width=True, key=f"btn_{i}"):
                    st.session_state.df.at[idx, "category_label"] = cat
                    st.session_state.df.to_csv(OUTPUT_FILE, index=False)
                    st.session_state.current_idx += 1
                    st.rerun()
                    
        st.divider()
        
        if st.button("⏪ Trở lại tin nhắn trước", disabled=(idx == 0)):
            st.session_state.current_idx -= 1
            st.session_state.df.at[st.session_state.current_idx, "category_label"] = None 
            st.session_state.df.to_csv(OUTPUT_FILE, index=False)
            st.rerun()
    else:
        st.balloons()
        st.success(f"🎉 Xuất sắc! Em đã hoàn thành việc gán nhãn cho file **{selected_file}**.")


# ==========================================
# TAB 2: REVIEW & CHỈNH SỬA
# ==========================================
with tab_review:
    st.write("### 🔍 Trạm kiểm soát & Sửa lỗi dữ liệu")
    st.info("💡 Mẹo: Chọn nhóm cần kiểm tra, click đúp vào cột 'category_label' trên bảng để sửa nhãn, sau đó bấm Lưu.")
    
    # Bộ lọc chọn nhóm
    target_category = st.selectbox("📌 Chọn nhóm muốn xem lại:", categories)
    
    # Lọc ra các dòng thuộc nhóm đã chọn
    filtered_df = df[df["category_label"] == target_category]
    
    if filtered_df.empty:
        st.write(f"Chưa có tin nhắn nào được gán nhãn **{target_category}**.")
    else:
        st.write(f"Đang hiển thị **{len(filtered_df)}** tin nhắn thuộc nhóm **{target_category}**:")
        
        # Khoá tất cả các cột không cho sửa, CHỈ CHO SỬA cột category_label
        disabled_cols = [col for col in df.columns if col != "category_label"]
        
        # Bảng dữ liệu tương tác (Cho phép chỉnh sửa drop-down)
        edited_df = st.data_editor(
            filtered_df,
            column_config={
                "category_label": st.column_config.SelectboxColumn(
                    "Nhãn phân loại (Sửa tại đây)",
                    help="Click để đổi sang nhãn khác",
                    options=categories,
                    required=True,
                )
            },
            disabled=disabled_cols,
            use_container_width=True,
            hide_index=False,
            height=400
        )
        
        # Nút lưu các thay đổi
        if st.button("💾 Lưu các thay đổi hàng loạt", type="primary"):
            # Cập nhật các dòng đã sửa vào DataFrame chính trong session state
            for index, row in edited_df.iterrows():
                st.session_state.df.at[index, "category_label"] = row["category_label"]
            
            # Lưu xuống ổ đĩa
            st.session_state.df.to_csv(OUTPUT_FILE, index=False)
            st.success("✅ Đã cập nhật nhãn thành công! Dữ liệu đã được lưu.")
            st.rerun() # Tải lại trang để cập nhật giao diện