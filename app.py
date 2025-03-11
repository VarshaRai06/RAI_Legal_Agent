




import streamlit as st
from main import run_pipeline  # Import LangGraph execution function
from agents.query_processing_agent import classify_legal_domain
from agents.RAI_Agent import ResponsibleAIPipeline
import time

# --- Configure Streamlit Page ---
st.set_page_config(page_title="⚖️ Legal Chatbot", page_icon="📜", layout="wide")

# --- Custom Styling for Chat UI ---
st.markdown(
    """
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 80%;
        margin: auto;
    }
    .user-message {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
        border-radius: 18px;
        align-self: flex-end;
        max-width: 60%;
    }
    .bot-message {
        background-color: #2C2F33;
        color: #FFFFFF;
        padding: 12px;
        border-radius: 18px;
        align-self: flex-start;
        max-width: 60%;
    }
    .system-message {
        background-color: #FFD700;
        color: #000;
        padding: 10px;
        border-radius: 18px;
        align-self: center;
        max-width: 50%;
    }
    .chat-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #1A1A2E;
        max-height: 400px;
        overflow-y: auto;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar with Instructions & Team Members ---
st.sidebar.title("ℹ️ Instructions:")
st.sidebar.write("""
1. Enter your legal query.
2. The chatbot will classify your query.
3. The correct law agent will respond.
""")

st.sidebar.title("👨‍💻 Developed By:")
st.sidebar.write("""
- Bhushan  
- Krunal  
- Pravin  
- Ria  
- Varsha  
""")

# # --- Initialize Chat History ---
# if "chat_history" not in st.session_state:
#     st.session_state["chat_history"] = []

# # --- Chat Display Section ---
# st.title("⚖️ Legal Chatbot")
# chat_area = st.container()

# with chat_area:
#     st.markdown('<div class="chat-box">', unsafe_allow_html=True)

#     for chat in st.session_state["chat_history"]:
#         if chat["role"] == "user":
#             st.markdown(f'<div class="user-message">{chat["message"]}</div>', unsafe_allow_html=True)
#         elif chat["role"] == "system":
#             st.markdown(f'<div class="system-message">{chat["message"]}</div>', unsafe_allow_html=True)
#         else:  # Bot response
#             st.markdown(f'<div class="bot-message">{chat["message"]}</div>', unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

# # --- User Input Section ---
# user_query = st.text_input("🔍 Type your legal query here and press Enter:", key="user_input")

# if user_query:
#     # Store user input in chat history
#     st.session_state["chat_history"].append({"role": "user", "message": user_query})
#     st.rerun()

# if st.session_state["chat_history"] and st.session_state["chat_history"][-1]["role"] == "user":
#     with st.spinner("🤖 Processing your query..."):
#         time.sleep(1)  # Simulate processing time
#         st.session_state["chat_history"].append(
#             {"role": "system", "message": "Hello there, I am your Master Legal Agent. Let me process your query..."}
#         )
#         st.rerun()

# if len(st.session_state["chat_history"]) > 1 and st.session_state["chat_history"][-1]["role"] == "system":
#     with st.spinner("🔍 Classifying your query..."):
#         time.sleep(3)  # Simulate processing delay
#         query_type = classify_legal_domain(user_query)

#         if query_type == "criminal_law":
#             st.session_state["chat_history"].append(
#                 {"role": "system", "message": "Your query belongs to **Criminal Law**. Calling the Criminal Law Agent..."}
#             )
#         elif query_type == "civil_law":
#             st.session_state["chat_history"].append(
#                 {"role": "system", "message": "Your query belongs to **Civil Law**. Calling the Civil Law Agent..."}
#             )
#         elif query_type == "both":
#             st.session_state["chat_history"].append(
#                 {"role": "system", "message": "Your query involves **Both Civil & Criminal Laws**. Calling both agents..."}
#             )
#         else:
#             st.session_state["chat_history"].append(
#                 {"role": "system", "message": "❌ This query is not applicable under Indian Law."}
#             )
#             st.rerun()

#     st.rerun()

# if len(st.session_state["chat_history"]) > 2 and st.session_state["chat_history"][-1]["role"] == "system":
#     with st.spinner("🔎 Fetching legal response..."):
#         # final_response = run_pipeline(user_query)
#         final_response = "final response"
#         st.session_state["chat_history"].append({"role": "bot", "message": final_response})
#         st.rerun()






# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "processing_step" not in st.session_state:
    st.session_state["processing_step"] = 0  # 0: user input, 1: master agent, 2: classification, 3: response

# --- Chat Display Section ---
st.title("⚖️ Legal Chatbot")
chat_area = st.container()

with chat_area:
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for chat in st.session_state["chat_history"]:
        if chat["role"] == "user":
            st.markdown(f'<div class="user-message">{chat["message"]}</div>', unsafe_allow_html=True)
        elif chat["role"] == "system":
            st.markdown(f'<div class="system-message">{chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{chat["message"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- User Input Section ---
user_query = st.text_input("🔍 Type your legal query here:", key="user_input")

if st.button("Send"):
    if user_query:
        if user_query == "mask_example":
            user_query = "John and Hitler were found guilty in the case of theft. Hitler had a long history of theft and was sentenced to 10 years in prison in Mumbai. John was sentenced to 5 years in prison in Mumbai. His phone number is 9876543210 and email is john@gmail.com"
            st.session_state["chat_history"].append({"role": "user", "message": user_query})
            ai_pipeline = ResponsibleAIPipeline()

            anonymized_text = ai_pipeline.anonymize(user_query)
            privacy_checked_text = ai_pipeline.check_privacy_compliance(anonymized_text)
            st.session_state["chat_history"].append({"role": "user", "message": f"Masked: {privacy_checked_text}"})
            st.session_state["processing_step"] = 0  # Reset for next query
            st.rerun()

        st.session_state["chat_history"].append({"role": "user", "message": user_query})
        st.session_state["processing_step"] = 1  # Move to master agent step
        st.rerun()

if st.session_state["processing_step"] == 1:
    with st.spinner("🤖 Processing your query..."):
        time.sleep(1)
        st.session_state["chat_history"].append(
            {"role": "system", "message": "👋 Hello there, I am your Master Legal Agent. Let me process your query..."}
        )
        st.session_state["processing_step"] = 2  # Move to classification step
        st.rerun()

if st.session_state["processing_step"] == 2:
    with st.spinner("🔍 Classifying your query..."):
        time.sleep(3)
        query_type = classify_legal_domain(st.session_state["chat_history"][-2]["message"])
        print(query_type)

        if query_type == "criminal_law":
            st.session_state["chat_history"].append(
                {"role": "system", "message": "🚨 Your query belongs to **Criminal Law**. Calling the Criminal Law Agent..."}
            )
        elif query_type == "civil_law":
            st.session_state["chat_history"].append(
                {"role": "system", "message": "⚖️ Your query belongs to **Civil Law**. Calling the Civil Law Agent..."}
            )
        elif query_type == "both":
            st.session_state["chat_history"].append(
                {"role": "system", "message": "⚠️ Your query involves **Both Civil & Criminal Laws**. Calling both agents..."}
            )
        else:
            st.session_state["chat_history"].append(
                {"role": "system", "message":query_type}
            )
            st.session_state["processing_step"] = 0 #reset
            st.rerun()

        st.session_state["processing_step"] = 3 #move to response step.
        st.rerun()

if st.session_state["processing_step"] == 3:
    with st.spinner("🔎 Fetching legal response..."):
        # final_response = run_pipeline(st.session_state["chat_history"][-2]["message"])
        final_response = "final response" #for test purposes.
        st.session_state["chat_history"].append({"role": "bot", "message": final_response})
        st.session_state["processing_step"] = 0  # Reset for next query
        st.rerun()


