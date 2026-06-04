# UAF Unified Prompt System v1.0

## Для ИИ (обработка запроса)

Когда ты видишь `@UAF_CONTEXT`:

1. Загрузи контекст:
   - AdaptiveLoop = структура + катализ + информация, замкнутость = closure_degree (0..1)
   - TippingPoint = пороговый переход при падении closure_degree ниже порога
   - MultiLevel = L0→L1→L2→L3
   - ActiveExperimenter = система выбора экспериментов

2. Выдай ответ **строго** в формате MANDATORY OUTPUT FORMAT.

## MANDATORY OUTPUT FORMAT

[НАЗВАНИЕ ЭКСПЕРИМЕНТА]

1. Что это? (2-3 абзаца на русском)
2. Гипотеза UAF (AdaptiveLoop, TippingPoint, Prediction)
3. Код (Python, готов для Colab, только numpy/matplotlib/random, без ошибок)
4. Инструкция запуска (4 шага)
5. Результаты (пример вывода)
6. Что получилось? (3-5 абзацев)
7. Почему это UAF? (closure_degree, типпинг и т.д.)

Репозиторий: https://github.com/131ymm-commits/UAF-Unified-Adaptive-Framework-v-2-1
