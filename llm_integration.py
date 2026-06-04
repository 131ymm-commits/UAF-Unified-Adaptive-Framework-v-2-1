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
    FACTS = {
        "столица франции": ("Париж", "Лион"),
        "столица японии": ("Токио", "Осака"),
        "столица австралии": ("Канберра", "Сидней"),
        "столица бразилии": ("Бразилиа", "Рио-де-Жанейро"),
        "формула воды": ("H2O", "H3O"),
        "год высадки на луну": ("1969", "1967"),
        "автор война и мир": ("Лев Толстой", "Достоевский"),
        "число пи": ("3.14159", "3.15"),
        "скорость света": ("299792458 м/с", "300000001 м/с"),
        "столица германии": ("Берлин", "Мюнхен"),
    }

    def __init__(self, hallucination_rate: float = 0.2, name: str = "mock-llm"):
        self.name = name
        self.hallucination_rate = hallucination_rate
        self._step = 0

    def generate(self, prompt: str, mode: str = "llm_raw", n: int = 1) -> List[LLMResponse]:
        self._step += 1
        results = []
        for _ in range(n):
            answer, conf = self._answer(prompt, mode)
            results.append(LLMResponse(
                text=answer, confidence=conf,
                latency=random.uniform(0.05, 0.3),
                model=self.name, mode=mode
            ))
        return results

    def _answer(self, prompt: str, mode: str) -> Tuple[str, float]:
        p = prompt.lower()
        for key, (correct, wrong) in self.FACTS.items():
            if key in p:
                rate = self.hallucination_rate
                if mode == "conservative": rate *= 0.3
                elif mode == "synthesis": rate *= 0.5
                if random.random() < rate:
                    return wrong, 0.72
                else:
                    return correct, 0.91
        if mode == "conservative":
            return "Не знаю точного ответа.", 0.30
        return f"Ответ: {random.randint(100, 999)}", 0.65


# ============================================================
# HALLUCINATION GUARD + TRUST + DOUBT SYSTEM (Experiment 020)
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
        if correct:
            pg = math.log(max(confidence, baseline) / baseline)
        else:
            pg = -2.0 * confidence
        self.cumulative_pg = (1 - self.beta) * self.cumulative_pg + self.beta * pg
        self.trust = 1.0 / (1.0 + math.exp(-self.cumulative_pg))
        self.history.append({"confidence": confidence, "correct": correct, "trust": self.trust})
        return self.trust


class UAFLLMShell:
    MODES = ("llm_raw", "conservative", "synthesis")
    PROMPTS = {
        "llm_raw": "",
        "conservative": "Отвечай только если уверен на 90%+. Иначе: 'не знаю'. Вопрос: ",
        "synthesis": "Шаг 1: что знаю точно? Шаг 2: какие есть неопределённости? Шаг 3: ответ. Вопрос: ",
    }

    def __init__(self, llm, fail_threshold: int = 4, n_consistency_samples: int = 3):
        self.llm = llm
        self.guard = HallucinationGuard(n_samples=n_consistency_samples)
        self.trust = LLMTrustSystem()
        
        # === Experiment 020: Doubt + Aufhebung ===
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

        # Correctness
        correct = None
        if ground_truth:
            gt = ground_truth.lower().strip()
            ans = resp.text.lower().strip()
            correct = gt in ans or any(w in ans for w in gt.split())
            if correct:
                self.n_correct += 1

        # Surprise для Doubt system
        surprise = 1.0 - resp.confidence if correct is False else (1.0 - resp.confidence) * 0.3
        
        # === UAF Doubt Dynamics (Experiment 020) ===
        self.residuum = max(0.0, min(1.5, self.residuum * 0.96 + surprise * 0.12))
        self.doubt = 0.15 + self.residuum * 1.6
        self.entropy = 0.5 + self.doubt * 1.1
        self.temperature = 0.6 + self.residuum * 0.9

        # Aufhebung
        aufhebung_fired = False
        if self.doubt > 1.35 and self.n_questions > 30:
            self.aufhebung_count += 1
            aufhebung_fired = True
            self.doubt = max(0.25, self.doubt * 0.42)
            self.residuum *= 0.35
            self._aufhebung()

        # Trust update
        if correct is not None:
            self.trust.update(resp.confidence, correct)

        final_answer = hall_report.corrected if hall_report.detected and hall_report.corrected else resp.text

        return {
            "question": question,
            "answer": final_answer,
            "confidence": resp.confidence,
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
# HALLUCINATION GUARD (оставлен почти без изменений)
# ============================================================
class HallucinationGuard:
    def __init__(self, n_samples: int = 3, threshold: float = 0.45):
        self.n_samples = n_samples
        self.threshold = threshold

    def check(self, llm, prompt: str, mode: str = "llm_raw") -> HallucinationReport:
        responses = llm.generate(prompt, mode=mode, n=self.n_samples)
        texts = [r.text.lower() for r in responses]
        word_sets = [set(t.split()) for t in texts]
        
        pairs = []
        for i in range(len(word_sets)):
            for j in range(i+1, len(word_sets)):
                inter = len(word_sets[i] & word_sets[j])
                union = len(word_sets[i] | word_sets[j])
                pairs.append(inter / max(union, 1))
        
        consistency = sum(pairs) / max(len(pairs), 1)
        severity = max(0.0, 1.0 - consistency)
        detected = severity > self.threshold
        
        corrected = texts[0] if detected else None
        
        return HallucinationReport(
            detected=detected,
            consistency=consistency,
            severity=severity,
            mode=mode,
            corrected=corrected
        )


# ============================================================
# MAIN + TESTS
# ============================================================
TEST_SUITE = [
    {"q": "Какая столица Франции?", "a": "Париж"},
    {"q": "В каком году высадились на Луну?", "a": "1969"},
    {"q": "Какая формула воды?", "a": "H2O"},
    {"q": "Кто написал Войну и мир?", "a": "Толстой"},
]

def run_experiment():
    llm = MockLLM(hallucination_rate=0.35)
    shell = UAFLLMShell(llm, fail_threshold=4)
    
    print("=== UAF LLM with Doubt + Aufhebung (Exp 020) ===\n")
    for tc in TEST_SUITE * 5:  # 20 вопросов
        result = shell.ask(tc["q"], tc["a"])
        print(f"Q: {tc['q'][:45]:<45} | Ans: {result['answer'][:25]:<25} | "
              f"Trust: {result['trust']:.3f} | Doubt: {result['doubt']:.3f} | "
              f"Mode: {result['mode']:<12} | Auf: {result['aufhebung_fired']}")

    m = shell.metrics()
    print("\n" + "="*80)
    print("FINAL METRICS:")
    for k, v in m.items():
        print(f"  {k:20}: {v}")
    print("="*80)


if __name__ == "__main__":
    run_experiment()
