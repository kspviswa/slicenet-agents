import subprocess
from litellm import completion
import os

# Set the ollama model name here
WEBAGENT_OLLAMA_MODEL_NAME = 'deepseek-coder-v2:16b'

os.environ['OPENAI_API_BASE'] = 'http://localhost:11434'
os.environ['OPENAI_MODEL_NAME'] = f'ollama/{WEBAGENT_OLLAMA_MODEL_NAME}'
os.environ['OPENAI_API_KEY'] = 'NA'

class SlicenetTool:
    
    def __init__(self):
        """Initialize tools with required configurations"""
        self.user_prompt = ""

    def generate_slicenet_config(self):
        pass


