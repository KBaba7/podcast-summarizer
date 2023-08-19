import streamlit as st
import modal
import json
import os

def main():
    # Set the page layout to wide mode
    st.set_page_config(
    page_title="Podcast Summarizer",
    page_icon="🎙️",
    layout="wide")
    #Set css styling 
    st.markdown("""
    <style>     
        body {font-family: serif; }
        .stButton>button {color: white; background-color: #4c8caf; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 6])
    with c1:
        st.image("mic.jpeg", width=100)
    with c2:    
        st.title("Podcast Newsletter")
    st.divider()

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Available Podcasts Feeds")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    if selected_podcast:

        podcast_info = available_podcast_info[selected_podcast]

        # Right section - Newsletter content
        st.subheader(podcast_info['podcast_details']['podcast_title'])

        # Display the podcast title
        #st.subheader("Episode Title")
        st.write(podcast_info['podcast_details']['episode_title'])
        st.audio(podcast_info['podcast_details']['episode_audio_url'])

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_people'])
            st.markdown("""---""")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        # Display the five key moments
        st.markdown("""---""")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)
        st.markdown("""---""")

    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    st.sidebar.markdown("Find the link to the RSS feed for your favorite podcast at [https://www.listennotes.com/](https://www.listennotes.com/)")

    url = st.sidebar.text_input("Link to RSS Feed")
    user_input = st.sidebar.empty()
    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("**Note**: A 30 min podcast processing can take up to 5 mins, please be patient.")

    if process_button:
        if not url:
            user_input.error("Please provide RSS feed URL!")
        elif user_input:
            user_input.empty()

        # Call the function to process the URLs and retrieve podcast guest information
        podcast_info = process_podcast_info(url)

        # Right section - Newsletter content
        st.subheader(podcast_info['podcast_details']['podcast_title'])

        # Display the podcast title
        #st.subheader("Episode Title")
        st.write(podcast_info['podcast_details']['episode_title'])
        st.audio(podcast_info['podcast_details']['episode_audio_url'])

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_people'])
            st.markdown("""---""")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        # Display the five key moments
        st.markdown("""---""")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)
        st.markdown("""---""")   

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            # Process the file data as needed
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("uplimit-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()
