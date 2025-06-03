
# AI Voice Assistant

An AI-powered voice assistant that can perform various tasks such as answering questions, opening applications, playing music, telling jokes, and more — all through simple voice commands.

## Features

- Speech recognition to understand user commands.
- Text-to-speech for voice responses.
- Performs web searches and answers general knowledge questions.
- Opens websites and local applications.
- Plays music and tells jokes.
- Provides weather updates and time information.
- Simple and interactive voice-based interface.


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Anusha0501/AI_voice_assistant.git
   cd AI_voice_assistant
   ````

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:

```bash
python assistant.py
```

Speak your commands clearly and interact with the assistant.

## Supported Commands

* "What time is it?"
* "Open YouTube"
* "Search Wikipedia for \[topic]"
* "Play music"
* "Tell me a joke"
* "What's the weather like?"
* And many more...

## Requirements

* Python 3.x
* Libraries as listed in `requirements.txt` (e.g., speech\_recognition, pyttsx3, wikipedia, etc.)

## Troubleshooting

* Ensure your microphone is working and accessible.
* Make sure you have an active internet connection for web-related queries.
* If text-to-speech does not work, verify your system supports `pyttsx3` or replace with another TTS library.

