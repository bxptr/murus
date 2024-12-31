from dataclasses import dataclass

@dataclass
class Config:
    JWT_SECRET_KEY = "SUP3R-SECURE-DEFAULT"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_DELTA_SECONDS = 3600

    SERVER_CERT = "./certs/server.crt"
    SERVER_KEY = "./certs/server.key"
    CA_CERT = "./certs/ca.crt"
    REQUIRE_CLIENT_CERT = True 

    LOG_LEVEL = "INFO" 

