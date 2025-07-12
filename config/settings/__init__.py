from decouple import config

ENVIRONMENT = config("ENVIRONMENT", default="local")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "test":
    from .test import *
else:
    from .local import *
