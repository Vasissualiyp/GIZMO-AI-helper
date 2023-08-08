# GIZMO Chat

GIZMO Chat is a tool designed to assist users in setting up their GIZMO simulations. Using OpenAI's GPT-3.5-turbo model (ChatGPT), it provides insights into configuration parameters, predicts the success of a simulation based on the provided settings, and assists in debugging by analyzing error messages.

## Setup and Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Set up a virtual environment (optional but recommended) and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
5. Change the filepaths to your params file, Config.sh file, GIZMO Documentation file as needed in the first lines of `gizmohelper.py`

## OpenAI API Key

For the tool to function, you'll need an OpenAI API key:

1. Visit [OpenAI's platform](https://platform.openai.com/signup) to sign up.
2. Navigate to personal -> View API Keys
3. Press on "Create new secret key"
4. Name it if you want. Then copy the key **IMMIDIATELY** - you will not be able to look at it again later!
5. Create a file named `OPENAI_API_KEY` in the root directory of the project.
6. Paste your API key into this file.

## Usage

1. Run `gizmohelper.py`:
   ```bash
   python gizmohelper.py
   ```
2. Follow the on-screen prompts. Provide parameters or paths to the `zel.params` and `Config.sh` files when asked.
3. For error analysis mode, type `error mode`. You can then paste the error message directly or provide a filepath to it.

