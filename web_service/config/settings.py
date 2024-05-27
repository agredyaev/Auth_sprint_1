from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

# Components definition
include(
    "components/application_definition.py",
    "components/database.py",
    "components/password_validation.py",
    "components/locale_settings.py",
    "components/secure_settings.py",
    "components/other_settings.py",
)
