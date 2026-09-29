# Пустой файл-маркер: pytest использует папку с conftest.py как
# корень проекта и сам добавляет её в sys.path. Благодаря этому
# `from clients import Client` работает как при запуске
# `python -m pytest`, так и при запуске просто `pytest`.
