import streamlit as st
import google.generativeai as genai

st.title("🧘 Mental Health Support Chatbot 💬")
st.subheader("Let's Talk and Feel Better Together")
st.subheader("By Thatchaphan Samphansompoch")

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Initialize session state for storing chat history and whether the initial message has been sent
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list
if "initial_message_sent" not in st.session_state:
    st.session_state.initial_message_sent = False  # Initialize the flag

# Initialize the Gemini Model only after the API key is provided
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
        
        # AI initiates the conversation only if it hasn't been sent yet
        if not st.session_state.initial_message_sent:
            initial_message = "Hello🤚 How is your feeling today? I'm here to listen and help you navigate through any emotions you are experiencing."
            st.session_state.chat_history.append(("assistant", initial_message))
            st.session_state.initial_message_sent = True  # Mark initial message as sent
            
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")

# Display previous chat history with message bubbles
for role, message in st.session_state.chat_history:
    if role == "assistant":
        st.chat_message("assistant").markdown(message)  # Use markdown for assistant messages
    else:
        st.chat_message("user").text(message)

# Capture user input using chat input
user_input = st.chat_input("Type your message here...")

# Process user input and generate AI response
if user_input:
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").text(user_input)

    # Use Gemini AI to generate a therapeutic response based on user input
    try:
        # Guide the AI with a structured prompt focused on mental health therapy
        prompt = f"You are a compassionate and understanding mental health therapist. Respond to the following in a supportive and empathetic manner:\n\nUser: {user_input}\nTherapist:"
        
        # Generate the response using the provided prompt
        response = model.generate_content(prompt)
        ai_response = response.text

        # Store and display AI response in bubble format
        st.session_state.chat_history.append(("assistant", ai_response))
        st.chat_message("assistant").markdown(ai_response)  # Use markdown for the AI response
        
    except Exception as e:
        st.error(f"An error occurred while generating the response: {e}")
