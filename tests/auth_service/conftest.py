BASE_PATH = "tests.fastapi_service.src.fixtures"

pytest_plugins = (
    f"{BASE_PATH}.asyncio",
    f"{BASE_PATH}.redis",
    f"{BASE_PATH}.elastic",
    f"{BASE_PATH}.aiohttp",
    f"{BASE_PATH}.film",
    f"{BASE_PATH}.genre",
    f"{BASE_PATH}.person",
)
