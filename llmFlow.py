from crewai.flow.flow import Flow, listen, start, router, or_
from litellm import completion
import os

# Set the ollama model name here
WEBAGENT_OLLAMA_MODEL_NAME = 'deepseek-coder-v2:16b'

os.environ['OPENAI_API_BASE'] = 'http://localhost:11434'
os.environ['OPENAI_MODEL_NAME'] = f'ollama/{WEBAGENT_OLLAMA_MODEL_NAME}'
os.environ['OPENAI_API_KEY'] = 'NA'

class slicenetAgentFlow(Flow):

    @start()
    def get_input(self):
        return self.state['prompt']
    
    @router(get_input)
    def determine_route(self):
        user_prompt = self.state['prompt']
        result = completion(
             model=f'ollama/{WEBAGENT_OLLAMA_MODEL_NAME}',
             messages = [
                  {
                       'role' : 'user',
                       'content' : f"""
                        Analyze the following user prompt and send a single text as a response based on the below constraints:
                        USER PROMPT: {user_prompt}

                        Constraints for sending final text:
                        1) If the prompt is asking to generate slicenet configuration files, then you should respond "generate"
                        2) If the prompt is asking to run or execute an experiment, you should respond with "execute"
                        3) If the prompt is asking to generate insights or visualize the experiment output, then you should respond with "visualize"
                        4) If the prompt is general question that doesn't have to do anything with slicenet then you should respond with "llm"

                        
                        Rules:
                        1) Only return a single text as per the constraints. Nothing else.
                        2) When deciding which respone to send, focus on understanding the user's underlying intent and context, even if their phrasing differs from the provided constraints. Prioritize the core task or need rather than specific keywords. Don't send your monologue as response. Follow rule 1 always. 

                        """
                  }
             ],
        )

        decision_text =  result['choices'][0]['message']['content']
        print(f'LLM as a judge decision : {decision_text}')

        if decision_text == 'llm':
             return 'llm'
        if decision_text == 'visualize':
             return 'visualize'
        if decision_text == 'experiment':
             return 'experiment'
        if decision_text == 'generate':
             return 'generate'
             

    @listen('generate')
    def generate_config(self):
         print('Inside Generate')
         return 'final_response'

    @listen('experiment')
    def run_experiment(self):
         print('Inside Experiment')
         return 'final_response'
    
    @listen('visualize')
    def visualize_output(self):
         print('Inside Visualize')
         return 'final_response'

    @listen(or_('llm', 'final_response'))
    def render_llm_response(self):
            result = completion(
                model=f'ollama/{WEBAGENT_OLLAMA_MODEL_NAME}',
                messages=[
                    {
                        'role' : 'user',
                        'content' : self.state['user_prompt']
                    }
                ])
            return result['choices'][0]['message']['content']
    

if __name__ == '__main__':
    flow = slicenetAgentFlow()
    print('\nEnter your query or say "plot" to render the flow or say "bye" to exit\n ')
    while True:
        query = input('\nYou => :\t')
        if query == 'bye':
            print('\n Good Bye! \n')
            exit()
        elif query == 'plot':
            flow.plot('experiment2')
            print('\nPlot saved!\n')
        else:
            flow_res = flow.kickoff(inputs={'prompt' : query})
            print(f'\nAgent 🤖 => : {flow_res}\n')