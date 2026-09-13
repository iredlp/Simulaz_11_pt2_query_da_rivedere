from dataclasses import dataclass

from model.attori import Attori


@dataclass
class Arco:
    a1: str
    a2: str
    incasso: str

    def get_peso_numerico(self) -> float:
        """Pulisce la stringa e restituisce il valore float."""
        if not self.incasso:
            return 0.0
        # Rimuove simboli come '$', virgole e spazi
        cifre = "".join([c for c in str(self.incasso) if c.isdigit() or c == "."])
        return float(cifre) if cifre else 0.0