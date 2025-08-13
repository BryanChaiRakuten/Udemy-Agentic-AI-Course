from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# when you set up a custom tool you have to first describe using a pedantic object, the schema of what will be passed in to your
# custom tool.
# And then you end up writing an underscore run method, which is going to take that schema as its parameters.


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
