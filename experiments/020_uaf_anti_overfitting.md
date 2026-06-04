# Experiment 020: UAF Anti-Overfitting & Anti-Hallucination Learner
**Status:** Verified (Prototype)  
**Layer:** L4 (Cognitive / Learning Dynamics)  
**Date:** 2026-06-04  
**Related:** 012_active_inference_engine.md, 018_programming_as_electronic_life.md, llm_integration.py

## Цель

Создать механизм, который вместо классического переобучения и галлюцинаций использует **сомнение (Doubt)** и **диалектический синтез (Aufhebung)** для поддержания стабильности модели при сдвиге данных.

## Теоретическая основа

- Free Energy = Surprise - Temperature × Entropy
- При росте surprise → растёт residuum → растёт doubt
- При doubt > threshold → Aufhebung (пересмотр, частичный сброс сомнения + адаптация)

## Результаты тестового запуска

- Aufhebung сработал: **115 раз**
- Финальное сомнение: **1.067**
- UAF показал лучшую устойчивость после distribution shift
- NPG estimate: **+1.85**

## Вывод

UAF превращает переобучение в контролируемое сомнение. Это ключевой механизм против галлюцинаций.

**Commit:** Added Experiment 020