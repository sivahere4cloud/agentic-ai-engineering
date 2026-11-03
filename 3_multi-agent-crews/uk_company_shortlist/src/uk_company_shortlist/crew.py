from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field


class TrendingCompany(BaseModel):
    """A UK-listed company that has been in the news"""
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock market ticker, or 'not found'")
    reason: str = Field(description="One sentence on why it is in the news")
    source_date: str = Field(description="Date of the source")
    source_url: str = Field(description="URL of the source")


class TrendingCompanyList(BaseModel):
    """A list of trending companies"""
    companies: List[TrendingCompany] = Field(description="Up to three trending companies")


class CompanyResearch(BaseModel):
    """Verified research on one company"""
    name: str = Field(description="Company name")
    key_facts: List[str] = Field(description="Five short verified facts, each with its source date")
    main_uncertainty: str = Field(description="The company's main uncertainty, in one line")
    sources: List[str] = Field(description="URLs of the sources used")


class CompanyResearchList(BaseModel):
    """Research on several companies"""
    research_list: List[CompanyResearch] = Field(description="Research on each company")


@CrewBase
class UkCompanyShortlist():
    """UkCompanyShortlist crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_company_finder'], # type: ignore[index]
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_researcher'], # type: ignore[index]
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def shortlist_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['shortlist_analyst'], # type: ignore[index]
            verbose=True
        )

    @task
    def find_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_companies'], # type: ignore[index]
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_companies'], # type: ignore[index]
            output_pydantic=CompanyResearchList,
        )

    @task
    def pick_best(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best'], # type: ignore[index]
            output_file='shortlist.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the UkCompanyShortlist crew"""
        manager = Agent(
            config=self.agents_config['manager'], # type: ignore[index]
            allow_delegation=True,
            verbose=True
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True,
        )