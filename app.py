import streamlit as st
from main import query_temp

# Streamlit Interface
st.set_page_config(page_title="Legal Chatbot", page_icon="📈", layout="wide")


# --- Custom Styling ---
st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .criminal-header {
        color: #FF5733; /* Reddish-orange for criminal */
    }
    .civil-header {
        color: #3498DB; /* Blue for civil */
    }
    .both-header {
        color: #2ECC71; /* Green for both */
    }
    .na-header {
        color: #95A5A6; /* Gray for not applicable */
    }
    .response-box {
        background-color: #F0F2F6;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        font-size: 18px;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50; /* Green submit button */
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }
    .user-query-box {
        background-color: #E8F5E9; /* Light green for user query */
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        font-size: 18px;
        font-weight: bold;
    }
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
    }
    .sidebar-text {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)




# Sidebar with description and instructions
st.sidebar.title("Instructions:")
st.sidebar.write(
    """
    
    1. Enter your legal query in the text area.
    
    2. Click the "Submit" button to get a response.
    
    3. Get the legal response.

    """
)

st.sidebar.title("")
st.sidebar.title("")
st.sidebar.title("DEVELOPED BY:")
st.sidebar.write(
    """

    


    
    1. Bhushan
    
    2. Krunal
    
    3. Pravin
    
    4. Ria

    5. Varsha
    """
)


# Main Title
st.title("⚖️ Legal Chatbot")

user_query = st.text_area("🔍 Enter your legal query here:", height=80)

if st.button("Submit"):
    if user_query.strip():
        with st.spinner("⚖️ Processing your legal query..."):
            # Replace with your actual legal processing logic
            # query_response = {"classification": "criminal_law", "response": "This is a sample legal response."} #Example data
            query_response = query_temp(user_query) #Use your actual function

        query_type = query_response["classification"]
        final_response = query_response["response"]
        print(final_response)
        st.markdown(f"<div class='user-query-box'><p class='big-font'>Hello, I have your query.</p></div>", unsafe_allow_html=True)
        # --- Display Response Based on Classification ---
        if query_type == "criminal_law":
            st.markdown("<h3 class='criminal-header'>⚖️ Criminal Law Agent Response</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='response-box'><p class='big-font'>{final_response}</p></div>", unsafe_allow_html=True)

        elif query_type == "civil_law":
            st.markdown("<h3 class='civil-header'>🏛 Civil Law Agent Response</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='response-box'><p class='big-font'>Hello, I am Civil Law Agent. {final_response}</p></div>", unsafe_allow_html=True)

        elif query_type == "both":
            st.markdown("<h3 class='both-header'>⚖️ Both Criminal & Civil Law Apply</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='response-box'><p class='big-font'>{final_response}</p></div>", unsafe_allow_html=True)

        else:  # Not Applicable
            st.markdown("<h3 class='na-header'>❌ Query Not Applicable</h3>", unsafe_allow_html=True)
            st.warning("Sorry, this query is not covered under Indian Law.")

        # --- Interactive Feedback ---
        st.markdown("---")
        if query_type != "na":
            feedback = st.radio("Was this response helpful?", ("Yes", "No"))
            if feedback == "Yes":
                st.success("Glad we could assist!")
            elif feedback == "No":
                st.error("We apologize. Please refine your query or try again later.")

    else:
        st.error("Please enter a query before submitting.")
