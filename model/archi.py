from dataclasses import dataclass
from model.retailers import Retailer

@dataclass
class Arco:
    arco1: Retailer
    arco2: Retailer
    peso: int