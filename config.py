from dataclasses import dataclass


@dataclass
class Appsettings:
    GPT3_URL: str
    GPT3_AUTH_KEY: str

@dataclass
class Gpt3Config:
    url: str
    auth_key: str
