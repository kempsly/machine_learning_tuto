import streamlit as st  # Streamlit for building web UI
from langchain_groq import ChatGroq  # Groq LLM (Gemma, Llama models)

from langchain_classic.chains import LLMMathChain, LLMChain  # Chains for math solving and LLM reasoning
from langchain_classic.prompts import PromptTemplate  # Used to define structured prompts

from langchain_community.utilities import WikipediaAPIWrapper  # Wrapper to access Wikipedia API
from langchain_classic.agents.agent_types import AgentType  # Defines agent behavior type

from langchain_classic.agents import Tool, initialize_agent  # Tool abstraction + agent initialization
from langchain_classic.callbacks import StreamlitCallbackHandler  # Shows agent thinking steps in Streamlit


## Set up Streamlit app configuration
st.set_page_config(
    page_title="Text To Math Problem Solver And Data Search Assistant",  # Browser tab title
    page_icon="🧮"  # Emoji icon for app
)

st.title("Text To Math Problem Solver Using DeepSeek")  # Main title displayed in UI


## Sidebar input for Groq API key
groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")  # Secure input field


## Stop app if API key is not provided
if not groq_api_key:
    st.info("Please add your Groq API key to continue")  # Show message
    st.stop()  # Stop execution of app


## Initialize LLM (Gemma model from Groq)
# llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", groq_api_key=groq_api_key)
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)



## Wikipedia tool setup
wikipedia_wrapper = WikipediaAPIWrapper()  # Create Wikipedia API wrapper

wikipedia_tool = Tool(
    name="Wikipedia",  # Tool name
    func=wikipedia_wrapper.run,  # Function executed when tool is called
    description="Search Wikipedia for general knowledge information"  # Tool description for agent
)


## Math tool setup using LLM-based math solver
math_chain = LLMMathChain.from_llm(llm=llm)  # Chain that solves math problems using LLM

calculator = Tool(
    name="Calculator",  # Tool name
    func=math_chain.run,  # Function to execute math solving
    description="Solves mathematical expressions and word problems"  # Tool description
)


## Prompt template for reasoning tool
prompt = """
You are an agent tasked with solving mathematical questions.
Think step by step and provide a clear explanation.

Question: {question}
Answer:
"""


## Convert prompt into LangChain PromptTemplate
prompt_template = PromptTemplate(
    input_variables=["question"],  # Input variable required by prompt
    template=prompt  # Actual prompt text
)


## LLM chain for reasoning-based answers
chain = LLMChain(llm=llm, prompt=prompt_template)


## Reasoning tool using LLM chain
reasoning_tool = Tool(
    name="Reasoning tool",  # Tool name
    func=chain.run,  # Function executed by tool
    description="Solves logical and reasoning-based questions step by step"  # Description
)


## Initialize agent with all tools
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],  # Available tools
    llm=llm,  # LLM used by agent
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Agent decides tool automatically
    verbose=False,  # Do not print internal steps
    handle_parsing_errors=True  # Prevent crashes from format errors
)


## Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer your questions"}
    ]


## Display previous chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


## Input box for user question
question = st.text_area(
    "Enter your question:",  # Label
    "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes..."  # Default text
)


## Button to trigger response generation
if st.button("Find my answer"):

    if question:  # If user entered a question

        with st.spinner("Generating response..."):  # Show loading animation

            # Save user message in session history
            st.session_state.messages.append({"role": "user", "content": question})

            # Display user message
            st.chat_message("user").write(question)

            # Callback to show agent reasoning in UI
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

            # Run agent with full chat history
            response = assistant_agent.run(
                st.session_state.messages,
                callbacks=[st_cb]
            )

            # Save assistant response in history
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Display response label
            st.write("### Response:")

            # Show final answer
            st.success(response)

    else:
        st.warning("Please enter a question")  # If input is empty