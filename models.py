from pydantic import Field
from openenv.core.env_server.types import Action, Observation

class ProjectAction(Action):
    """Action containing a message to echo."""
    message: str = Field(..., description="Message to echo back")

class ProjectObservation(Observation):
    """Observation with echoed message and its length."""
    echoed_message: str = Field(default="", description="The echoed message")
    message_length: int = Field(default=0, description="Length of the echoed message")

__all__ = ["ProjectAction", "ProjectObservation"]