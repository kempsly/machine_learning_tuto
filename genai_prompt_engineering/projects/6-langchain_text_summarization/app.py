import validators, streamlit as st  # validators checks if URL is valid, streamlit builds UI

from langchain_classic.prompts import PromptTemplate  # used to define prompt structure for LLM
from langchain_groq import ChatGroq  # Groq LLM (Gemma, Llama models)
from langchain_classic.chains.summarize import load_summarize_chain  # ready-made summarization chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader  
# loads content from YouTube or normal websites

## Streamlit APP setup
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")  
# sets page title and icon

st.title("🦜 LangChain: Summarize Text From YT or Website")  # main title
st.subheader('Summarize URL')  # subtitle

## Sidebar input for API key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")  
    # user enters Groq API key securely

# main input field for URL
generic_url = st.text_input("URL", label_visibility="collapsed")  
# user enters YouTube or website URL

## Initialize LLM (Gemma model via Groq)
llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", groq_api_key=groq_api_key)  
# connects to Groq LLM

## Prompt template for summarization
prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}
"""  
# instruction given to model

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])  
# converts template into LangChain prompt object

## Button to trigger summarization
if st.button("Summarize the Content from YT or Website"):
    
    ## Validate inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")  
        # error if missing inputs

    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. It can be a YT video or website url")  
        # error if URL is invalid

    else:
        try:
            with st.spinner("Waiting..."):  
                # shows loading spinner

                ## Load data from source
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(
                        generic_url,
                        add_video_info=False,
                        language=["en"]
                    )
                    # loads transcript + metadata from YouTube video
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) "
                                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                                          "Chrome/116.0.0.0 Safari/537.36"
                        }
                    )
                    # loads text content from website

                docs = loader.load()  
                # extracts documents from URL

                ## Create summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)  
                # uses "stuff" method (all text into one prompt)

                output_summary = chain.run(docs)  
                # runs summarization on extracted content

                st.success(output_summary)  
                # displays final summary in UI

        except Exception as e:
            st.exception(f"Exception: {e}")  
            # shows error if something fails