from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Callable
import numpy as np

@dataclass
class TippingIndicator:
    name: str
    compute: Callable[[Dict[str, Any]], float]
    threshold: float
    direction: str  # "increase" or "decrease"

@dataclass
class TippingEvent:
    name: str
    indicators_triggered: List[str]
    time: float
    context: Dict[str, Any]

class TippingDetector:
    def __init__(self):
        self.indicators: List[TippingIndicator] = []
        self.history: List[Dict[str, float]] = []
        self.events: List[TippingEvent] = []
    
    def add_indicator(self, ind: TippingIndicator):
        self.indicators.append(ind)
    
    def update(self, state: Dict[str, Any], time: float) -> List[TippingEvent]:
        new_vals = {}
        triggered = []
        for ind in self.indicators:
            try:
                v = float(ind.compute(state))
            except:
                v = 0.0
            new_vals[ind.name] = v
            if ind.direction == "increase" and v >= ind.threshold:
                triggered.append(ind.name)
            if ind.direction == "decrease" and v <= ind.threshold:
                triggered.append(ind.name)
        self.history.append(new_vals)
        events = []
        if triggered:
            events.append(TippingEvent("tipping_candidate", triggered, time, state.copy()))
            self.events.extend(events)
        return events
