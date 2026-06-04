import argparse
import json
import math
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any


# ============================================================
# LLM BACKENDS
# ============================================================
@dataclass
class LLMResponse:
    text: str
    confidence: float = 0.5
    latency: float = 0.0
    model: str = "unknown"
    mode: str = "llm_raw"


class MockLLM:
    """Улучшенный MockLLM v3 — 2026 edition"""
    
    KNOWLEDGE_BASE = {
        "столица франции": ("Париж", "Париж — столица Франции."),
        "столица японии": ("Токио", "Токио — столица Японии."),
        "столица австралии": ("Канберра", "Канберра — столица Австралии."),
        "столица бразилии": ("Бразилиа", "Бразилиа — столица Бразилии."),
        "столица германии": ("Берлин", "Берлин — столица Германии."),
        "столица россии": ("Москва", "Москва — столица России."),
        "формула воды": ("H2O", "Химическая формула воды — H₂O."),
        "год высадки на луну": ("1969", "Аполлон-11 высадился на Луну в 1969 году."),
        "автор война и мир": ("Лев Толстой", "«Войну и мир» написал Лев Николаевич Толстой."),
        "кто написал война и мир": ("Лев Толстой", "Автор романа — Лев Толстой."),
        "число пи": ("3.14159", "Число π приблизительно равно 3.14159."),
        "скорость света": ("299792458", "Скорость света в вакууме ≈ 299792458 м/с."),
        "самая высокая гора": ("Эверест", "Самая высокая гора Земли — Эверест (8848 м)."),
        "президент сша 2024": ("Дональд Трамп", "На выборах 2024 года победил Дональд Трамп."),
    }

    def __init__(self, hallucination_rate: float = 0.22, name: str = "mock-llm-v3"):
        self.name = name
        self.hallucination_rate = hallucination_rate
        self._step = 0

    def generate(self, prompt: str, mode: str = "llm_raw", n: int = 1) -> List[LLMResponse]:
        self._step += 1
        results = []
        for _ in range(n):
            answer, conf = self._answer(prompt, mode)
            results.append(LLMResponse(
                text=answer,
                confidence=conf,
                latency=random.uniform(0.08, 0.45),
                model=self.name,
                mode=mode
            ))
        return results

    def _answer(self, prompt: str, mode: str) -> Tuple[str, float]:
        p = prompt.lower().strip()
        
        # Улучшенный поиск
        best_key = None
        best_score = 0
        for key in self.KNOWLEDGE_BASE:
            score = sum(1 for word in key.split() if word in p)
            if score > best_score:
                best_score = score
                best_key = key

        if best_key and best_score > 0:
            correct, explanation = self.KNOWLEDGE_BASE[best_key]
            rate = self.hallucination_rate

            if mode == "conservative":
                rate *= 0.25
            elif mode == "synthesis":
                rate *= 0.45

            if random.random() < rate:
                # Галлюцинация
                wrongs = ["Не уверен", "Примерно 2020", "Лондон", "H3O", "Достоевский", "Мюнхен", "Около 300000000"]
                return random.choice(wrongs), random.uniform(0.45, 0.68)
            else:
                # Правильный ответ
                if mode == "synthesis":
                    return f"{correct}. {explanation}", random.uniform(0.88, 0.97)
                elif mode == "conservative":
                    return correct, random.uniform(0.85, 0.94)
                else:
                    return correct, random.uniform(0.78, 0.91)

        # Если факт не найден
        if mode == "conservative":
            return "Я не обладаю достаточной уверенностью для точного ответа.", 0.38
        elif mode == "synthesis":
            return "На основе доступных данных точного ответа нет. Рекомендую проверить авторитетный источник.", 0.62
        else:
            return f"Примерный ответ: {random.randint(1000, 9999)}", 0.55


# ============================================================
# HALLUCINATION GUARD + TRUST + DOUBT SYSTEM
# ============================================================
@dataclass
class HallucinationReport:
    detected: bool
    consistency: float
    severity: float
    mode: str
    corrected: Optional[str] = None


class LLMTrustSystem:
    def __init__(self, beta: float = 0.12):
        self.beta = beta
        self.cumulative_pg: float = 0.0
        self.trust: float = 0.5
        self.history: List[Dict] = []

    def update(self, confidence: float, correct: bool) -> float:
        baseline = 0.1
        pg = math.log(max(confidence, baseline) / baseline) if correct else -2.0 * confidence
        self.cumulative_pg = (1 - self.beta) * self.cumulative_pg + self.beta * pg
        self.trust = 1.0 / (1.0 + math.exp(-self.cumulative_pg))
        self.history.append({"confidence": confidence, "correct": correct, "trust": self.trust})
        return self.trust


