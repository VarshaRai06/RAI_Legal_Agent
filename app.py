# import streamlit as st
# from main import query_temp

# # Streamlit Interface
# st.set_page_config(page_title="Legal Chatbot", page_icon="📈", layout="wide")


# # --- Custom Styling ---
# st.markdown(
#     """
#     <style>
#     .big-font {
#         font-size:20px !important;
#         font-weight: bold;
#     }
#     .criminal-header {
#         color: #FF5733; /* Reddish-orange for criminal */
#     }
#     .civil-header {
#         color: #3498DB; /* Blue for civil */
#     }
#     .both-header {
#         color: #2ECC71; /* Green for both */
#     }
#     .na-header {
#         color: #95A5A6; /* Gray for not applicable */
#     }
#     .response-box {
#         background-color: #F0F2F6;
#         padding: 15px;
#         border-radius: 10px;
#         margin-top: 10px;
#         font-size: 18px;
#     }
#     .stButton>button {
#         color: white;
#         background-color: #4CAF50; /* Green submit button */
#         border: none;
#         padding: 10px 20px;
#         text-align: center;
#         text-decoration: none;
#         display: inline-block;
#         font-size: 16px;
#         border-radius: 5px;
#         cursor: pointer;
#     }
#     .user-query-box {
#         background-color: #E8F5E9; /* Light green for user query */
#         padding: 15px;
#         border-radius: 10px;
#         margin-top: 10px;
#         font-size: 18px;
#         font-weight: bold;
#     }
#     .sidebar-title {
#         font-size: 22px;
#         font-weight: bold;
#     }
#     .sidebar-text {
#         font-size: 16px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )




# # Sidebar with description and instructions
# st.sidebar.title("Instructions:")
# st.sidebar.write(
#     """
    
#     1. Enter your legal query in the text area.
    
#     2. Click the "Submit" button to get a response.
    
#     3. Get the legal response.

#     """
# )

# st.sidebar.title("")
# st.sidebar.title("")
# st.sidebar.title("DEVELOPED BY:")
# st.sidebar.write(
#     """

    


    
#     1. Bhushan
    
#     2. Krunal
    
#     3. Pravin
    
#     4. Ria

#     5. Varsha
#     """
# )


# # Main Title
# st.title("⚖️ Legal Chatbot")

# user_query = st.text_area("🔍 Enter your legal query here:", height=80)

# if st.button("Submit"):
#     if user_query.strip():
#         with st.spinner("⚖️ Processing your legal query..."):
#             # Replace with your actual legal processing logic
#             # query_response = {"classification": "criminal_law", "response": "This is a sample legal response."} #Example data
#             query_response = query_temp(user_query) #Use your actual function

#         query_type = query_response["classification"]
#         final_response = query_response["response"]
#         print(final_response)
#         # --- Display Response Based on Classification ---
#         if query_type == "criminal_law":
#             st.markdown("<h3 class='criminal-header'>⚖️ Criminal Law Agent Response</h3>", unsafe_allow_html=True)
#             st.markdown(f"<div class='response-box'><p class='big-font'>{final_response}</p></div>", unsafe_allow_html=True)

#         elif query_type == "civil_law":
#             st.markdown("<h3 class='civil-header'>🏛 Civil Law Agent Response</h3>", unsafe_allow_html=True)
#             st.markdown(f"<div class='response-box'><p class='big-font'>Hello, I am Civil Law Agent. {final_response}</p></div>", unsafe_allow_html=True)

#         elif query_type == "both":
#             st.markdown("<h3 class='both-header'>⚖️ Both Criminal & Civil Law Apply</h3>", unsafe_allow_html=True)
#             st.markdown(f"<div class='response-box'><p class='big-font'>{final_response}</p></div>", unsafe_allow_html=True)

#         else:  # Not Applicable
#             st.markdown("<h3 class='na-header'>❌ Query Not Applicable</h3>", unsafe_allow_html=True)
#             st.warning("Sorry, this query is not covered under Indian Law.")

#         # --- Interactive Feedback ---
#         st.markdown("---")
#         if query_type != "na":
#             feedback = st.radio("Was this response helpful?", ("Yes", "No"))
#             if feedback == "Yes":
#                 st.success("Glad we could assist!")
#             elif feedback == "No":
#                 st.error("We apologize. Please refine your query or try again later.")

