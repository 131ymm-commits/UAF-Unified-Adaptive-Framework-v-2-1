import random
import numpy as np
import copy
from typing import Dict, List, Any
from abc import ABC, abstractmethod

# ====================== UAF CORE ======================
class UAFSystem(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.state = {}
        self.history = []
        self.adaptation_level = 0

    @abstractmethod
    def adapt(self, perturbation: Any) -> bool:
        pass

    @abstractmethod
    def replicate(self) -> 'UAFSystem':
        pass

    def is_alive(self) -> bool:
        return self.adaptation_level >= 3


# ====================== MOLECULES ======================
class Molecule:
    def __init__(self, molecule_type: str, properties: Dict):
        self.type = molecule_type
        self.properties = properties
        self.state = "free"
        self.position = (0.0, 0.0)

    def interact(self, other: 'Molecule') -> bool:
        return False  # будет переопределено в наследниках


class Lipid(Molecule):
    def __init__(self):
        super().__init__("lipid", {
            "chain_length": random.randint(12, 18),
            "saturation": random.uniform(0, 1)
        })


class Catalyst(Molecule):
    def __init__(self):
        super().__init__("catalyst", {
            "efficiency": random.uniform(0.1, 0.9),
            "specificity": random.choice(["lipid", "nucleotide", "peptide"])
        })


class Nucleotide(Molecule):
    def __init__(self):
        super().__init__("nucleotide", {
            "sequence": ''.join(random.choices("ACGU", k=6)),
            "stability": random.uniform(0.3, 0.8)
        })


# ====================== ADAPTATION LOOP ======================
class AdaptationLoop:
    def __init__(self):
        self.catalytic_components = []
        self.info_components = []
        self.structural_components = []
        self.adaptation_memory = []

    def add_catalyst(self, cat: Catalyst):
        self.catalytic_components.append(cat)

    def add_info_polymer(self, poly: Nucleotide):
        self.info_components.append(poly)

    def is_closed(self) -> bool:
        return len(self.catalytic_components) > 0 and len(self.info_components) > 0

    def adapt_to_perturbation(self, perturbation: Dict) -> bool:
        success = random.random() < 0.75  # упрощённая вероятность успеха
        if success:
            self.adaptation_memory.append({
                "perturbation": perturbation,
                "success": True
            })
            self.adaptation_level = min(3, self.adaptation_level + 1)
        return success

    def replicate_with_inheritance(self) -> 'AdaptationLoop':
        child = AdaptationLoop()
        for cat in self.catalytic_components:
            if random.random() > 0.12:  # мутация
                child.add_catalyst(copy.deepcopy(cat))
        for poly in self.info_components:
            if random.random() > 0.07:
                child.add_info_polymer(copy.deepcopy(poly))
        child.adaptation_memory = self.adaptation_memory[-2:]
        return child


# ====================== ENVIRONMENT ======================
class PrebioticEnvironment:
    def __init__(self, size: tuple = (100, 100)):
        self.size = size
        self.molecules: List[Molecule] = []
        self.ensembles = []

    def add_molecule(self, mol: Molecule, pos: tuple):
        mol.position = pos
        self.molecules.append(mol)

    def step(self):
        # Простая модель: случайные взаимодействия
        if random.random() < 0.15 and len(self.molecules) > 20:
            # Формирование простого ансамбля
            self.ensembles.append({"molecules": random.sample(self.molecules, k=min(15, len(self.molecules)))})


# ====================== MAIN SIMULATION ======================
class LifeEmergenceSimulation:
    def __init__(self):
        self.environment = PrebioticEnvironment()
        self.time = 0.0
        self.life_formed = False
        self.events = []
        self._initialize()

    def _initialize(self):
        # Липиды
        for _ in range(1200):
            lipid = Lipid()
            pos = (random.uniform(0, 99), random.uniform(0, 99))
            self.environment.add_molecule(lipid, pos)

        # Катализаторы
        for _ in range(250):
            cat = Catalyst()
            pos = (random.uniform(0, 99), random.uniform(0, 99))
            self.environment.add_molecule(cat, pos)

        # Нуклеотиды
        for _ in range(600):
            nuc = Nucleotide()
            pos = (random.uniform(0, 99), random.uniform(0, 99))
            self.environment.add_molecule(nuc, pos)

    def run(self, max_time: int = 10000):
        print("Запуск симуляции появления жизни (UAF v2.1)...\n")

        while self.time < max_time and not self.life_formed:
            self.environment.step()
            self.time += 0.1

            if self.time % 100 < 0.1:
                print(f"Time: {self.time:.1f} | Molecules: {len(self.environment.molecules)} | Ensembles: {len(self.environment.ensembles)}")

            # Проверка возникновения жизни
            if len(self.environment.ensembles) > 5 and random.random() < 0.08:
                loop = AdaptationLoop()
                # Заполняем контур
                for _ in range(4):
                    loop.add_catalyst(Catalyst())
                for _ in range(3):
                    loop.add_info_polymer(Nucleotide())

                if loop.is_closed():
                    perturbation = {"type": "temperature", "value": 12}
                    if loop.adapt_to_perturbation(perturbation):
                        self.life_formed = True
                        self.events.append({
                            "time": self.time,
                            "event": "LIFE_EMERGENCE",
                            "details": "Closed adaptation loop formed"
                        })
                        print(f"\n*** LIFE EMERGED at time {self.time:.1f} ***")
                        break

        if not self.life_formed:
            print(f"\nЖизнь не возникла за {max_time} единиц времени.")

        return self


# ====================== ЗАПУСК ======================
if __name__ == "__main__":
    sim = LifeEmergenceSimulation()
    sim.run(max_time=8000)

    print("\n" + "="*60)
    print("Симуляция завершена")
    print(f"Результат: {'ЖИЗНЬ ВОЗНИКЛА' if sim.life_formed else 'Жизнь не возникла'}")
    print("="*60)
