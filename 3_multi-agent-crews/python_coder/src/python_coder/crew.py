from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from python_coder.docker_tool import RunPythonInDocker

@CrewBase
class PythonCoder():
    """PythonCoder crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config['coder'],  # type: ignore[index]
            verbose=True,
            tools=[RunPythonInDocker()],
            max_execution_time=180,
            max_retry_limit=3,
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'], # type: ignore[index]
            output_file='result.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PythonCoder crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )