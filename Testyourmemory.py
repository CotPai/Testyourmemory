import streamlit as st
import random
from streamlit_sortables import sort_items

# ==== DỮ LIỆU ==== 
topics_data = {
    "Zoo": [
        "Symbol of privilege and wealth",
        "Opening the door for everyone",
        "Away from amusement towards instruction",
        "Away from enclosure towards greater freedom",
        "A different set of values",
        "A new mission of conversation",
        "A modern day alternative"
    ],
    # ... (giữ nguyên các chủ đề khác) ...
}

# ==== GIAO DIỆN ==== 
st.title("🧠 Luyện trí nhớ theo chủ đề")
selected_topic = st.selectbox("📚 Chọn một chủ đề", list(topics_data.keys()))

if selected_topic:
    correct_order = topics_data[selected_topic]

    # Reset khi đổi chủ đề
    if st.session_state.get("last_topic") != selected_topic:
        for key in list(st.session_state.keys()):
            if key.startswith("shuffled") or key.startswith("show_results") or key == "last_topic":
                del st.session_state[key]
        st.session_state.last_topic = selected_topic
        st.session_state.shuffled = random.sample(correct_order, len(correct_order))

    shuffled = st.session_state.shuffled

    # Kéo thả để sắp xếp
    st.markdown("### 📝 Kéo thả để sắp xếp các câu:")
    arranged = sort_items(shuffled, key="sortable_list", direction="vertical")

    # Nút kiểm tra
    if st.button("✅ Kiểm tra"):
        st.session_state.show_results = True
    elif "show_results" in st.session_state:
        st.session_state.show_results = False

    # Hiển thị kết quả
    if st.session_state.get("show_results", False):
        score = sum(1 for i, desc in enumerate(arranged) if desc == correct_order[i])
        st.success(f"🎉 Bạn sắp xếp đúng {score}/{len(correct_order)}")
        if score < len(correct_order):
            st.markdown("### 📘 Đáp án đúng là:")
            for idx, line in enumerate(correct_order, 1):
                st.markdown(f"{idx}. {line}")
    else:
        st.info("Kéo thả các câu theo thứ tự bạn cho là đúng, rồi nhấn '✅ Kiểm tra' để xem kết quả.")
