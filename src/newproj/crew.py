from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai import LLM
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool

from dotenv import load_dotenv


load_dotenv()
'''llm = LLM(
    model = "ollama/llama3.2:1b",
    base_url="http://localhost:11434",
    temperature=0.5,
    max_tokens=2000,
    timeout=120,
    retry_attempts=3
)'''

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)


@CrewBase
class NewsSummaryCrew():
    """Daily News Summary Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self, inputs: dict = None):
        super().__init__()
        self.inputs = inputs or {}
   
    def _interpolate_string(self, text: str) -> str:
        """Interpolate input values in a string."""
        if isinstance(text, str):
            return text.format(**self.inputs)
        return text
    
    def _interpolate_config(self, config: dict) -> dict:
        """Interpolate input values in a configuration dictionary."""
        interpolated_config = {}
        for key, value in config.items():
            if isinstance(value, str):
                interpolated_config[key] = self._interpolate_string(value)
            elif isinstance(value, dict):
                interpolated_config[key] = self._interpolate_config(value)
            else:
                interpolated_config[key] = value
        return interpolated_config
   
    @agent
    def news_researcher(self) -> Agent:
        # Interpolate the agent config
        agent_config = self._interpolate_config(self.agents_config['news_researcher'])
        return Agent(
            config=agent_config, 
            verbose=True,
            llm=llm,
            tools=[SerperDevTool()]
        )

    @agent
    def news_writer(self) -> Agent:
        # Interpolate the agent config
        agent_config = self._interpolate_config(self.agents_config['news_writer'])
        return Agent(
            config=agent_config,
            verbose=True,
            llm=llm
        )

    @task
    def find_news(self) -> Task:
        # Interpolate the task config
        task_config = self._interpolate_config(self.tasks_config['find_news'])
        return Task(
            config=task_config
        )

    @task
    def write_report(self) -> Task:
        # Interpolate the task config
        task_config = self._interpolate_config(self.tasks_config['write_report'])
        return Task(
            config=task_config,
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the News Summary Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