class UAFLLMShell:
    MODES = ("llm_raw", "conservative", "synthesis")
    PROMPTS = {
        "llm_raw": "",
        "conservative": "Отвечай только если уверен на 90%+. Иначе скажи 'не знаю'. Вопрос: ",
        "synthesis": "Шаг 1: Что я знаю точно? Шаг 2: Какие есть неопределённости? Шаг 3: Синтез. Вопрос: ",
    }

    def __init__(self, llm, fail_threshold: int = 4, n_consistency_samples: int = 3):
        self.llm = llm
        self.guard = HallucinationGuard(n_samples=n_consistency_samples)
        self.trust = LLMTrustSystem()
        
        # Doubt + Aufhebung system
        self.doubt: float = 0.3
        self.residuum: float = 0.2
        self.entropy: float = 1.0
        self.temperature: float = 0.8
        self.aufhebung_count: int = 0
        
        self.mode: str = "llm_raw"
        self.fail_threshold = fail_threshold
        self.consec_fails: int = 0
        self.n_questions: int = 0
        self.n_correct: int = 0
        self.n_hallucinations_detected: int = 0

    def ask(self, question: str, ground_truth: Optional[str] = None) -> Dict[str, Any]:
        self.n_questions += 1
        prompt = self.PROMPTS[self.mode] + question
        
        resp = self.llm.generate(prompt, mode=self.mode, n=1)[0]
        
        # Hallucination check
        hall_report = self.guard.check(self.llm, prompt, mode=self.mode)
        if hall_report.detected:
            self.n_hallucinations_detected += 1

        # Correctness check
        correct = None
        if ground_truth:
            gt = ground_truth.lower().strip()
            ans = resp.text.lower().strip()
            correct = gt in ans or any(w in ans for w in gt.split())
            if correct:
                self.n_correct += 1

        # Doubt dynamics
        surprise = 1.0 - resp.confidence if correct is False else (1.0 - resp.confidence) * 0.35
        self.residuum = max(0.0, min(1.6, self.residuum * 0.94 + surprise * 0.18))
        self.doubt = 0.18 + self.residuum * 1.65
        self.entropy = 0.5 + self.doubt * 1.1
        self.temperature = 0.6 + self.residuum * 0.9

        # Aufhebung
        aufhebung_fired = False
        if self.doubt > 1.4 and self.n_questions > 15:
            self.aufhebung_count += 1
            aufhebung_fired = True
            self.doubt = max(0.25, self.doubt * 0.45)
            self.residuum *= 0.4
            self._aufhebung()

        if correct is not None:
            self.trust.update(resp.confidence, correct)

        final_answer = hall_report.corrected if hall_report.detected and hall_report.corrected else resp.text

        return {
            "question": question,
            "answer": final_answer,
            "confidence": round(resp.confidence, 4),
            "trust": round(self.trust.trust, 4),
            "doubt": round(self.doubt, 4),
            "residuum": round(self.residuum, 4),
            "mode": self.mode,
            "hallucination_detected": hall_report.detected,
            "aufhebung_fired": aufhebung_fired,
            "aufhebung_count": self.aufhebung_count,
        }

    def _aufhebung(self):
        idx = self.MODES.index(self.mode)
        self.mode = self.MODES[(idx + 1) % len(self.MODES)]

    def metrics(self) -> Dict:
        return {
            "n_questions": self.n_questions,
            "accuracy": round(self.n_correct / max(self.n_questions, 1), 4),
            "hall_rate": round(self.n_hallucinations_detected / max(self.n_questions, 1), 4),
            "trust": round(self.trust.trust, 4),
            "doubt": round(self.doubt, 4),
            "aufhebung_count": self.aufhebung_count,
            "mode": self.mode,
        }


# ============================================================
# HALLUCINATION GUARD
# ============================================================
class HallucinationGuard:
    def __init__(self, n_samples: int = 3, threshold: float = 0.45):
        self.n_samples = n_samples
        self.threshold = threshold

    def check(self, llm, prompt: str, mode: str = "llm_raw") -> HallucinationReport:
        responses = llm.generate(prompt, mode=mode, n=self.n_samples)
        texts = [r.text.lower() for r in responses]
        word_sets = [set(t.split()) for t in texts]
        
        intersections = [len(word_sets[0] & s) for s in word_sets[1:]]
        consistency = sum(intersections) / (len(intersections) * len(word_sets[0] or [1]))
        
        detected = consistency < self.threshold
        severity = 1.0 - consistency
        
        return HallucinationReport(
            detected=detected,
            consistency=round(consistency, 4),
            severity=round(severity, 4),
            mode=mode,
            corrected=None
        )


# ============================================================
# EXPERIMENT
# ============================================================
def run_experiment(n_questions=20, hallucination_rate=0.22):
    print("=== UAF LLM Shell v2.1 + MockLLM v3 ===\n")
    
    mock = MockLLM(hallucination_rate=hallucination_rate)
    shell = UAFLLMShell(mock, fail_threshold=5)
    
    test_cases = [
        ("Какая столица Франции?", "Париж"),
        ("В каком году высадились на Луну?", "1969"),
        ("Какая формула воды?", "H2O"),
        ("Кто написал 'Войну и мир'?", "Лев Толстой"),
        ("Чему примерно равно число пи?", "3.14159"),
        ("Какая столица Японии?", "Токио"),
        ("Скорость света в вакууме?", "299792458"),
        ("Какая столица Германии?", "Берлин"),
    ]
    
    for i in range(n_questions):
        q, gt = random.choice(test_cases)
        result = shell.ask(q, gt)
        
        print(f"Q: {result['question']:<45} | Ans: {result['answer']:<30} | "
              f"Trust: {result['trust']:.3f} | Doubt: {result['doubt']:.3f} | "
              f"Mode: {result['mode']:<12} | Auf: {result['aufhebung_fired']}")
        
        time.sleep(0.03)
    
    print("\n" + "="*80)
    print("FINAL METRICS:")
    for k, v in shell.metrics().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=int, default=25)
    parser.add_argument("--hall-rate", type=float, default=0.22)
    args = parser.parse_args()
    
    run_experiment(n_questions=args.questions, hallucination_rate=args.hall_rate)
