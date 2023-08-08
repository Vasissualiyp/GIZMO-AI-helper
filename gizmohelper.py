import openai
import re
from context_extraction import best_extract_relevant_docs_v18 as extract_documentation
import os
import json
import time


# Change the filepaths here
params_filename = '/scratch/m/murray/vasissua/MUSIC/template/zel.params'
config_filename = '/scratch/m/murray/vasissua/MUSIC/gizmo/Config.sh'
gizmo_documentation_filename = './GIZMO_Documentation.txt'


# OpenAI setup
def get_api_key(file_path): # {{{
    with open(file_path, 'r') as file:
        api_key = file.readline().strip()
    return api_key
#}}}

openai.api_key = get_api_key('OPENAI_API_KEY')
CACHE_FILE = 'params_cache.json'

def summarize_documentation(parameter, doc):
    """
    Summarize the documentation for a single parameter using GPT-3.5-Turbo.
    """
    model = "gpt-3.5-turbo"

    prompt = f"The parameter '{parameter}' is used in the GIZMO hydrodynamics simulation code. " \
             f"Assume that I already know everything about how GIZMO works, but I do not know which parameter does what. Do not tell me if you cannot find something in documentation." \
             f"Please provide a concise, practical summary of the indfluence of the parameter '{parameter}' on the simulation, what what can its different values do (if it has any values, otherwise ignore this value part), " \
             f"based on the following documentation excerpt: '{doc}'."

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant that summarizes technical documentation for astrophysicists."},
            {"role": "user", "content": prompt}
        ]
    )
    print()
    print(f'Original documentation for {parameter}: {doc}')
    print()
    print(f"AI Summary: {response.choices[0].message['content']}")

    return response.choices[0].message['content']
#}}}

def get_cached_documentation(parameters, gizmo_documentation_filename): # {{{
    # Check if cache file exists
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            # Check if the file is not empty
            if os.stat(CACHE_FILE).st_size != 0:
                cached_docs = json.load(f)
            else:
                cached_docs = {}
    else:
        cached_docs = {}

    # Identify parameters whose documentation needs to be fetched
    missing_params = [param for param in parameters if param not in cached_docs]
    print(f" Missing parameters are: {missing_params}")

    # Fetch documentation for missing parameters
    for param in missing_params:
        print(f'Working with {param}...')
        doc_entry = extract_documentation(param, gizmo_documentation_filename)  # Implement this function to get documentation for a parameter
        doc_entry = summarize_documentation(param, doc_entry)
        cached_docs[param] = doc_entry

    # Remove parameters from cache that are not in the current configuration
    for cached_param in list(cached_docs.keys()):
        if cached_param not in parameters:
            del cached_docs[cached_param]

    # Update the cache file
    with open(CACHE_FILE, 'w') as f:
        json.dump(cached_docs, f)

    return cached_docs
#}}}

# Use this function to get documentation for all parameters
# all_documentations = get_cached_documentation(all_parameters)

# Function to extract parameters from the configuration files
def extract_parameters_from_file(file_path): # {{{
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Filter out commented lines and empty lines
    content = [line.strip() for line in content if not line.startswith(('#', '%')) and line.strip()]

    # Extract parameters
    parameters = [line.split('=')[0].strip() if '=' in line else line.strip() for line in content]

    return parameters
#}}}

start_time = time.time()

# Extract the parameters
zel_params = extract_parameters_from_file(params_filename)
config_params = extract_parameters_from_file(config_filename)

end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for documentation extraction: {time_taken} seconds")
start_time = time.time()

# Extract documentation for the parameters #{{{
#docs_zel_params = extract_documentation(zel_params, gizmo_documentation_filename)
#print('zel.params:')
#print(zel_params)
#docs_config_params = extract_documentation(config_params, gizmo_documentation_filename)
#print('Config.sh:')
#print(config_params)
docs_zel_params =    get_cached_documentation(zel_params, gizmo_documentation_filename)
docs_config_params = get_cached_documentation(config_params, gizmo_documentation_filename)
#}}}

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
    #model = "gpt-4-32k"
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

end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for initial respone: {time_taken} seconds")
start_time = time.time()

# Interactive chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        break
    response = get_information_from_openai(user_input, messages)
    print("AI:", response)

end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for total response: {time_taken} seconds")
