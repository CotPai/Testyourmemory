import streamlit as st
import random

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
    "Coffee": [
        "The custom of coffee drinking begins to spread",
        "Coffee encourages",
        "A habit that has become a big economy",
        "Problems of coffee economy",
        "A remedy of unjust revenue distribution",
        "Health risks versus health benefits debate",
        "The ancient origin of coffee"
    ],
    "Consumer age": [
        "Making things last longer",
        "A temporary experiment",
        "The reason of secrecy",
        "Still relevant to our times",
        "The difficulty of being generous",
        "Reason to reach a compromise",
        "Important lessons for all of us"
    ],
    "Early Australia": [
        "An alternative history of settlement",
        "Natural barrier to resettlement",
        "Technology helps uncover the ocean's secret",
        "A Journey made by stages",
        "A new evidence that leads to speculation",
        "Lack of knowledge and skills",
        "Determination of the explorers through the ages"
    ],
    "Charles Dickens": [
        "Dickens for our time",
        "Difficulties for modern readers",
        "Keeping the readers guessing",
        "The influence of media",
        "Dickens's early success",
        "Trying to protect his property",
        "Bring the books to life"
    ],
    "Tulips": [
        "The economy during the Golden Age",
        "Coming into fashion",
        "An object of trade",
        "Different types of tulip",
        "Trade mechanics",
        "Trade across Europe",
        "An unexpected turn of events"
    ],
    "Eating in China": [
        "The origins of chinese food",
        "The influence of philosophy",
        "Regional variations",
        "Cooking methods",
        "The style of eating",
        "Changes in the Chinese diets",
        "Effects of a changing diet"
    ],
    "Children and exercises": [
        "Factors contributing to inactivity",
        "The situation have the potential of being worst",
        "The success of a simple idea",
        "The wider effects of regular activity",
        "Ways in which environment can influence behavior",
        "A design for exercise and for study",
        "Achieving the right balance"
    ],
    "Antarctica - Frozen land": [
        "Who is in charge?",
        "First step on the ice",
        "Where is the end of the Earth?",
        "Hidden geography",
        "Race to the Pole",
        "Less effort needed",
        "Why is it so cold?"
    ],
    "Doggett's coat and badge": [
        "The easiest way to travel",
        "Result of a lucky escape",
        "Origins of what the winner receives",
        "A need for change",
        "Earning a reputation",
        "Generations of champions",
        "Not in it for the money"
    ],
    "Meatless diet": [
        "Types of vegetarian",
        "Various explanations",
        "Possible to happen",
        "Farming Factory - it is a harmful thing",
        "Respect the life",
        "Health gets better with diet",
        "Our responsibilities with global"
    ],
    "Music": [
        "A physically demanding activity",
        "A good way to boost your memory",
        "A great opportunity to broaden your social circle",
        "A way to learn discipline and the importance of routine",
        "A creative outlet for expressing emotions",
        "Enhanced sensitivity to other people's feelings",
        "Develop a greater sense of well-being"
    ],
    "Hotel": [
        "A sensible financial choice",
        "The price of convenience may be high",
        "The importance of planning in advance",
        "The impact of lack of freedom",
        "The benefits of living with less",
        "The advantages of having your own space",
        "A competitive business"
    ]
}

# ==== GIAO DIỆN ====
st.set_page_config(page_title="Luyện trí nhớ", layout="centered")
st.title("🧠 Luyện trí nhớ theo chủ đề")

# Chọn chủ đề với key để tự động lưu vào session_state
selected_topic = st.selectbox(
    "📚 Chọn một chủ đề",
    list(topics_data.keys()),
    key="selected_topic"
)

# Khi đổi chủ đề, khởi tạo lại shuffled và các biến liên quan
if 'last_topic' not in st.session_state or st.session_state.last_topic != selected_topic:
    st.session_state.last_topic = selected_topic
    st.session_state.shuffled = random.sample(
        topics_data[selected_topic],
        len(topics_data[selected_topic])
    )
    st.session_state.selected_positions = [None] * len(topics_data[selected_topic])
    st.session_state.show_results = False

# Nút bắt đầu lại: chỉ xáo lại shuffled và reset chọn
if st.button("🔄 Bắt đầu lại"):
    st.session_state.shuffled = random.sample(
        topics_data[selected_topic],
        len(topics_data[selected_topic])
    )
    st.session_state.selected_positions = [None] * len(topics_data[selected_topic])
    st.session_state.show_results = False

correct_order = topics_data[selected_topic]

# Nút kiểm tra kết quả
if st.button("✅ Kiểm tra"):
    st.session_state.show_results = True

# Chưa kiểm tra: hiển thị giao diện chọn vị trí
if not st.session_state.show_results:
    st.markdown("### 🔀 Chọn vị trí (1-{0}) cho từng mô tả:".format(len(correct_order)))
    all_filled = True
    user_sequence = [None] * len(correct_order)

    for i, desc in enumerate(st.session_state.shuffled):
        cols = st.columns([6, 2])
        cols[0].markdown(f"**{desc}**")

        options = [""] + [str(j) for j in range(1, len(correct_order) + 1)]
        pos = cols[1].selectbox(
            "Vị trí",
            options=options,
            key=f"select_{i}",
            index=options.index(str(st.session_state.selected_positions[i])) if st.session_state.selected_positions[i] else 0,
            label_visibility="collapsed"
        )

        if pos == "":
            all_filled = False
            st.session_state.selected_positions[i] = None
        else:
            val = int(pos)
            # kiểm tra trùng
            if user_sequence[val - 1] is not None:
                st.warning(f"⚠️ Vị trí {val} đã được dùng cho mô tả khác!")
                all_filled = False
            else:
                st.session_state.selected_positions[i] = val
                user_sequence[val - 1] = desc

# Đã kiểm tra: hiện kết quả
else:
    st.markdown("### 🎯 Kết quả:")
    user_sequence = [None] * len(correct_order)
    for i, val in enumerate(st.session_state.selected_positions):
        if val is not None and 1 <= val <= len(correct_order):
            user_sequence[val - 1] = st.session_state.shuffled[i]

    score = 0
    for i, correct_desc in enumerate(correct_order):
        user_desc = user_sequence[i]
        if user_desc == correct_desc:
            st.success(f"{i+1}. ✅ {user_desc}")
            score += 1
        elif user_desc is None:
            st.error(f"{i+1}. ⛔ Chưa có mô tả nào được chọn")
        else:
            st.error(f"{i+1}. ❌ {user_desc}")

    st.markdown(f"**🎉 Bạn sắp xếp đúng {score}/{len(correct_order)} mô tả.**")
    
    st.markdown("### 📘 Đáp án đúng là:")
    for i, line in enumerate(correct_order, 1):
        st.markdown(f"{i}. {line}")
