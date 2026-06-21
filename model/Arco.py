from dataclasses import dataclass

from model.Pilota import Pilota


@dataclass
class Arco:
    p1: Pilota
    p2: Pilota
    peso: int