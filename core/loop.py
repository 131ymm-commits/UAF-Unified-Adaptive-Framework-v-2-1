from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
import copy
import math
import uuid

@dataclass
class Perturbation:
    name: str
    magnitude: float
    params: Dict[str, Any] = field(default_factory=dict)
    time: Optional[float] = None

@dataclass
class AdaptationRecord:
    perturbation: Perturbation
    config_before: Dict[str, Any]
    config_after: Dict[str, Any]
    success: bool
    fitness_delta: float
    memory_key: Optional[str] = None

class AdaptiveLoop:
    """Замкнутый адаптационный контур."""
    
    def __init__(self, components: Optional[Dict[str, List[Any]]] = None, memory_limit: int = 20):
        self.id = str(uuid.uuid4())
        self.components = {
            "structural": components.get("structural", []) if components else [],
            "catalytic": components.get("catalytic", []) if components else [],
            "informational": components.get("informational", []) if components else []
        }
        self.memory: List[AdaptationRecord] = []
        self.memory_limit = memory_limit
        self.state: Dict[str, Any] = {"fitness": 1.0, "stability": 1.0}
    
    def is_closed(self, min_counts: Optional[Dict[str, int]] = None) -> bool:
        mc = min_counts or {"structural": 1, "catalytic": 1, "informational": 1}
        return all(len(self.components[k]) >= mc[k] for k in mc)
    
    def evaluate_fitness(self, context: Dict[str, Any]) -> float:
        return float(self.state.get("fitness", 1.0))
    
    def adapt(self, perturbation: Perturbation, generate_configs: Callable, test_config: Callable, apply_config: Callable) -> AdaptationRecord:
        before_cfg = self.snapshot_config()
        success = False
        after_cfg = before_cfg
        for cfg in generate_configs(self, perturbation):
            if test_config(self, cfg, perturbation):
                apply_config(self, cfg)
                after_cfg = cfg
                success = True
                break
        record = AdaptationRecord(perturbation, before_cfg, after_cfg, success, self.evaluate_fitness({}) - (before_cfg.get("fitness",1.0)))
        self._store_record(record)
        return record
    
    def replicate(self, mutation_rate: float = 0.05) -> "AdaptiveLoop":
        child = AdaptiveLoop(copy.deepcopy(self.components), self.memory_limit)
        child.memory = [copy.deepcopy(r) for r in self.memory[-3:]]
        return child
    
    def _store_record(self, rec: AdaptationRecord):
        self.memory.append(rec)
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)
    
    def snapshot_config(self) -> Dict[str, Any]:
        return {"fitness": self.state.get("fitness",1.0), "counts": {k: len(v) for k,v in self.components.items()}}