#     else:
#         st.error("Please enter a query before submitting.")






# import streamlit as st
# from main import run_pipeline  # Importing main LangGraph execution function
# from agents.query_processing_agent import classify_legal_domain
# import time

# # --- Configure Streamlit Page ---
# st.set_page_config(page_title="⚖️ Legal Chatbot", page_icon="📜", layout="wide")

# # --- Custom Styling ---
# st.markdown(
#     """
#     <style>
#     .big-font { font-size:20px !important; font-weight: bold; }
#     .criminal-header { color: #FF5733; } /* Criminal Law */
#     .civil-header { color: #3498DB; } /* Civil Law */
#     .both-header { color: #2ECC71; } /* Both */
#     .na-header { color: #95A5A6; } /* Not Applicable */
#     .response-box {
#         background-color: #000000; padding: 15px; border-radius: 10px; margin-top: 10px;
#         font-size: 18px; font-weight: bold;
#     }
#     .stButton>button {
#         color: white; background-color: #4CAF50; border: none; padding: 10px 20px;
#         text-align: center; text-decoration: none; display: inline-block;
#         font-size: 16px; border-radius: 5px; cursor: pointer;
#     }
#     .user-query-box {
#         background-color: #E8F5E9; padding: 15px; border-radius: 10px;
#         margin-top: 10px; font-size: 18px; font-weight: bold;
#     }
#     .sidebar-title { font-size: 22px; font-weight: bold; }
#     .sidebar-text { font-size: 16px; }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # --- Sidebar with Instructions & Team Members ---
# st.sidebar.title("ℹ️ Instructions:")
# st.sidebar.write("""
# 1. Enter your legal query.
# 2. Click **Submit**.
# 3. Chatbot will classify your query.
# 4. The relevant **Criminal** or **Civil** law agent will respond.
# """)

# st.sidebar.title("👨‍💻 Developed By:")
# st.sidebar.write("""
# - Bhushan  
# - Krunal  
# - Pravin  
# - Ria  
# - Varsha  
# """)

# # --- Main Title ---
# st.title("⚖️ Legal Chatbot")

# # --- User Query Input ---
# user_query = st.text_area("🔍 Enter your legal query here:", height=80)

# if st.button("Submit"):
#     if user_query.strip():
#         with st.spinner("⚖️ Processing your legal query..."):
#             query_response = {}
#             # query_response = run_pipeline(user_query)  # Call the LangGraph pipeline
#             qr = classify_legal_domain(user_query)  # Call the LangGraph pipeline
#             query_response['classification'] = qr
#             query_response['response'] = qr

#         if isinstance(query_response, dict) and "classification" in query_response and "response" in query_response:
#             query_type = query_response["classification"]  # e.g., "criminal_law", "civil_law", "both", "na"
#             final_response = query_response["response"]

#             # --- Step 1: Master Agent Response ---
#             st.markdown("<h3 class='big-font'>🤖 Master Agent</h3>", unsafe_allow_html=True)
#             if query_type == "criminal_law":
#                 st.markdown(f"<div class='response-box'>Hello! This is a **Criminal Law** query. Calling Criminal Law Agent now...</div>", unsafe_allow_html=True)

#             elif query_type == "civil_law":
#                 st.markdown(f"<div class='response-box'>Hello! This is a **Civil Law** query. Calling Civil Law Agent now...</div>", unsafe_allow_html=True)

#             elif query_type == "both":
#                 st.markdown(f"<div class='response-box'>Hello! This query involves **Both Civil & Criminal Laws**. Calling both agents now...</div>", unsafe_allow_html=True)

#             else:  # Not Applicable
#                 st.markdown(f"<div class='response-box'>❌ Query Not Applicable</h3>", unsafe_allow_html=True)
#                 st.markdown(f"<div class='response-box'>{final_response}</div>", unsafe_allow_html=True)
#                 st.stop()
#             time.sleep(3)
#             # --- Step 2: Criminal or Civil Law Agent Response ---
#             # st.markdown("---")
#             if query_type == "criminal_law":
#                 st.markdown("<h3 class='big-font'>⚖️ Criminal Law Agent Response</h3>", unsafe_allow_html=True)
#                 st.markdown(f"<div class='response-box'><p class='big-font'>{final_response}</p></div>", unsafe_allow_html=True)

