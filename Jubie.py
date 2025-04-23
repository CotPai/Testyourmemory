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

# Chọn chủ đề ngẫu nhiên nếu chưa chọn chủ đề
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = random.choice(list(topics_data.keys()))

# Cho phép người dùng thay đổi chủ đề
selected_topic = st.selectbox("📚 Chọn một chủ đề", list(topics_data.keys()), index=list(topics_data.keys()).index(st.session_state.selected_topic))

# ==== RESET khi bắt đầu lại ====
if st.button("🔄 Bắt đầu lại"):
    # Reset tất cả các giá trị trong session state khi bấm bắt đầu lại
    st.session_state.selected_topic = st.session_state.selected_topic  # Giữ nguyên chủ đề hiện tại
    st.session_state.shuffled = random.sample(topics_data[st.session_state.selected_topic], len(topics_data[st.session_state.selected_topic]))
    st.session_state.selected_positions = [None] * 7  # Reset các vị trí của các mô tả
    st.session_state.show_results = False

# Dữ liệu chủ đề đã chọn
correct_order = topics_data[selected_topic]

# Reset khi đổi chủ đề (xử lý để tránh bị reload)
if st.session_state.get("last_topic") != selected_topic:
    st.session_state.last_topic = selected_topic
    st.session_state.shuffled = random.sample(correct_order, len(correct_order))
    st.session_state.selected_positions = [None] * 7
    st.session_state.show_results = False

# Xử lý nút kiểm tra
if st.button("✅ Kiểm tra"):
    st.session_state.show_results = True

# Nếu chưa bấm kiểm tra: hiển thị phần chọn vị trí
if not st.session_state.show_results:
    st.markdown("### 🔀 Chọn vị trí (1-7) cho từng mô tả:")

    all_filled = True
    user_sequence = [None] * 7

    for i, desc in enumerate(st.session_state.shuffled):
        cols = st.columns([6, 2])
        cols[0].markdown(f"**{desc}**")

        current_value = st.session_state.selected_positions[i]
        options = [""] + [str(j) for j in range(1, 8)]

        pos = cols[1].selectbox(
            "Vị trí",
            options=options,
            key=f"select_{i}",
            index=options.index(str(current_value)) if current_value is not None else 0,
            label_visibility="collapsed"
        )

        if pos == "":
            all_filled = False
            st.session_state.selected_positions[i] = None
        else:
            val = int(pos)
            st.session_state.selected_positions[i] = val
            if user_sequence[val - 1] is not None:
                st.warning(f"⚠️ Vị trí {val} đã được dùng cho mô tả khác!")
                all_filled = False
            else:
                user_sequence[val - 1] = desc

# Nếu đã bấm kiểm tra: hiển thị kết quả và đáp án đúng
if st.session_state.show_results:
    st.markdown("### 🎯 Kết quả:")

    user_sequence = [None] * 7
    for i, val in enumerate(st.session_state.selected_positions):
        if val is not None and 1 <= val <= 7:
            user_sequence[val - 1] = st.session_state.shuffled[i]

    score = 0
    for i in range(7):
        correct_desc = correct_order[i]
        user_desc = user_sequence[i]
        if user_desc == correct_desc:
            st.success(f"{i+1}. ✅ {user_desc}")
            score += 1
        elif user_desc is None:
            st.error(f"{i+1}. ⛔ Chưa có mô tả nào được chọn")
        else:
            st.error(f"{i+1}. ❌ {user_desc}")

    st.markdown(f"**🎉 Bạn sắp xếp đúng {score}/7 mô tả.**")

    # Hiển thị đáp án đúng dưới cùng, cách nhau không quá xa
    st.markdown("### 📘 Đáp án đúng là:")

    for i, line in enumerate(correct_order, 1):
        st.markdown(f"{i}. {line}", unsafe_allow_html=True)
