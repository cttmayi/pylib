import asyncio


def sync(func, *args, **kwargs):
    return asyncio.run(func(*args, **kwargs))


if __name__ == "__main__":

    async def async_function(param1, param2):
        await asyncio.sleep(1)
        return f"Hello, {param1} and {param2}!"

    result = sync(async_function, "Alice", "Bob")
    print(result)