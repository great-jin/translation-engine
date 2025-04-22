from dataclasses import dataclass

@dataclass
class AppConfig:
    name: str
    description: str
    version: str
    host: str
    port: int
