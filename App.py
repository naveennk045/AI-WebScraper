import streamlit as st
from Llama import prompt
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
)

# Streamlit UI
st.title(" 🤖 AI Webscraper")

# Description of features (with an appealing UI)
st.markdown("###")
st.subheader(" Welcome to the **AI Web Scraper Chatbot**! 🌟")
st.markdown("""

<p style="margin-left: 20px;">
Seamlessly scrape content from any website and ask intelligent questions to extract specific information.
</p>

<p style="margin-left: 20px;">
This tool is designed to simplify data extraction and make interaction with web content easier than ever before. It combines the power of web scraping and conversational AI to provide a smart, user-friendly interface.
</p>
""", unsafe_allow_html=True)
st.markdown("###")


# Initialize chat history and stage
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Please enter a URL to scrape the website."}]
    st.session_state["stage"] = "url_input"  

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Single chat_input widget for both URL and description
if user_input := st.chat_input("Enter here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Stage 1: User inputs URL for scraping
    if st.session_state["stage"] == "url_input":
        # Step 1: Scrape the website
        with st.spinner("Scraping the website..."):
            dom_content = scrape_website(user_input)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

        # Store cleaned DOM content in session state
        st.session_state.dom_content = cleaned_content

        # Update assistant's message and transition to the next stage
        st.session_state.messages.append({"role": "assistant", "content": "Website scraped successfully! You can now ask questions about the content."})
        st.chat_message("assistant").write("Website scraped successfully! You can now ask questions about the content.")
        
        # Move to next stage (description input)
        st.session_state["stage"] = "description_input"

    # Stage 2: User provides a description for parsing
    elif st.session_state["stage"] == "description_input":
        dom_content = st.session_state.dom_content

        # Step 2: Parse the DOM content based on user input
        st.write("Parsing the content...")

        # Use the user input as the parse description in the Llama model prompt
        template = f"""
            "You are tasked with extracting specific information from the following text content: {dom_content}. "
            "Please follow these instructions carefully: \n\n"
            "1. **Extract Information:** Only extract the information that directly matches the provided description: {user_input}. "
            "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
            "3. **Empty Response:** If no information matches the description, return an empty string ('')."
            "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
        """
        
        # Get response from Llama model
        response = prompt(template)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# Always display the DOM content if it exists
if "dom_content" in st.session_state:
    with st.expander("View  Content", expanded=True):  # Keep the expander open by default
        st.text_area(" Content", st.session_state.dom_content, height=300)
