```python
#!/usr/bin/env python3
"""
UAF Context Loader — система автоматического внедрения контекста UAF в запросы к ИИ.

Использование:
    from uaf_context_loader import UAFContext
    
    ctx = UAFContext("Создать симуляцию рака")
    print(ctx.prompt_for_gpt())      # Для ChatGPT
    print(ctx.prompt_for_claude())   # Для Claude
    print(ctx.prompt_for_any_llm())  # Универсальный
"""

import json
from typing import Dict, Any, Optional

class UAFContext:
    """Контекст UAF для встраивания в любой запрос к ИИ."""
    
    REPO_URL = "https://github.com/131ymm-commits/UAF-Unified-Adaptive-Framework-v-2-1"
    
    # Минимальный контекст UAF (на русском, компактный)
    UAF_CORE = {
        "name": "Unified Adaptive Framework",
        "version": "2.1",
        "key_concepts": {
            "AdaptiveLoop": (
                "Замкнутый контур из трёх компонентов: "
                "structural (структура), catalytic (катализ), informational (информация). "
                "Замкнутость = closure_degree (0..1)."
            ),
            "TippingPoint": (
                "Пороговый переход: когда closure_degree падает ниже порога, "
                "система скачком меняет состояние (молодость → старость, здоровье → болезнь)."
            ),
            "MultiLevel": (
                "L0 (молекулы) → L1 (клетки) → L2 (ткани) → L3 (организм). "
                "Каждый уровень — AdaptiveLoop следующего порядка."
            ),
            "ActiveExperimenter": (
                "Система выбора экспериментов на основе информационного выигрыша. "
                "Система сама предлагает, что проверить дальше."
            ),
        },
        "repo": REPO_URL,
    }
    
    def __init__(self, task: str, format_type: str = "code_with_description"):
        self.task = task
        self.format_type = format_type
        self.context_json = json.dumps(self.UAF_CORE, ensure_ascii=False, indent=2)
    
    def prompt_for_gpt(self) -> str:
        """Промпт для ChatGPT/GPT-4."""
        return f"""
# Контекст: Unified Adaptive Framework

Ты работаешь с научной теорией **Unified Adaptive Framework (UAF)**. 
Вот её ключевые концепции (JSON):

```json
{self.context_json}
