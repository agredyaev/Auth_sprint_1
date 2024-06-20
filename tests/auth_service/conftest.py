BASE_PATH = "tests.auth_service.src.fixtures"

pytest_plugins = (
    f"{BASE_PATH}.asyncio",
    f"{BASE_PATH}.redis",
    f"{BASE_PATH}.aiohttp",
    f"{BASE_PATH}.user",
    f"{BASE_PATH}.role",
    f"{BASE_PATH}.pg",
)
