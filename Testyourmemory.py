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
st.title("🧠 Luyện trí nhớ theo chủ đề")

selected_topic = st.selectbox("📚 Chọn một chủ đề", list(topics_data.keys()))

if selected_topic:
    correct_order = topics_data[selected_topic]

    # Reset mọi thứ khi đổi chủ đề
    if st.session_state.get("last_topic") != selected_topic:
        for key in list(st.session_state.keys()):
            if key.startswith("input_"):
                del st.session_state[key]
        keys_to_reset = ['shuffled', 'last_topic', 'show_results']
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.last_topic = selected_topic
        st.session_state.shuffled = random.sample(correct_order, len(correct_order))
    
    shuffled = st.session_state.get("shuffled", random.sample(correct_order, len(correct_order)))

    # Xử lý nút kiểm tra
    if st.button("✅ Kiểm tra"):
        st.session_state.show_results = True
    else:
        if 'show_results' in st.session_state:
            st.session_state.show_results = False

    st.markdown("### 🔢 Nhập số thứ tự (1-7) sau mỗi mô tả:")

    user_inputs = []
    used_numbers = set()
    has_error = False
    all_valid = True

    for i, desc in enumerate(shuffled):
        cols = st.columns([6, 1])
        
        # Lấy giá trị input
        user_input = cols[1].number_input(
            " ", 
            min_value=0, 
            max_value=7, 
            step=1, 
            key=f"input_{i}", 
            label_visibility="collapsed",
            value=st.session_state.get(f"input_{i}", 0)
        )

        # Kiểm tra lỗi
        if user_input == 0:
            has_error = True
            all_valid = False
        elif user_input in used_numbers:
            st.error(f"⚠️ Số {user_input} đã bị trùng!")
            has_error = True
            all_valid = False
        else:
            used_numbers.add(user_input)
            user_inputs.append((user_input, desc))

        # Tính toán màu sắc
        if st.session_state.get("show_results", False) and all_valid:
            correct_pos = correct_order.index(desc) + 1
            color = "green" if user_input == correct_pos else "red"
            cols[0].markdown(f"<span style='color: {color};'>**{desc}**</span>", unsafe_allow_html=True)
        else:
            cols[0].markdown(f"**{desc}**")

    # Xử lý kết quả
    if st.session_state.get("show_results", False):
        if has_error or len(user_inputs) != 7:
            st.warning("🚫 Vui lòng nhập đủ 7 số từ 1 đến 7, không để trống hoặc trùng.")
            st.session_state.show_results = False
        else:
            user_inputs.sort()
            user_sequence = [desc for _, desc in user_inputs]
            score = sum(1 for i in range(7) if user_sequence[i] == correct_order[i])
            st.success(f"🎉 Bạn sắp xếp đúng {score}/7")

            if score < 7:
                st.markdown("### 📘 Đáp án đúng là:")
                for i, line in enumerate(correct_order, 1):
                    st.markdown(f"{i}. {line}")