#             elif query_type == "civil_law":
#                 st.markdown("<h3 class='big-font'>🏛 Civil Law Agent Response</h3>", unsafe_allow_html=True)
#                 st.markdown(f"<div class='response-box'><p class='big-font'>Hello, I am Civil Law Agent. {final_response}</p></div>", unsafe_allow_html=True)

#             elif query_type == "both":
#                 st.markdown("<h3 class='big-font'>⚖️ Both Criminal & Civil Law Apply</h3>", unsafe_allow_html=True)
#                 st.markdown(f"<div class='response-box'><p class='big-font'>{final_response}</p></div>", unsafe_allow_html=True)

#             # --- Step 3: Feedback Section ---
#             st.markdown("---")
#             if query_type != "na":
#                 feedback = st.radio("Was this response helpful?", ("Yes", "No"))
#                 if feedback == "Yes":
#                     st.success("✅ Glad we could assist!")
#                 elif feedback == "No":
#                     st.error("⚠️ We apologize. Please refine your query or try again later.")

#         else:
#             st.error("⚠️ Unexpected response format. Please try again.")

#     else:
#         st.error("⚠️ Please enter a legal query before submitting.")



import streamlit as st
from main import run_pipeline  # Import LangGraph execution function
from agents.query_processing_agent import classify_legal_domain
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
2. Click Submit.
3. Master Agent will process the query.
4. The correct legal agent will respond.
""")

st.sidebar.title("👨‍💻 Developed By:")
st.sidebar.write("""
- Bhushan  
- Krunal  
- Pravin  
- Ria  
- Varsha  
""")

# --- Initialize Chat History ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

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
        else:  # Bot response
            st.markdown(f'<div class="bot-message">{chat["message"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- User Input Section ---
user_query = st.text_input("🔍 Type your legal query here and press Enter:", key="user_input")

if user_query:
    # Store user input in chat history
    st.session_state["chat_history"].append({"role": "user", "message": user_query})

    with st.spinner("🤖 Processing your query..."):
        time.sleep(1)  # Simulate processing time
        st.session_state["chat_history"].append(
            {"role": "system", "message": "Hello there, I am your Master Legal Agent. Let me process your query..."}
        )

# --- Wait for user to press Enter before proceeding ---
if len(st.session_state["chat_history"]) > 1 and st.button("Continue"):
    with st.spinner("🔍 Classifying your query..."):
        time.sleep(3)  # Simulate processing delay
        query_type = classify_legal_domain(user_query)

        # Add classification message to chat
        if query_type == "criminal_law":
            st.session_state["chat_history"].append(
                {"role": "system", "message": "Your query belongs to **Criminal Law**. Calling the Criminal Law Agent..."}
            )
        elif query_type == "civil_law":
            st.session_state["chat_history"].append(
                {"role": "system", "message": "Your query belongs to **Civil Law**. Calling the Civil Law Agent..."}
            )
        elif query_type == "both":
            st.session_state["chat_history"].append(
                {"role": "system", "message": "Your query involves **Both Civil & Criminal Laws**. Calling both agents..."}
            )
        else:
            st.session_state["chat_history"].append(
                {"role": "system", "message": "❌ This query is not applicable under Indian Law."}
            )

    st.session_state["chat_history"].append(
                {"role": "system", "message": "Your query involves {query_type}**. Calling {query_type} agents..."}
            )

    with st.spinner("🔎 Fetching legal response..."):
        final_response = run_pipeline(user_query)
        st.session_state["chat_history"].append({"role": "bot", "message": final_response})
       


# # --- Final response handling ---
# if len(st.session_state["chat_history"]) > 2 and st.button("Get Response"):
#     with st.spinner("🔎 Fetching legal response..."):
#         final_response = run_pipeline(user_query)
#         st.session_state["chat_history"].append({"role": "bot", "message": final_response})
#         st.rerun()
