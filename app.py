import streamlit as st
from ai71 import AI71

# Access the API key from Streamlit secrets
ai71_api_key = st.secrets["AI71_API_KEY"]

# Initialize the AI71 client with the API key
client = AI71(ai71_api_key)

# Set page config with title and favicon
st.set_page_config(
    page_title="LegalMind 🧑‍⚖️",
    page_icon="assets/lawyer_icon.png",  # Replace with your favicon path
)

# Add custom CSS for styling
st.markdown(
    """
    <style>
    /* Set a light background and dark text color to ensure visibility in dark mode */
    body {
        background-color: #ffffff; /* White background */
        color: #000000; /* Black text */
    }
    .main {
        background-color: #f0f4f8; /* Light background */
        color: #000000; /* Black text */
    }
    .sidebar .sidebar-content {
        background-color: #003366; /* Dark blue sidebar background */
        color: #ffffff; /* White text in the sidebar */
    }
    .stButton>button {
        color: #FFFFFF; /* White text for buttons */
        background-color: #003366; /* Dark blue button background */
    }
    .stChatMessage--assistant {
        background-color: #e0f7fa; /* Light cyan background for assistant messages */
        color: #000000; /* Black text for assistant messages */
    }
    .stChatMessage--user {
        background-color: #ffffff; /* White background for user messages */
        color: #000000; /* Black text for user messages */
    }
    .title {
        color: #003366; /* Dark title color */
    }
    .initial-message {
        color: #000000; /* Black text for the initial message */
    }
    .message-content {
        color: #000000 !important; /* Black text for all messages */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.write("""
**Legal Mind** is your intelligent assistant for legal advice and information. Powered by advanced AI technology, Legal Mind helps you understand legal matters by providing detailed insights and potential solutions. Whether you have questions about contracts, disputes, or legal procedures, Legal Mind is here to assist you.
""")

st.sidebar.header("How to Use Legal Mind")
st.sidebar.write("""
1. **Enter Your Legal Question**:
   - Provide your legal query or describe the legal issue you are experiencing.

2. **Submit the Question**:
   - Use the input field at the bottom of the page to enter your query.

3. **Get a Response**:
   - Legal Mind will process your input and generate a detailed response with relevant legal information and advice.

4. **Review and Take Action**:
   - Read the response provided by Legal Mind and follow the suggested advice. Consult with a legal professional for further assistance if needed.
""")

# Show title and description.
st.markdown('<h1 class="title">Legal Mind 🧑‍⚖️</h1>', unsafe_allow_html=True)
st.write(
    "This is your Legal Mind that uses the AI71 model to provide legal advice and information."
)

# Initialize session state variables if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.max_tokens = 512
    st.session_state.temperature = 0.7
    st.session_state.top_p = 0.95
    instruction = ("<span class='initial-message'>Hi! This is your Legal Mind 🧑‍⚖️. "
                   "Please describe your legal question or issue. For example: 'I need help "
                   "understanding a contract clause.'</span>")
    st.session_state.messages.append({"role": "assistant", "content": instruction})

# Display the existing chat messages via st.chat_message.
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(f"<div class='message-content'>{message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"<div class='message-content'>{message['content']}</div>", unsafe_allow_html=True)

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What legal question or issue do you need help with?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='message-content'>{prompt}</div>", unsafe_allow_html=True)

    # Generate a response using the AI71 API.
    with st.spinner("Generating response..."):
        try:
            response = client.chat.completions.create(
                model="tiiuae/falcon-180B-chat",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=st.session_state.max_tokens,
                temperature=st.session_state.temperature,
                top_p=st.session_state.top_p
            )
            # Collect and concatenate response chunks
            if response.choices and response.choices[0].message:
                full_response = response.choices[0].message.content

                # Ensure the response does not include 'User:'
                if full_response.endswith('User:'):
                    full_response = full_response.replace('User:', '').strip()

                # Stream the full response to the chat using st.write
                with st.chat_message("assistant"):
                    st.markdown(f"<div class='message-content'>{full_response}</div>", unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"An error occurred: {e}")
