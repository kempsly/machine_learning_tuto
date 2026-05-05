from crewai import Agent
from tools import yt_tool
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"]    = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

blog_researcher = Agent(
    role='Blog Researcher from Youtube Videos',
    goal='Get the relevant video content for the topic {topic} from the provided YouTube video',
    verbose=True,
    memory=True,
    backstory="Expert in understanding videos in AI, Data Science, Machine Learning and GenAI.",
    tools=[yt_tool],
    allow_delegation=True,
)

blog_writer = Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the topic {topic} from the YouTube video',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft "
        "engaging narratives that captivate and educate, bringing new "
        "discoveries to light in an accessible manner."
    ),
    tools=[],               # writer doesn't need the tool
    allow_delegation=False,
)




# from crewai import Agent  # imports Agent class used to create autonomous AI agents
# from tools import yt_tool  # custom tool used to fetch YouTube video content/transcripts

# from dotenv import load_dotenv  # loads environment variables from .env file

# load_dotenv()  # activates environment variables (like API keys)

# import os  # provides access to system environment variables

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  


# # sets OpenAI API key from .env into environment variables

# # os.environ["OPENAI_MODEL_NAME"] = "gpt-4-0125-preview"  
# os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"  

# # defines which OpenAI model the agents will use


# ## Create a senior blog content researcher

# blog_researcher = Agent(
#     role='Blog Researcher from Youtube Videos',  
#     # defines the identity/role of this agent
#     goal='get the relevant video transcription for the topic {topic} from the provided Yt channel',  
#     # what this agent is supposed to achieve
#     verbose=True,  
#     # (typo: should be verbose=True) → enables detailed logs of agent reasoning
#     memory=True,  
#     # enables memory so agent can remember previous interactions
#     backstory=(
#        "Expert in understanding videos in AI Data Science , Machine Learning And GEN AI and providing suggestion"  
#     ),  
#     # gives personality and expertise context to the agent
#     tools=[yt_tool],  
#     # tools available to this agent (YouTube tool for fetching video content)
#     allow_delegation=True  
#     # allows this agent to delegate tasks to other agents if needed
# )

# ## Creating a senior blog writer agent with YT tool

# blog_writer = Agent(
#     role='Blog Writer',  
#     # defines writer agent role
#     goal='Narrate compelling tech stories about the video {topic} from YT video',  
#     # objective: convert raw video info into structured blog content
#     verbose=True,  
#     # shows internal reasoning process during execution
#     memory=True,  
#     # allows memory of previous writing tasks
#     backstory=(
#         "With a flair for simplifying complex topics, you craft"
#         "engaging narratives that captivate and educate, bringing new"
#         "discoveries to light in an accessible manner."
#     ),  
#     # defines writing style and personality of the agent
#     tools=[yt_tool],  
#     # allows access to YouTube tool again for context retrieval
#     allow_delegation=False  
#     # this agent cannot delegate tasks to other agents
# )