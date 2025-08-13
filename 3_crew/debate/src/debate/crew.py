from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Debate():
    # Description of your crew
    """Debate crew"""


    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def debater(self) -> Agent:
        return Agent(
            config=self.agents_config['debater'],
            verbose=True # print as its running with what's going on
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config['judge'],
            verbose=True  # print as its running with what's going on
        )

    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config['propose'],
            # not needed as specific in config
            # output_file="output/propose.md" 
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config['oppose'],
            # not needed as specific in config
            # output_file="output/oppose.md"
        )

    @task
    def decide(self) -> Task:
        return Task(
            config=self.tasks_config['decide'],
            # not needed as specific in config
            # output_file="output/decide.md"
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            # Hierarchical: A project manager telling workers what to do based on real-time progress. use a manager LLM to assign
            # process=Process.hierarchical
            # Sequential: A factory conveyor belt — parts move in a set order. run tasks in order they are defined
            process=Process.sequential,
            verbose=True,
        )
