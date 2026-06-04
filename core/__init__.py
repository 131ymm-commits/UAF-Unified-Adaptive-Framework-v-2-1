"""UAF Core — формальные сущности первого уровня."""

from .loop import AdaptiveLoop, Perturbation, AdaptationRecord
from .levels import (
    MultiLevelSystem, LevelId, LevelState,
    LevelTransition, EmergenceEvent,
)
from .tipping import TippingDetector, TippingIndicator, TippingEvent
from .active_inference import (
    ActiveExperimenter, ExperimentProposal, ExperimentResult,
)

__all__ = [
    "AdaptiveLoop", "Perturbation", "AdaptationRecord",
    "MultiLevelSystem", "LevelId", "LevelState", "LevelTransition", "EmergenceEvent",
    "TippingDetector", "TippingIndicator", "TippingEvent",
    "ActiveExperimenter", "ExperimentProposal", "ExperimentResult",
]
