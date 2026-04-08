# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Project Environment Implementation.

A simple test environment that echoes back messages sent to it.
Perfect for testing HTTP server infrastructure.
"""

from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

# Import models (works both in‑repo and standalone)
try:
    from ..models import ProjectAction, ProjectObservation
except ImportError:
    from models import ProjectAction, ProjectObservation


class ProjectEnvironment(Environment):
    """
    A simple echo environment that echoes back messages.

    This environment is designed for testing the HTTP server infrastructure.
    It maintains minimal state and simply echoes back whatever message it receives.
    """

    # Enable concurrent WebSocket sessions.
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        """Initialize the project environment."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._reset_count = 0

    def reset(self) -> ProjectObservation:
        """Reset the environment."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._reset_count += 1

        return ProjectObservation(
            echoed_message="Project environment ready!",
            message_length=0,
            done=False,
            reward=0.0,
        )

    def step(self, action: ProjectAction) -> ProjectObservation:
        """Execute a step by echoing the message."""
        self._state.step_count += 1

        message = action.message
        length = len(message)

        # Simple reward: longer messages get higher rewards
        reward = length * 0.1

        return ProjectObservation(
            echoed_message=message,
            message_length=length,
            done=False,
            reward=reward,
            metadata={"original_message": message, "step": self._state.step_count},
        )

    @property
    def state(self) -> State:
        """Get the current environment state."""
        return self._state
