"""
Пороговые переходы (Tipping Points) — формализация №3.

Что делает уникального:
- Измеримые индикаторы, а не субъективные оценки
- Защита от повторного срабатывания
- Прогнозирование расстояния до порога
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional


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
    phase_from: str = ""
    phase_to: str = ""


class TippingDetector:
    """
    Детектор пороговых переходов.
    
    Считает:
    - Какие индикаторы превысили порог
    - Как далеко система до следующего порога
    - Какие эксперименты помогут приблизиться к переходу
    """
    
    def __init__(self):
        self.indicators: List[TippingIndicator] = []
        self.history: List[Dict[str, float]] = []
        self.events: List[TippingEvent] = []
        # Какие индикаторы уже срабатывали (защита от повторов)
        self._triggered: set = set()
    
    def add_indicator(self, ind: TippingIndicator):
        self.indicators.append(ind)
    
    def reset(self):
        """Полный сброс истории и событий."""
        self.history.clear()
        self.events.clear()
        self._triggered.clear()
    
    def reset_triggers(self):
        """Сбросить триггеры, но сохранить историю."""
        self._triggered.clear()
    
    def update(self, state: Dict[str, Any], time: float) -> List[TippingEvent]:
        """Обновление. Возвращает только НОВЫЕ события."""
        new_vals = {}
        triggered = []
        
        for ind in self.indicators:
            try:
                v = float(ind.compute(state))
            except (TypeError, ValueError, KeyError):
                v = 0.0
            
            new_vals[ind.name] = v
            
            # Проверяем порог и не срабатываем повторно
            if ind.name not in self._triggered:
                if ind.direction == "increase" and v >= ind.threshold:
                    triggered.append(ind.name)
                elif ind.direction == "decrease" and v <= ind.threshold:
                    triggered.append(ind.name)
        
        self.history.append(new_vals)
        events = []
        
        if triggered:
            event = TippingEvent(
                name=f"tipping_{'_'.join(sorted(triggered))}",
                indicators_triggered=triggered,
                time=time,
                context=state.copy(),
            )
            self.events.append(event)
            events.append(event)
            
            # Помечаем как сработавшие
            for name in triggered:
                self._triggered.add(name)
        
        return events
    
    def distance_to_threshold(self, state: Dict[str, Any]) -> Dict[str, float]:
        """Расстояние каждого индикатора до порога (0 = достигнут)."""
        distances = {}
        for ind in self.indicators:
            try:
                v = float(ind.compute(state))
            except (TypeError, ValueError, KeyError):
                v = 0.0
            
            if ind.direction == "increase":
                distances[ind.name] = max(0.0, ind.threshold - v)
            else:
                distances[ind.name] = max(0.0, v - ind.threshold)
        
        return distances
    
    def proximity_score(self, state: Dict[str, Any]) -> float:
        """
        Общая близость к порогу: 0.0 (далеко) -> 1.0 (все достигнуты).
        """
        if not self.indicators:
            return 0.0
        
        distances = self.distance_to_threshold(state)
        
        # Среднее выполнение
        scores = []
        for ind in self.indicators:
            try:
                v = float(ind.compute(state))
            except (TypeError, ValueError, KeyError):
                v = 0.0
            
            if ind.direction == "increase":
                scores.append(min(1.0, v / ind.threshold) if ind.threshold > 0 else 0.0)
            else:
                scores.append(min(1.0, 1.0 - v) if ind.threshold > 0 else 0.0)
        
        return sum(scores) / len(scores)
    
    def suggest_action(self, state: Dict[str, Any]) -> Optional[str]:
        """Предложить действие для достижения порога."""
        distances = self.distance_to_threshold(state)
        
        if not distances:
            return None
        
        # Находим самый отстающий индикатор
        weakest = max(distances, key=distances.get)
        
        if distances[weakest] <= 0:
            return None  # Все пороги достигнуты
        
        return (
            f"Самый отстающий индикатор: '{weakest}' "
            f"(расстояние до порога: {distances[weakest]:.3f}). "
            f"Необходимо увеличить этот показатель."
        )
    
    def summary(self) -> str:
        lines = [f"TippingDetector: {len(self.indicators)} indicators, "
                 f"{len(self.events)} events, "
                 f"{len(self._triggered)} triggered"]
        if self.history:
            last = self.history[-1]
            lines.append(f"  Last values: {last}")
        return "\n".join(lines)
