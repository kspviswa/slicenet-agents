from openai import OpenAI
from typing import Dict
from typing_extensions import List

class Prompter:
    def __init__(self):
        self.client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
        self.messages = []
        self.appendSystem()

    def doLLM(self) -> str:
        response = self.client.chat.completions.create(messages=self.messages, model='deepseek-coder-v2:16b').choices[0].message.content
        self.appendHistory('assistant', response)
        return response
    
    def appendHistory(self, role, content):
        self.messages.append({
        'role' : role,
        'content' : content
        })
    
    def getMessages(self) -> List[Dict]:
        return self.messages
    
    def appendSystem(self):
        systemMessage = f"""
        You are a YAML generator assistant for Slicenet Project. Your task is to create a valid YAML file based on the following sample for a slicenet experiment:

        ```yaml
        name: "config0-example"
        description: "This is a test config for slicenet experiment"
        delay_pattern : "default" # or "exponential" "normal" "default"
        epoch: 1 # this applies to slicelets only. TBD to also include slice infra

        clouds:
        - ram: 32
          cpu: 10
          hdd: 200
          name: "wan"

        nfs:
        - name: "NF1"
          ram: 100
          cpu: 9
          hdd: 1234


        policies:
        - type: "NfMgr"
          policy: "first-available-method"
        - type: "SliceMgr"
          policy: "first-available-method"

        slices:
        - name : "Video Streaming"
          composition:
          - nf : "NF1"
            weight : 80


        services:
        - name : "silver"
          composition:
          - slice : "Video Streaming"
            weight : 30

        slicelets:
        - name : "slicelet1"
          service : "silver"
          duration : 5
        ```


        Instructions:
        1. Generate a complete YAML file that adheres to this schema.
        2. Use proper YAML syntax, including correct indentation.
        3. Provide realistic and coherent values for each field.
        4. Ensure all required fields are included.
        5. If any information is missing, ask for clarification before generating the YAML.
        6. After generating the YAML, verify that it matches the schema structure.

        The user will provide specific details or requirements. Based on their input, generate the appropriate YAML file or ask follow-up questions to gather necessary information. If the user has provided response to your previous questions, it should be available in the following chat history. You should keep asking follow-up questions until you determine you have all data to proceed to generate a valid YAML file. You should proceed ONLY if you get user input for all of the required fields. Donot assume or self generate any value.

"""
        self.appendHistory(role='system', content=systemMessage)