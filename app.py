import streamlit as st
from main import run_pipeline  # Import LangGraph execution function
from agents.query_processing import classify_legal_domain
from agents.responsible_flow import ResponsibleAIPipeline
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
            gap: 20px; /* Increased spacing between messages */
            max-width: 100%;
            margin: auto;
        }

        /* User Message - Left Side with Human Icon */
        .user-message-container {
            display: flex;
            align-items: center;
            justify-content: flex-start; /* Move user message to the left */
            gap: 10px;
        }

        .user-icon {
            width: 35px;
            height: 35px;
            background: url('https://cdn-icons-png.flaticon.com/512/847/847969.png') no-repeat center;
            background-size: cover;
        }

        .user-message {
            background-color: #D3D3D3;  /* Light Grey */
            color: #000000;  /* Black Text */
            padding: 12px;
            border-radius: 18px;
            align-self: flex-start; /* Push to extreme left */
            max-width: 50%;
            text-align: left;
        }

        /* Bot Response - Right Side with Robot Icon */
        .bot-message-container {
            display: flex;
            align-items: center;
            justify-content: flex-end; /* Move bot message to the right */
            gap: 10px;
            margin-left: 50px;  /* ✅ Push system message slightly to the right */
        }

        .bot-icon {
            width: 35px;
            height: 35px;
            background: url('https://cdn-icons-png.flaticon.com/512/4712/4712102.png') no-repeat center;
            background-size: cover;
        }

        .bot-message {
            background-color: #A98EF7; /* Light Purple */
            color: #000000;  /* Black Text */
            padding: 12px;
            border-radius: 18px;
            align-self: flex-end;
            max-width: 50%;
            text-align: right;
        }

        .system-message-container {
            display: flex;
            align-items: center;
            justify-content: flex-end; /* Move bot message to the right */
            gap: 10px;
            
        }

        .system-icon {
            width: 35px;
            height: 35px;
            background: url('https://cdn-icons-png.flaticon.com/512/3798/3798933.png') no-repeat center;
            background-size: cover;
        }

        .system-message {
            background-color: #6063d6;
            color: #000000;
            padding: 12px;
            border-radius: 18px;
            align-self: center;
            max-width: 60%;
            text-align: center;
        }

        .chat-box {
            display: flex;
            flex-direction: column;
            padding: 15px;
            border-radius: 10px;
            background-color: #1A1A2E;
            max-height: 600px;
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
            st.markdown(
                f"""
                <div class="user-message-container">
                    <div class="user-icon"></div>
                    <div class="user-message">{chat["message"]}</div>
                </div>
                """, unsafe_allow_html=True
            )
        elif chat["role"] == "system":
            st.markdown(
                f"""
                <div class="system-message-container">
                    <div class="system-message">{chat["message"]}</div>
                    <div class="system-icon"></div>
                </div>
                """, unsafe_allow_html=True
            )
            # st.markdown(f'<div class="system-message">{chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f"""
                <div class="bot-message-container">
                    <div class="bot-message">{chat["message"]}</div>
                    <div class="bot-icon"></div>
                </div>
                """, unsafe_allow_html=True
            )
        st.markdown("<br>", unsafe_allow_html=True)  # Add space between messages
    st.markdown('</div>', unsafe_allow_html=True)


# --- User Input Section ---

user_query = st.text_input("🔍 Type your legal query here:", key="user_input")

 

if st.button("Send"):

    if user_query:

        if user_query == "mask_example":

            user_query = "Varsha and Bhushi were found guilty in the case of murder. Hitler had a long history of theft and was sentenced to 10 years in prison in Mumbai. John was sentenced to 5 years in prison in Mumbai. His phone number is 9876543210 and email is john@gmail.com"

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

                {"role": "system", "message": "🚨 Your query belongs to *Criminal Law*. Calling the Criminal Law Agent..."}

            )

        elif query_type == "civil_law":

            st.session_state["chat_history"].append(

                {"role": "system", "message": "⚖️ Your query belongs to *Civil Law*. Calling the Civil Law Agent..."}

            )

        elif query_type == "both":

            st.session_state["chat_history"].append(

                {"role": "system", "message": "⚠️ Your query involves *Both Civil & Criminal Laws*. Calling both agents..."}

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


        final_response = run_pipeline(user_query)

        # final_response = "final response" #for test purposes.

        st.session_state["chat_history"].append({"role": "bot", "message": final_response})

        st.session_state["processing_step"] = 0  # Reset for next query

        st.rerun()