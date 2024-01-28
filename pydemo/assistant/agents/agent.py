from __future__ import annotations

from typing import Any, Callable, List, NamedTuple, Optional, Sequence

from pydantic import Field



class Agent:
    def __init__(self):
        pass

    def think(
        self,
        instruction: Optional[str] = None,
    ):
        pass

    def execute(
        self,
        command_name: str,
        command_args: dict[str, str] = {},
        user_input: str = "",
    ):
        pass
