from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage # vectrr based retrival
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
 
# Structured outputs In other words, we are going to ask our different tasks to be providing information according to a
# particular JSON schema

# Because remember, whilst memory, these abstractions are trying to make memory seem quite magical and
# taken care of for you.
# At the end of the day, memory just means more stuff shoved into the prompt, more relevant context
# put into the prompt so that when you call an LLM it has knowledge.
# It's in the input is included information about prior conversations or about prior information that it retrieved.

# And then we told our agents we turned memory on by saying memory equals true for the agents that we
# wanted to remember things.

class TrendingCompany(BaseModel):
    """ A company that is in the news and attracting attention """
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """ List of multiple trending companies that are in the news """
    companies: List[TrendingCompany] = Field(description="List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    """ Detailed research on a company """
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """ A list of detailed research on all the companies """
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending companies")


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'],
                     tools=[SerperDevTool()], memory=True) # to let agent have memory
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], 
                     tools=[SerperDevTool()])

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], 
                     tools=[PushNotificationTool()], memory=True) # to let agent have memory, Don't pick the same company twice
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            # And that is telling it that this task needs to output some JSON in the schema that conforms to TrendingCompanyList.
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList,
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'],
        )
    
    # It's the manager, and we don't want that to be in the list of the of the, the general agents that
    # are going to be working on the task at hand.
    # We're going to want to create this separately and handle it separately.
    # So we create our manager agent like this just as a, as a as a separate variable manager, an agent
    # that has the config from that's called manager.


    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        # manager agent
        manager = Agent(
            config=self.agents_config['manager'],
            # telling crew that this agent can delegate tasks to other agents, equivalent to handoff in OpenAI Agents SDK
            allow_delegation=True
        )
            
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            # Hierarchical: A project manager telling workers what to do based on real-time progress. use a manager LLM to assign
            # Sequential: A factory conveyor belt — parts move in a set order. run tasks in order they are defined
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            # Long-term memory for persistent storage across sessions
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            # Short-term memory for current context using RAG
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config={
                            "provider": "openai",
                            "config": {
                                "model": 'text-embedding-3-small' # generate vectors from text
                            }
                        },
                        type="short_term",
                        path="./memory/"
                    )
                ),            
            # Entity memory for tracking key information about entities
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )
