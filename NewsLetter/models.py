# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the Project Environment.

The project environment is a simple test environment that echoes back messages.
"""

from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class ProjectAction(Action):
    """Action for the Project environment - just a message to echo."""

    message: str = Field(..., description="Message to echo back")


class ProjectObservation(Observation):
    """Observation from the Project environment - the echoed message."""

    echoed_message: str = Field(default="", description="The echoed message")
    message_length: int = Field(default=0, description="Length of the echoed message")
from pydantic import Field
from openenv.core.env_server.types import Action, Observation

class ProjectAction(Action):
    priority_score: float = Field(ge=0.0, le=1.0, description="Priority 0 to 1")

class ProjectObservation(Observation):
    article_length: int = Field(..., description="Word count")
    relevance: float = Field(..., description="User interest match (0-1)")
    reliability: float = Field(..., description="Source trust (0-1)")
    from pydantic import Field
from openenv.core.env_server.types import Action, Observation

class ProjectAction(Action):
    priority_score: float = Field(ge=0.0, le=1.0, description="Priority 0 to 1")

class ProjectObservation(Observation):
    article_length: int = Field(..., description="Word count")
    relevance: float = Field(..., description="User interest match (0-1)")
    reliability: float = Field(..., description="Source trust (0-1)")