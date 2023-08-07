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

def get_information_from_openai(prompt, messages):
    model = "gpt-3.5-turbo"
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message['content']

# Extract parameters
zel_params = extract_parameters_from_file_v2('./zel.params')
config_params = extract_parameters_from_file_v2('./Config.sh')

# Define a comprehensive system introduction based on the newly summarized information
system_intro = """
You are a knowledgeable assistant familiar with the GIZMO cosmological simulation software.
- GIZMO operates in "code units" which users select to ensure numerical stability and precision.
- For cosmological runs, it's common to use units where \( G = 1 \) with time in units of the Hubble time.
- Initialization is crucial with parameters like initial time step, boundary conditions, and the initial conditions file playing vital roles.
- Performance optimization is essential. The simulation should be well-balanced across processors.
- Memory allocation can be a bottleneck. The "MaxMemsize" parameter defines the maximum amount of memory the code will allocate per CPU core.
- Softening lengths are important in cosmological simulations. They determine scales below which gravitational forces are suppressed.
- Various physical processes like cooling, star formation, and feedback are part of GIZMO, each having its parameters that need tuning.
"""

# Construct the initial prompt
initial_prompt = f"""
Given the insights above and considering the following parameters from zel.params: {', '.join(zel_params)} and from Config.sh: {', '.join(config_params)}, can you advise on the likelihood of the GIZMO simulation running successfully and any potential concerns?
"""

# Initial system message
messages = [{"role": "system", "content": system_intro}]

# Get initial response from the AI
response = get_information_from_openai(initial_prompt, messages)
print(response)

# Allow the user to have an interactive chat with the model
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    # Append user input to the messages list
    messages.append({"role": "user", "content": user_input})

    response = get_information_from_openai(user_input, messages)

    # Append AI response to the messages list
    messages.append({"role": "ai", "content": response})

    print(f"AI: {response}")

