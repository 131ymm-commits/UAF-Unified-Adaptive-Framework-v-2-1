"""
Мультиуровневость (Multilevel) — формализация №2.

Что делает уникального:
- Уровни связаны через AdaptiveLoop
- Переход создаёт РЕАЛЬНУЮ сущность следующего уровня
- Отслеживает историю всех переходов
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Callable, List, Optional
from enum import Enum
import time as _time

from .loop import AdaptiveLoop


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
    metadata: Dict[str, Any] = field(default_factory=dict)


class LevelTransition:
    def __init__(
        self,
        from_level: LevelId,
        to_level: LevelId,
        condition: Callable[[Dict[LevelId, LevelState], Dict[str, Any]], bool],
        name: str = "",
    ):
        self.from_level = from_level
        self.to_level = to_level
        self.condition = condition
        self.name = name


@dataclass
class EmergenceEvent:
    """Событие эмерджентного перехода."""
    from_level: LevelId
    to_level: LevelId
    transition_name: str
    time: float
    context: Dict[str, Any]
    loop_snapshot: Dict[str, Any]


class MultiLevelSystem:
    """
    Многоуровневая система UAF.
    
    Связь с AdaptiveLoop:
    - Когда AdaptiveLoop на уровне L0 достигает замкнутости,
      система проверяет условия перехода на L1
    - Переход создаёт новый AdaptiveLoop как сущность L1
    """
    
    def __init__(self):
        self.states: Dict[LevelId, LevelState] = {}
        self.transitions: List[LevelTransition] = []
        self.history: List[EmergenceEvent] = []
        
        # Сущности на каждом уровне (AdaptiveLoop'ы)
        self.entities: Dict[LevelId, List[AdaptiveLoop]] = {
            level: [] for level in LevelId
        }
    
    def set_state(self, state: LevelState):
        self.states[state.level_id] = state
    
    def register_entity(self, loop: AdaptiveLoop, level: LevelId):
        """Зарегистрировать AdaptiveLoop на уровне."""
        self.entities[level].append(loop)
    
    def register_transition(self, t: LevelTransition):
        self.transitions.append(t)
    
    def check_transitions(self, context: Dict[str, Any]) -> List[LevelTransition]:
        """Проверить, какие переходы доступны."""
        active = []
        for t in self.transitions:
            if t.from_level in self.states:
                try:
                    if t.condition(self.states, context):
                        active.append(t)
                except Exception:
                    pass
        return active
    
    def execute_transition(
        self,
        transition: LevelTransition,
        source_loop: AdaptiveLoop,
        context: Dict[str, Any],
    ) -> Optional[AdaptiveLoop]:
        """
        Выполнить переход: создать новую сущность на следующем уровне.
        
        Новая сущность — это AdaptiveLoop, порождённый из исходного,
        но с обновлёнными компонентами (на уровне выше).
        """
        if not transition.condition(self.states, context):
            return None
        
        # Создаём новый AdaptiveLoop на следующем уровне
        # Его компоненты — это агрегаты компонентов исходных
        new_loop = AdaptiveLoop(
            components={
                "structural": [f"L1_structure_{len(self.entities[transition.to_level])}"],
                "catalytic": [f"L1_catalyst_{len(self.entities[transition.to_level])}"],
                "informational": [f"L1_info_{len(self.entities[transition.to_level])}"],
            }
        )
        
        # Настройка связей для нового уровня
        new_loop.add_link("structural", "catalytic")
        new_loop.add_link("catalytic", "informational")
        new_loop.add_link("informational", "structural")
        
        # Наследуем память от исходного
        new_loop.memory = list(source_loop.memory[-3:])
        
        # Регистрируем
        self.register_entity(new_loop, transition.to_level)
        
        # Обновляем состояние
        entity_count = len(self.entities[transition.to_level])
        self.set_state(LevelState(
            level_id=transition.to_level,
            entities=entity_count,
            order_parameter=new_loop.closure_degree(),
            metadata={"created_from": source_loop.id},
        ))
        
        # Записываем в историю
        event = EmergenceEvent(
            from_level=transition.from_level,
            to_level=transition.to_level,
            transition_name=transition.name,
            time=_time.time(),
            context=context.copy(),
            loop_snapshot=source_loop.snapshot_config(),
        )
        self.history.append(event)
        
        return new_loop
    
    def get_summary(self) -> Dict[str, Any]:
        """Общая сводка по всем уровням."""
        summary = {}
        for level in LevelId:
            entities = self.entities.get(level, [])
            closed = sum(1 for e in entities if e.is_closed())
            summary[level.value] = {
                "total": len(entities),
                "closed": closed,
                "open": len(entities) - closed,
            }
        summary["transitions_count"] = len(self.history)
        return summary
    
    def has_life_emerged(self) -> bool:
        """Появилась ли жизнь (хотя бы один замкнутый контур на L1+)."""
        for level in [LevelId.L1_PROTOCELL, LevelId.L2_POPULATION, LevelId.L3_ECOSYSTEM]:
            for entity in self.entities.get(level, []):
                if entity.is_closed():
                    return True
        return False
