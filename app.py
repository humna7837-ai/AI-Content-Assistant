import streamlit as st
from groq import Groq

# Page layout configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate engaging social media posts tailored to your platform, audience, and tone.")

# Sidebar - API Configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
st.sidebar.markdown("[Get a free Groq API Key](https://console.groq.com/keys)")

# Main Form Inputs
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Platform", 
            ["LinkedIn", "Instagram", "X (Twitter)", "Facebook", "TikTok"]
        )
        content_type = st.selectbox(
            "Content Type", 
            ["Educational", "Promotional", "Storytelling", "Announcement", "Thought Leadership"]
        )
        tone = st.selectbox(
            "Tone", 
            ["Professional", "Casual & Friendly", "Energetic & Hype", "Witty & Humorous", "Inspirational"]
        )
        
    with col2:
        topic = st.text_input("Topic / Main Message", placeholder="e.g., Launching a new remote-work productivity app")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Tech professionals, Freelancers, Gen Z")
        include_emojis = st.checkbox("Include Emojis", value=True)

    submitted = st.form_submit_button("✨ Generate Post", use_container_width=True)

# Generation Logic
if submitted:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar to proceed.")
    elif not topic:
        st.warning("Please provide a topic for your content.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=api_key)
            
            # Construct Prompt
            prompt = f"""
            You are an expert social media manager. Create a high-converting {platform} post based on the parameters below:
            
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Tone: {tone}
            - Emojis: {'Yes, use relevant emojis' if include_emojis else 'No emojis'}
            
            Formatting requirements:
            1. Deliver a strong hook on the first line.
            2. Write a clear, engaging body section optimized for {platform}.
            3. End with an actionable Call to Action (CTA).
            4. Provide 5-8 highly relevant hashtags at the bottom.
            """
            
            with st.spinner("Crafting your post..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000,
                )
                
            generated_content = response.choices[0].message.content
            
            st.success("Post generated successfully!")
            st.subheader("Your Generated Post:")
            st.markdown(generated_content)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
