from gradio_tools.tools import (
    ImageCaptioningTool,
    # StableDiffusionPromptGeneratorTool,
    # StableDiffusionTool,
    TextToVideoTool,
)
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
tools = [
    # StableDiffusionTool().langchain,
    ImageCaptioningTool().langchain,
    # StableDiffusionPromptGeneratorTool().langchain,
    TextToVideoTool().langchain,
]


agent = initialize_agent(
    tools, llm, memory=memory, agent="conversational-react-description", verbose=True
)
output = agent.run(
    input=(
        "Please create a photo of a dog riding a skateboard "
        "but improve my prompt prior to using an image generator."
        "Please caption the generated image and create a video for it using the improved prompt."
    )
)