# Podcast-Summarizer

This project is part of the course [Building AI products with OpenAI](https://uplimit.com/course/building-ai-products-with-openai) taught by Sidharth Ramachandran.

In this project, I built an LLM app that summarizes a podcast episode, identifies podcast guests, and key momments. You can view it at https://podcast-summarizer.streamlit.app/.

## Approach

- Part 1: use a Large Language Model (LLM) from OpenAI to build the information extraction functionality paired with a Speech to Text model for transcribing the podcast. 
   * I used [Whisper](https://github.com/openai/whisper) as the speech to text model.
   * I used the OpenAI `gpt-3.5-turbo-16k` model to generate the summary by passing in the generated transcript. 

- Part 2: use a simple cloud deployment provider to easily convert the information extraction function to run on demand - this would be the app backend. See [Modal](https://modal.com/).

- Part 3: use ChatGPT from OpenAI as coding assistant to create and deploy a front-end that allows users to experience the end to end functionality. See [streamlit.io](https://streamlit.io/).

