# app/pipeline/config.py
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass(frozen=True)
class Settings:
    products_list: str = 'data/products.csv'

settings = Settings()