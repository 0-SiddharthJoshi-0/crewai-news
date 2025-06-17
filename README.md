# CrewAI News Research System

A multi-agent AI system built with [crewAI](https://crewai.com) that automatically researches and summarizes the latest news articles from India and technology sectors. The system features dynamic date support and uses AI agents to collaborate on complex information gathering and synthesis tasks.

## 🚀 Features

- **Multi-Agent Collaboration**: Uses specialized AI agents for news research and content writing
- **Dynamic Date Support**: Automatically uses current date for news searches
- **Web Search Integration**: Leverages SerperDev for real-time news gathering
- **Structured Output**: Generates well-formatted markdown reports
- **Modular Design**: Easy to customize agents and tasks

## 📋 Prerequisites

- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) package manager
- OpenAI API key or Gemini API key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/0-SiddharthJoshi-0/crewai-news.git
   cd crewai-news
   ```

2. **Install UV (if not already installed)**
   ```bash
   pip install uv
   ```

3. **Install dependencies**
   ```bash
   crewai install
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   # OR
   GEMINI_API_KEY=your_gemini_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

## 🎯 Usage

### Running the News Research System

```bash
crewai run
```

This command will:
1. Initialize the news research crew
2. Search for recent news articles from India and technology sectors
3. Generate a comprehensive report in `report.md`

### Customizing the System

#### Agents Configuration
Modify `src/newproj/config/agents.yaml` to customize agent roles, goals, and behaviors.

#### Tasks Configuration  
Modify `src/newproj/config/tasks.yaml` to adjust task descriptions and expected outputs.

#### Adding Custom Tools
Extend the system by adding custom tools in `src/newproj/tools/` directory.

## 🏗️ Project Structure

```
crewai-news/
├── src/newproj/
│   ├── config/
│   │   ├── agents.yaml      # Agent definitions
│   │   └── tasks.yaml       # Task definitions
│   ├── crew.py              # Main crew implementation
│   ├── main.py              # Entry point
│   └── tools/               # Custom tools
├── knowledge/               # Knowledge base
├── report.md               # Generated reports
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## 🤖 Agents

### News Researcher
- **Role**: News Finder
- **Goal**: Find the 10 most recent and important news articles
- **Tools**: Web search capabilities via SerperDev

### News Writer
- **Role**: Content Writer  
- **Goal**: Create clear and engaging summaries with compelling headlines
- **Output**: Well-formatted markdown reports

## 📊 Output Format

The system generates a `report.md` file containing:
- **Title with current date**
- **Indian News Section** (5 articles)
- **Technology News Section** (5 articles)
- Each article includes headline, summary, source, and URL

## 🔧 Configuration

### LLM Configuration
Currently configured to use Gemini 2.0 Flash. You can modify the LLM settings in `src/newproj/crew.py`.

