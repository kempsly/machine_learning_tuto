from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

research_task = Task(
    description=(
        "Search the YouTube video for content about {topic}. "
        "Extract detailed information, key concepts, and main points covered."
    ),
    expected_output='A comprehensive 3-paragraph report based on the {topic} from the video content.',
    tools=[yt_tool],
    agent=blog_researcher,
)

write_task = Task(
    description=(
        "Using the research report provided, write a complete blog post about {topic}. "
        "Structure it with an introduction, main sections, and a conclusion."
    ),
    expected_output=(
        "A well-structured blog post in Markdown format with headers "
        "and a minimum of 500 words about {topic}."
    ),
    context=[research_task],    # explicitly passes researcher output
    agent=blog_writer,
    async_execution=False,
    output_file='new-blog-post.md',
)



# from crewai import Task  # imports Task class used to define jobs for agents
# from tools import yt_tool  # custom YouTube tool used to fetch video data
# from agents import blog_researcher, blog_writer  
# # imports the two agents created earlier (researcher + writer)


# ## Research Task

# research_task = Task(
#   description=(
#     "Identify the video {topic}."  
#     # tells agent what video/topic to focus on

#     "Get detailed information about the video from the channel video."
#     # instructs agent to extract detailed content from YouTube video
#   ),

#   expected_output='A comprehensive 3 paragraphs long report based on the {topic} of video content.',  
#   # defines what the final result should look like

#   tools=[yt_tool],  
#   # allows the task to use YouTube tool for fetching video content

#   agent=blog_researcher,  
#   # assigns this task to the research agent
# )


# # Writing task with language model configuration

# write_task = Task(
#   description=(
#     "get the info from the youtube channel on the topic {topic}."  
#     # instructs agent to collect information about the topic
#   ),

#   expected_output='Summarize the info from the youtube channel video on the topic{topic} and create the content for the blog',  
#   # defines final blog-style output

#   tools=[yt_tool],  
#   # gives access to YouTube tool again if needed

#   agent=blog_writer,  
#   # assigns this task to the writer agent

#   async_execution=False,  
#   # task runs sequentially (not in parallel)

#   output_file='new-blog-post.md'  
#   # saves final output into a Markdown file
# )