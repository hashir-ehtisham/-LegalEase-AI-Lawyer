import streamlit as st
from ai71 import AI71

# Access the API key from Streamlit secrets
ai71_api_key = st.secrets["AI71_API_KEY"]

# Initialize the AI71 client with the API key
client = AI71(ai71_api_key)

# Set page config with title and favicon
st.set_page_config(
    page_title="LegalEase 🧑‍⚖️",
    page_icon="assets/lawyer_icon.png",  # Replace with your favicon path
)

# Add custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f4f8;
    }
    .sidebar .sidebar-content {
        background-color: #003366;
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #003366;
    }
    .stChatMessage--assistant {
        background-color: #e0f7fa;
    }
    .stChatMessage--user {
        background-color: #ffffff;
    }
    .title {
        color: #003366;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.write("""
**Legal Ease** is your intelligent assistant for legal advice and information. Powered by advanced AI technology, Legal Ease helps you understand legal matters by providing detailed insights and potential solutions. Whether you have questions about contracts, disputes, or legal procedures, Legal Ease is here to assist you.
""")

st.sidebar.header("How to Use Legal Ease")
st.sidebar.write("""
1. **Enter Your Legal Question**:
   - Provide your legal query or describe the legal issue you are experiencing.

2. **Submit the Question**:
   - Use the input field at the bottom of the page to enter your query.

3. **Get a Response**:
   - Legal Ease will process your input and generate a detailed response with relevant legal information and advice.

4. **Review and Take Action**:
   - Read the response provided by Legal Ease and follow the suggested advice. Consult with a legal professional for further assistance if needed.
""")

# Show title and description.
st.markdown('<h1 class="title">Legal Ease 🧑‍⚖️</h1>', unsafe_allow_html=True)
st.write(
    "This is your Legal Ease that uses the AI71 model to provide legal advice and information."
)

# Initialize session state variables if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.max_tokens = 512
    st.session_state.temperature = 0.7
    st.session_state.top_p = 0.95
    instruction = "Hi! This is your Legal Ease 🧑‍⚖️. Please describe your legal question or issue. For example: 'I need help understanding a contract clause.'"
    st.session_state.messages.append({"role": "assistant", "content": instruction})

# Display the existing chat messages via st.chat_message.
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
    elif message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What legal question or issue do you need help with?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
                    st.markdown(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"An error occurred: {e}")
