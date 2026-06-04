"""
Адаптационный контур (Adaptive Loop) — формализация №1.

Что делает уникального:
- Не просто проверяет наличие компонентов, а проверяет ЗАМКНУТОСТЬ ЦИКЛА
- Память адаптаций — система помнит прошлые возмущения
- Репликация с наследованием памяти
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
import copy
import random
import uuid


@dataclass
class Perturbation:
    """Возмущение среды."""
    name: str
    magnitude: float
    params: Dict[str, Any] = field(default_factory=dict)
    time: Optional[float] = None


@dataclass
class AdaptationRecord:
    """Запись об адаптации."""
    perturbation: Perturbation
    config_before: Dict[str, Any]
    config_after: Dict[str, Any]
    success: bool
    fitness_delta: float
    iteration: int = 0


class AdaptiveLoop:
    """
    Замкнутый адаптационный контур.
    
    Контур замкнут, если:
    1. Есть структурные компоненты (мембрана/каркас)
    2. Есть каталитические компоненты (ускорители реакций)
    3. Есть информационные компоненты (память/код)
    4. Цикл S -> C -> I -> S реально работает
    """
    
    def __init__(
        self,
        components: Optional[Dict[str, List[Any]]] = None,
        memory_limit: int = 20
    ):
        self.id = str(uuid.uuid4())[:8]
        self.components = {
            "structural": list(components.get("structural", [])) if components else [],
            "catalytic": list(components.get("catalytic", [])) if components else [],
            "informational": list(components.get("informational", [])) if components else [],
        }
        self.memory: List[AdaptationRecord] = []
        self.memory_limit = memory_limit
        self.state: Dict[str, Any] = {
            "fitness": 1.0,
            "stability": 1.0,
            "iteration": 0,
        }
        # Связи между компонентами (замкнутость цикла)
        self._links: Dict[str, List[str]] = {
            "structural": [],
            "catalytic": [],
            "informational": [],
        }
    
    def add_link(self, from_type: str, to_type: str):
        """Добавить связь между типами компонентов (S->C, C->I, I->S)."""
        if from_type in self._links and to_type != from_type:
            if to_type not in self._links[from_type]:
                self._links[from_type].append(to_type)
    
    def has_all_components(self) -> bool:
        """Есть ли хотя бы один компонент каждого типа."""
        return all(len(self.components[k]) >= 1 for k in self.components)
    
    def is_closed(self) -> bool:
        """
        Проверка ЗАМКНУТОСТИ цикла.
        
        Не просто наличие компонентов, а:
        structural -> catalytic (структура создаёт условия для катализа)
        catalytic -> informational (катализ кодирует информацию)
        informational -> structural (информация строит структуру)
        """
        if not self.has_all_components():
            return False
        
        # Проверяем цикл: S->C, C->I, I->S
        s_to_c = "catalytic" in self._links.get("structural", [])
        c_to_i = "informational" in self._links.get("catalytic", [])
        i_to_s = "structural" in self._links.get("informational", [])
        
        return s_to_c and c_to_i and i_to_s
    
    def closure_degree(self) -> float:
        """Степень замкнутости: 0.0 (полностью разомкнут) -> 1.0 (полностью замкнут)."""
        if not self.has_all_components():
            return 0.0
        
        links_found = 0
        required = 3  # S->C, C->I, I->S
        
        if "catalytic" in self._links.get("structural", []):
            links_found += 1
        if "informational" in self._links.get("catalytic", []):
            links_found += 1
        if "structural" in self._links.get("informational", []):
            links_found += 1
        
        return links_found / required
    
    def evaluate_fitness(self, context: Optional[Dict[str, Any]] = None) -> float:
        """Оценка приспособленности."""
        ctx = context or {}
        
        fitness = 1.0
        
        # Базовый фитнес зависит от замкнутости
        if self.is_closed():
            fitness += 0.3
        
        # Фитнес растёт с глубиной памяти
        successful_memories = sum(1 for r in self.memory if r.success)
        fitness += 0.1 * min(successful_memories, 10)
        
        # Внешний контекст может модифицировать фитнес
        if "environment_quality" in ctx:
            fitness *= ctx["environment_quality"]
        
        self.state["fitness"] = round(fitness, 4)
        return self.state["fitness"]
    
    def adapt(
        self,
        perturbation: Perturbation,
        generate_configs: Optional[Callable] = None,
        test_config: Optional[Callable] = None,
        apply_config: Optional[Callable] = None,
    ) -> AdaptationRecord:
        """
        Адаптация к возмущению.
        
        Если колбэки не переданы, используется встроенная логика:
        - Пропорционально уменьшает фитнес
        - Пытается восстановить через память прошлых адаптаций
        """
        before_fitness = self.state.get("fitness", 1.0)
        before_cfg = self.snapshot_config()
        success = False
        after_cfg = before_cfg.copy()
        
        if generate_configs and test_config and apply_config:
            # Внешняя логика адаптации
            for cfg in generate_configs(self, perturbation):
                if test_config(self, cfg, perturbation):
                    apply_config(self, cfg)
                    after_cfg = cfg
                    success = True
                    break
        else:
            # Встроенная логика: ищем похожую ситуацию в памяти
            for record in reversed(self.memory):
                if (record.success and
                        record.perturbation.name == perturbation.name and
                        abs(record.perturbation.magnitude - perturbation.magnitude) < 0.3):
                    # Применяем прошлое решение
                    self.state["stability"] = min(1.0, self.state["stability"] + 0.1)
                    after_cfg = record.config_after
                    success = True
                    break
        
        after_fitness = self.evaluate_fitness({})
        
        record = AdaptationRecord(
            perturbation=perturbation,
            config_before=before_cfg,
            config_after=after_cfg,
            success=success,
            fitness_delta=round(after_fitness - before_fitness, 4),
            iteration=self.state["iteration"],
        )
        
        self._store_record(record)
        self.state["iteration"] += 1
        return record
    
    def replicate(self, mutation_rate: float = 0.05) -> "AdaptiveLoop":
        """
        Самовоспроизведение с наследованием памяти и мутациями.
        """
        new_components = copy.deepcopy(self.components)
        
        # Мутация: с вероятностью mutation_rate удаляем или добавляем компонент
        for key in new_components:
            if random.random() < mutation_rate:
                if new_components[key] and random.random() < 0.5:
                    new_components[key].pop()
                else:
                    new_components[key].append(f"mutant_{uuid.uuid4().hex[:4]}")
        
        child = AdaptiveLoop(new_components, self.memory_limit)
        
        # Наследуем связи
        child._links = copy.deepcopy(self._links)
        
        # Наследуем последние 3 адаптации (эпигенетическая память)
        inherited = self.memory[-3:] if len(self.memory) >= 3 else list(self.memory)
        child.memory = [copy.deepcopy(r) for r in inherited]
        
        return child
    
    def _store_record(self, rec: AdaptationRecord):
        """Сохранение с ограничением размера."""
        self.memory.append(rec)
        while len(self.memory) > self.memory_limit:
            self.memory.pop(0)
    
    def snapshot_config(self) -> Dict[str, Any]:
        """Снимок конфигурации."""
        return {
            "fitness": self.state.get("fitness", 1.0),
            "counts": {k: len(v) for k, v in self.components.items()},
            "closure": self.closure_degree(),
            "memory_depth": len(self.memory),
        }
    
    def summary(self) -> str:
        """Человекочитаемое описание."""
        return (
            f"Loop[{self.id}] "
            f"closed={self.is_closed()} "
            f"closure={self.closure_degree():.1%} "
            f"fitness={self.state['fitness']:.2f} "
            f"memory={len(self.memory)} "
            f"components={dict((k, len(v)) for k, v in self.components.items())}"
        )
