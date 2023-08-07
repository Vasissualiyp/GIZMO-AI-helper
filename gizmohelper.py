import openai
import re

# OpenAI setup
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.readline().strip()
    return api_key

openai.api_key = get_api_key('OPENAI_API_KEY')

def extract_parameters_from_file_v2(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Filter out commented lines and empty lines
    content = [line.strip() for line in content if not line.startswith(('#', '%')) and line.strip()]

    # Extract parameters
    parameters = [line.split('=')[0].strip() if '=' in line else line.strip() for line in content]
    
    return parameters

def get_information_from_openai(prompt):
    model = "gpt-3.5-turbo"
    messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message['content']

# Extract parameters
zel_params = extract_parameters_from_file_v2('./zel.params')
config_params = extract_parameters_from_file_v2('./Config.sh')

# Formulate the initial question for the AI
initial_prompt = f"I have a GIZMO simulation setup with the following parameters from zel.params: {', '.join(zel_params)} and from Config.sh: {', '.join(config_params)}. Based on these configurations, will the simulation run successfully?"

# Get initial response from the AI
response = get_information_from_openai(initial_prompt)
print(response)

# Additional conversation can be continued based on the initial response
# For instance, if the AI provides a generic answer or asks for more information, 
# you can follow up with more specific questions or provide the details it needs.
