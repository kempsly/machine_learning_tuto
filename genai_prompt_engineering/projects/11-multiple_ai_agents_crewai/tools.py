from dotenv import load_dotenv
load_dotenv()

from crewai_tools import YoutubeVideoSearchTool

# targets individual videos instead of whole channel — much more stable
yt_tool = YoutubeVideoSearchTool(
    youtube_video_url='https://www.youtube.com/watch?v=aircAruvnKk'
)




# from dotenv import load_dotenv
# load_dotenv()

# from crewai_tools import YoutubeChannelSearchTool

# yt_tool = YoutubeChannelSearchTool(youtube_channel_handle='https://www.youtube.com/@krishnaik06')


# # yt_tool = YoutubeChannelSearchTool(youtube_channel_handle='@krishnaik06')




# # from crewai_tools import YoutubeChannelSearchTool

# # # Initialize the tool with a specific Youtube channel handle to target your search
# # yt_tool = YoutubeChannelSearchTool(youtube_channel_handle='@krishnaik06')

