# Python LLM Integration - Interactive AI Utilities

This repository contains Python scripts for connecting to a **Large Language Model (LLM)** and interacting with a selected AI, providing multiple functionalities such as translation, image generation, audio transcription, etc.

## Files

### 1. `llm_connection.py`
This script handles the connection from Python to the LLM and links it to the selected AI (e.g., **Gemma AI**).  
It allows you to interact with the AI programmatically and set up an interactive session for modeling tasks or custom queries.

**Main features:**
- Connect to the chosen LLM
- Select the AI for interactive use
- Send prompts and receive responses programmatically

### 2. `interactive-AI.py`
This script provides additional utility functions for tasks beyond text interaction.  
You can use it for translation, image creation, audio transcription, and other AI-driven operations.

**Main features:**
- Translate text between languages
- Generate images from prompts
- Transcribe audio files
- Extendable to other AI functionalities

## Usage

1. Ensure you have Python 3.x installed.  
2. Install required dependencies (e.g., `requests`, `openai`, or any library your scripts need).  
3. Run `llm_connection.py` to start an interactive session with the AI.  
4. Use `ai_utilities.py` for specialized tasks like translation, image generation, or audio transcription.

