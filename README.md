# Research AI Agent

## Overview
This project is an **Advanced Multi-Agent AI Researcher & Writing Tool** that generates in-depth research papers and articles using multiple AI agents. It leverages AI models, web scraping, and language processing tools to provide detailed and structured research on any given topic.

## Features
- AI-powered research and content generation
- Multi-agent system for research, writing, and editing
- Wikipedia integration for quick topic insights
- Supports multiple languages (English, Spanish, French, etc.)
- Different research depths: Basic and Detailed
- AI-generated summaries
- Download reports in PDF or Markdown formats

## Installation
Clone the repository and install the required dependencies:
```sh
 git clone https://github.com/Vermasushant144/Research-AI-agent.git
 cd Research-AI-agent
 pip install -r requirements.txt
```

## Dependencies
This project uses the following Python libraries:
- `streamlit` (for web-based UI)
- `openai` (for AI-powered content generation)
- `crewAI` (for multi-agent task coordination)
- `crewai-tools` (for additional AI functionalities)
- `SerperDevTool` (for web search capabilities)
- `wikipedia` (for Wikipedia-based research)
- `python-dotenv` (for managing API keys)

## Usage
1. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```
2. Enter a research topic and select language & depth.
3. Click on **Run AI Research & Writing**.
4. View the generated research and download the report.

## API Keys
Ensure you have valid API keys set in your `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

## Contributing
Feel free to fork the repository and contribute to the project.

## License
This project is licensed under the MIT License.

