from dataclasses import dataclass

@dataclass
class TIVState:
    N: float      # nominal
    R: float      # risk
    C: float      # context
    H: float      # history
    alpha_R: float = 1.0
    alpha_C: float = 1.0
    alpha_H: float = 1.0

    def value_A(self) -> float:
        return self.N

    def value_B(self) -> float:
        return self.alpha_R * self.R + self.alpha_C * self.C + self.alpha_H * self.H

    def total(self) -> float:
        return self.value_A() + self.value_B()
