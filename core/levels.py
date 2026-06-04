from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable, List
from enum import Enum

class LevelId(str, Enum):
    L0_CHEMISTRY = "L0"
    L1_PROTOCELL = "L1"
    L2_POPULATION = "L2"
    L3_ECOSYSTEM = "L3"

@dataclass
class LevelState:
    level_id: LevelId
    entities: int
    order_parameter: float
    metadata: Dict[str, Any]

class LevelTransition:
    def __init__(self, from_level: LevelId, to_level: LevelId, condition: Callable[[Dict[LevelId, LevelState], Dict[str,Any]], bool], name: str = ""):
        self.from_level = from_level
        self.to_level = to_level
        self.condition = condition
        self.name = name

class MultiLevelSystem:
    def __init__(self):
        self.states: Dict[LevelId, LevelState] = {}
        self.transitions: List[LevelTransition] = []
    
    def register_transition(self, t: LevelTransition):
        self.transitions.append(t)
    
    def check_transitions(self, context: Dict[str,Any]) -> List[LevelTransition]:
        active = []
        for t in self.transitions:
            if t.from_level in self.states and t.condition(self.states, context):
                active.append(t)
        return active
