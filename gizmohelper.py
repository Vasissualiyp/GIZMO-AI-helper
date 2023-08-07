import openai
import re
from context_extraction import best_extract_relevant_docs_v18

# Change the filepaths here
params_filename = './zel.params'
config_filename = './Config.sh'
gizmo_documentation_filename = './GIZMO_Documentation.txt'


# OpenAI setup
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.readline().strip()
    return api_key

openai.api_key = get_api_key('OPENAI_API_KEY')

# Function to extract parameters from the configuration files
def extract_parameters_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Filter out commented lines and empty lines
    content = [line.strip() for line in content if not line.startswith(('#', '%')) and line.strip()]

    # Extract parameters
    parameters = [line.split('=')[0].strip() if '=' in line else line.strip() for line in content]

    return parameters

# Extract the parameters
zel_params = extract_parameters_from_file(params_filename)
config_params = extract_parameters_from_file(config_filename)

# Extract documentation for the parameters
docs_zel_params = best_extract_relevant_docs_v18(zel_params, gizmo_documentation_filename)
#print('zel.params:')
#print(zel_params)
docs_config_params = best_extract_relevant_docs_v18(config_params, gizmo_documentation_filename)
#print('Config.sh:')
#print(config_params)

# Formulate the documentation snippets for the initial prompt
doc_snippets = []
for param, doc in docs_zel_params.items():
    doc_snippets.append(f"{param}: {doc}")
for param, doc in docs_config_params.items():
    doc_snippets.append(f"{param}: {doc}")

# Initial prompt with documentation
initial_prompt = (
    f"I have a GIZMO simulation setup with the following parameters from zel.params: {', '.join(zel_params)} "
    f"and from Config.sh: {', '.join(config_params)}. "
    f"Based on these configurations and the following documentation snippets, will the simulation run successfully?"
    f"\n\n{' '.join(doc_snippets)}"
)

def get_information_from_openai(prompt, messages):
    model = "gpt-3.5-turbo"
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message['content']

# Initial system message
messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Initial response
response = get_information_from_openai(initial_prompt, messages)
print(response)

# Interactive chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        break
    response = get_information_from_openai(user_input, messages)
    print("AI:", response)

