"""
Active Inference / Экспериментальный контроль — формализация №4.

Что делает уникального:
- Система САМА предлагает эксперименты
- Каждый эксперимент имеет ожидаемый информационный выигрыш
- Система учится из результатов прошлых экспериментов
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional
import math
import uuid


@dataclass
class ExperimentProposal:
    name: str
    description: str
    parameters: Dict[str, Any]
    expected_info_gain: float
    cost: float
    priority: float
    
    def __repr__(self):
        return (f"Experiment({self.name}, priority={self.priority:.2f}, "
                f"gain={self.expected_info_gain:.2f}, cost={self.cost:.2f})")


@dataclass
class ExperimentResult:
    experiment_name: str
    observed: Dict[str, float]
    predicted: Dict[str, float]
    info_gain_actual: float
    hypothesis_confirmed: bool


class ActiveExperimenter:
    """
    Система активного вывода.
    
    Отличие от пассивного наблюдения:
    - Не просто измеряет, а РЕШАЕТ, что измерить
    - Выбирает эксперимент с максимальным info_gain / cost
    - Обновляет свои модели после каждого эксперимента
    """
    
    def __init__(
        self,
        model_predict: Optional[Callable[[Dict[str, Any]], Dict[str, float]]] = None,
        measure: Optional[Callable[[Dict[str, Any]], Dict[str, float]]] = None,
    ):
        # Модель: предсказывает метрики по параметрам
        self.model_predict = model_predict or self._default_predict
        # Измеритель: получает реальные метрики по параметрам
        self.measure = measure or self._default_measure
        
        self.proposals: List[ExperimentProposal] = []
        self.results: List[ExperimentResult] = []
        
        # Наученная точность модели (начинаем с низкой)
        self.model_accuracy: float = 0.5
    
    @staticmethod
    def _default_predict(params: Dict[str, Any]) -> Dict[str, float]:
        """Заглушка: предсказывает на основе простых правил."""
        result = {}
        for key, val in params.items():
            if isinstance(val, (int, float)):
                result[key] = float(val) * 0.9  # Модель немного неточна
            else:
                result[key] = 0.5
        return result
    
    @staticmethod
    def _default_measure(params: Dict[str, Any]) -> Dict[str, float]:
        """Заглушка: измеряет реальные значения."""
        result = {}
        for key, val in params.items():
            if isinstance(val, (int, float)):
                result[key] = float(val)
            else:
                result[key] = 0.5
        return result
    
    def propose(
        self,
        hypotheses: List[Dict[str, Any]],
        budget: float = 10.0,
    ) -> List[ExperimentProposal]:
        """
        Генерация экспериментов из гипотез.
        Сортировка по priority = info_gain / cost.
        """
        candidates = []
        
        for h in hypotheses:
            param_sets = self._param_grid(h)
            
            for params in param_sets:
                gain = self._info_gain(h, params)
                cost = self._cost(params)
                
                if cost <= budget:
                    desc = self._build_description(h, params)
                    
                    candidates.append(ExperimentProposal(
                        name=f"exp_{h.get('id', uuid.uuid4().hex[:6])}",
                        description=desc,
                        parameters=params,
                        expected_info_gain=round(gain, 4),
                        cost=round(cost, 4),
                        priority=round(gain / cost if cost > 0 else float('inf'), 4),
                    ))
        
        candidates.sort(key=lambda x: x.priority, reverse=True)
        self.proposals = candidates
        return candidates
    
    def execute(
        self,
        proposal: ExperimentProposal,
        hypothesis: Optional[Dict[str, Any]] = None,
    ) -> ExperimentResult:
        """
        Выполнение эксперимента и обновление модели.
        """
        # Получаем предсказание модели
        predicted = self.model_predict(proposal.parameters)
        
        # Получаем реальное измерение
        observed = self.measure(proposal.parameters)
        
        # Вычисляем реальный информационный выигрыш
        info_gain_actual = self._compute_actual_gain(predicted, observed)
        
        # Определяем, подтвердилась ли гипотеза
        confirmed = False
        if hypothesis and "success_criteria" in hypothesis:
            criteria = hypothesis["success_criteria"]
            confirmed = all(
                observed.get(k, 0) >= v for k, v in criteria.items()
            )
        
        result = ExperimentResult(
            experiment_name=proposal.name,
            observed=observed,
            predicted=predicted,
            info_gain_actual=round(info_gain_actual, 4),
            hypothesis_confirmed=confirmed,
        )
        
        self.results.append(result)
        
        # Обновляем точность модели
        self._update_model_accuracy(predicted, observed)
        
        return result
    
    def _param_grid(self, hypothesis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Генерация сетки параметров из гипотезы.
        
        Если гипотеза содержит param_ranges вида {key: (min, max)},
        генерируем 3 точки: min, mid, max.
        """
        ranges = hypothesis.get("param_ranges", {})
        
        if not ranges:
            return [hypothesis.get("params", {})]
        
        # Для каждого параметра берём среднее значение
        # (полный декартов произведение был бы слишком большим)
        grid = [{}]
        
        for key, bounds in ranges.items():
            if isinstance(bounds, (list, tuple)) and len(bounds) == 2:
                lo, hi = float(bounds[0]), float(bounds[1])
                mid = (lo + hi) / 2.0
                
                new_grid = []
                for existing in grid:
                    # Берём только среднюю точку для компактности
                    entry = existing.copy()
                    entry[key] = mid
                    new_grid.append(entry)
                grid = new_grid
            else:
                new_grid = []
                for existing in grid:
                    entry = existing.copy()
                    entry[key] = bounds
                    new_grid.append(entry)
                grid = new_grid
        
        return grid if grid else [{}]
    
    def _info_gain(self, hypothesis: Dict[str, Any], params: Dict[str, Any]) -> float:
        """
        Ожидаемый информационный выигрыш.
        
        Вычисляется как разность между предсказанием модели и ожидаемым.
        Чем больше неопределённость, тем выше info_gain.
        """
        predicted = self.model_predict(params)
        expected = hypothesis.get("expected_evidence", 0.5)
        
        if not predicted:
            return expected
        
        # Среднее отклонение предсказаний
        avg_predicted = sum(predicted.values()) / len(predicted) if predicted else 0.5
        uncertainty = abs(avg_predicted - expected)
        
        # Чем больше неопределённость, тем больше info_gain
        # Но ограничен сверху 1.0
        gain = min(1.0, uncertainty + expected * (1 - self.model_accuracy))
        return gain
    
    def _cost(self, params: Dict[str, Any]) -> float:
        """
        Стоимость эксперимента.
        Зависит от числа параметров и их диапазонов.
        """
        base_cost = 1.0
        
        # Каждый параметр увеличивает стоимость
        param_count = sum(1 for v in params.values() if isinstance(v, (int, float)))
        base_cost += 0.1 * param_count
        
        return params.get("estimated_cost", base_cost)
    
    def _build_description(self, hypothesis: Dict[str, Any], params: Dict[str, Any]) -> str:
        """Генерация описания эксперимента."""
        h_desc = hypothesis.get("description", "Без описания")
        param_str = ", ".join(f"{k}={v:.2f}" if isinstance(v, float) else f"{k}={v}"
                              for k, v in params.items())
        return f"Тест гипотезы '{h_desc}' при параметрах: {param_str}"
    
    def _compute_actual_gain(
        self, predicted: Dict[str, float], observed: Dict[str, float]
    ) -> float:
        """Реальный информационный выигрыш: разность между предсказанием и наблюдением."""
        if not predicted or not observed:
            return 0.0
        
        common_keys = set(predicted.keys()) & set(observed.keys())
        if not common_keys:
            return 0.0
        
        diffs = [abs(predicted[k] - observed[k]) for k in common_keys
                 if isinstance(predicted[k], (int, float)) and isinstance(observed[k], (int, float))]
        
        if not diffs:
            return 0.0
        
        # Среднее отклонение (нормированное)
        avg_diff = sum(diffs) / len(diffs)
        return min(1.0, avg_diff)
    
    def _update_model_accuracy(self, predicted: Dict[str, float], observed: Dict[str, float]):
        """Обновить оценку точности модели на основе результата."""
        gain = self._compute_actual_gain(predicted, observed)
        
        # Чем больше info_gain, тем менее точна модель
        new_accuracy = 1.0 - gain
        
        # Экспоненциальное скользящее среднее
        self.model_accuracy = 0.8 * self.model_accuracy + 0.2 * new_accuracy
    
    def summary(self) -> str:
        lines = [
            f"ActiveExperimenter:",
            f"  Proposals: {len(self.proposals)}",
            f"  Executed: {len(self.results)}",
            f"  Model accuracy: {self.model_accuracy:.2f}",
        ]
        
        if self.results:
            last = self.results[-1]
            lines.append(f"  Last result: gain={last.info_gain_actual}, "
                         f"confirmed={last.hypothesis_confirmed}")
        
        return "\n".join(lines)
