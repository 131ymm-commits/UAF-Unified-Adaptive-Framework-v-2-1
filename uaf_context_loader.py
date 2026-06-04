#!/usr/bin/env python3
import json

class UAFContext:
    REPO_URL = "https://github.com/131ymm-commits/UAF-Unified-Adaptive-Framework-v-2-1"
    
    def __init__(self, task: str):
        self.task = task
    
    def prompt_for_any_llm(self) -> str:
        return f"""@UAF_CONTEXT

FRAMEWORK: Unified Adaptive Framework v2.1
REPO: {self.REPO_URL}

KEY_CONCEPTS:
AdaptiveLoop = closed loop (structure + catalysis + information)
closure_degree (0..1)
TippingPoint = threshold transition
MultiLevel = L0→L1→L2→L3

TASK: {self.task}

OUTPUT_FORMAT (exactly 7 sections, in Russian for explanations, code in Python):
1. Что это? (2-3 paragraphs)
2. Гипотеза UAF (AdaptiveLoop, TippingPoint, Prediction)
3. Код (complete, no errors, only numpy/matplotlib/random, Colab-ready)
4. Инструкция запуска
5. Результаты (example output)
6. Что получилось? (findings)
7. Почему это UAF? (closure_degree, tipping point)
"""

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python uaf_context_loader.py 'Your task description'")
        sys.exit(1)
    task = sys.argv[1]
    ctx = UAFContext(task)
    print(ctx.prompt_for_any_llm())

if __name__ == "__main__":
    main()
