import streamlit as st
from ai71 import AI71

# Initialize AI71 client
AI71_API_KEY = "ai71-api-d95427d8-ce80-42cb-8117-cd12ecfe7907"  # Your API key
client = AI71(AI71_API_KEY)

def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for chunk in client.chat.completions.create(
        model="tiiuae/falcon-180B-chat",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True,
    ):
        delta_content = chunk.choices[0].delta.content
        if delta_content:
            response += delta_content

    return response

def send_message():
    message = st.session_state["new_message"]
    if message:
        response = respond(
            message=message,
            history=st.session_state.history,
            system_message=st.session_state.system_message,
            max_tokens=st.session_state.max_tokens,
            temperature=st.session_state.temperature,
            top_p=st.session_state.top_p,
        )
        st.session_state.history.append((message, response))
        st.session_state["new_message"] = ""

# Streamlit UI
st.title("AI Lawyer Chatbot")
st.write("Welcome to your legal assistant. How can I assist you with your legal questions today?")
st.markdown("<p style='color:blue;'>Developed by Hashir Ehtisham</p>", unsafe_allow_html=True)

# Add description to sidebar
st.sidebar.markdown("""
### AI Lawyer Chatbot
Welcome to your AI Lawyer Chatbot, a cutting-edge tool designed to assist you with legal questions and provide insightful legal advice. Developed by Hashir Ehtisham, this application leverages advanced AI technology to offer accurate and relevant legal information.

#### Features:
- **Interactive Chat**: Engage in real-time conversations with the chatbot, designed to simulate interactions with a knowledgeable legal expert.
- **Customizable Settings**: Adjust the behavior of the AI with settings for max tokens, temperature, and top-p (nucleus sampling) to fine-tune responses according to your needs.
- **Chat History**: Review previous interactions with the chatbot directly in the app, keeping track of your legal inquiries and the AI's responses.

#### How It Works:
- **System Message**: The chatbot operates with a predefined system message that sets the context for its responses, ensuring it provides legal advice and information accurately.
- **Real-Time Interaction**: As you input your messages, the AI processes them and generates responses based on the ongoing conversation history and the selected settings.
- **Adaptive Response**: The chatbot's response can be adjusted by changing parameters such as the number of tokens generated, the randomness of the responses (temperature), and the focus on the most likely outcomes (top-p).

This tool is designed to enhance your understanding of legal matters and provide immediate support for your legal inquiries. Enjoy a seamless and informative interaction with your AI-powered legal assistant!
""")

# Set default system message directly
if 'system_message' not in st.session_state:
    st.session_state.system_message = "You are a knowledgeable AI lawyer providing legal advice and information."

with st.expander("Settings"):
    max_tokens_options = [64, 128, 256, 512, 1024, 2048]
    temperature_options = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0]
    top_p_options = [0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0]

    max_tokens = st.selectbox("Max new tokens", options=max_tokens_options, index=max_tokens_options.index(512), key="max_tokens")
    temperature = st.selectbox("Temperature", options=temperature_options, index=temperature_options.index(0.7), key="temperature")
    top_p = st.selectbox("Top-p (nucleus sampling)", options=top_p_options, index=top_p_options.index(0.95), key="top_p")

if 'history' not in st.session_state:
    st.session_state.history = []

# Display chat history above the message input
st.text_area("Chat History", value="\n\n".join([f"User: {h[0]}\n\nAI Lawyer: {h[1]}" for h in st.session_state.history]), height=400, key="chat_history")

message = st.text_input("Your message", key="new_message", on_change=send_message)
