import openai
import re
from context_extraction import best_extract_relevant_docs_v18

# Function to extract the OPENAI API KEY from the given file
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.readline().strip()
    return api_key

# OpenAI setup
openai.api_key = get_api_key('OPENAI_API_KEY')

# Parameters extraction from zel.params and Config.sh
def extract_parameters_from_file(file_path):
    """
    Extract parameter names from a given file.
    Designed to work with GIZMO's `zel.params` and `Config.sh` style files.
    """
    with open(file_path, 'r') as file:
        content = file.readlines()

    parameters = []

    # Define patterns for parameter extraction. This captures any sequence
    # of non-whitespace characters at the beginning of lines.
    param_pattern = re.compile(r"^\s*([^#\s%=]+)", re.MULTILINE)

    for line in content:
        match = param_pattern.search(line)
        if match:
            parameters.append(match.group(1).strip())

    return parameters



# Fetching details about the parameters using OpenAI
def chat_with_openai(message_history, new_message):
    message_history.append({"role": "user", "content": new_message})
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message_history
    )
    message_content = response.choices[0].message['content'].strip()
    message_history.append({"role": "assistant", "content": message_content})
    return message_history, message_content

# Extract parameters from the files
zel_params = extract_parameters_from_file("zel.params")
config_params = extract_parameters_from_file("Config.sh")

# Print the parameters for verification
print("Parameters from zel.params:")
for param in zel_params:
    print(param)
print("\nParameters from Config.sh:")
for param in config_params:
    print(param)

# Extract documentation snippets for the mentioned parameters
zel_docs = best_extract_relevant_docs_v18(zel_params, "GIZMO_Documentation.txt")
config_docs = best_extract_relevant_docs_v18(config_params, "GIZMO_Documentation.txt")

# Consolidate documentation and parameters
all_docs = {**zel_docs, **config_docs}
relevant_docs = {k: v for k, v in all_docs.items() if v != "Not Found in Documentation"}
documentation_text = "\n".join(relevant_docs.values())

# Start a conversation with OpenAI API
intro_message = "We are running a GIZMO simulation and want to understand the significance of certain parameters. Here are the documentation entries for those parameters. Based on this, please tell us if the simulation will work and provide insights into the provided parameters."
message_history = [{"role": "system", "content": "You are a helpful assistant that understands GIZMO simulations."}]
message_history, response = chat_with_openai(message_history, intro_message + "\n" + documentation_text)
print(response)

