# create folder core

#create pyproject.toml file in core directory
# core/pyroject.toml
"""
[project]
name = "FastAPI-ToDo-app"
version = "0.116.1"
description = "A FastAPI-based service"
requires-python = "==3.12.4"
dependencies = [
  "fastapi[standard]",
  "uvicorn[standard]",
  "sqlalchemy",
  "pydantic>=2",
]

[tool.uv]
dev-dependencies = ["pytest", "httpx", "ruff"]
"""
"""
[tool.poetry]          # اگر Poetry استفاده کنی
authors = ["You <you@example.com>"]

[tool.poetry.dependencies]
python = "3.12.4"
fastapi = "*"
uvicorn = {extras = ["standard"]}
sqlalchemy = "*"
pydantic = "^2"

[tool.poetry.group.dev.dependencies]
pytest = "*"
httpx = "*"
ruff = "*"
"""
# in outside if core folder execute these command :
# python -m pip install --upgrade pip
# python -m pip install uv
# معمولاً باینری‌ها اینجاست، مطمئن شو به PATH اضافه شده:
# %USERPROFILE%\.local\bin  یا  %APPDATA%\Python\Python312\Scripts
# uv --version

# اگر هنوز شناسایی نشد، موقتاً می‌تونی این‌طوری صداش بزنی:
# python -m uv --version

# 2) ساخت/فعال‌سازی محیط مجازی با uv
# (اگر Python 3.12.4 را با خود uv می‌خواهی نصب کند:)
# uv python install 3.12.4



# حالا داخل ریشه‌ی پروژه‌ات (همان جایی که pyproject.toml هست—طبق اسکرین‌شات پوشه‌ی core/) برو و venv بساز:
# cd core
# uv venv --python 3.12.4


# uv sync

# create main.py

# uv run fastapi dev main.py


# روش ۱: استفاده از pip داخل venv
# اگر venv رو فعال کردی (.venv\Scripts\activate روی ویندوز):
# با uv خودش (راه مدرن‌تر)
# uv pip list
# uv pip freeze


# .venv\Scripts\activate
# mkdir F:\Git-Repository\FastAPI-ToDo-app\uv-cache
# $env:UV_CACHE_DIR = "F:\Git-Repository\FastAPI-ToDo-app\uv-cache"
# echo $env:UV_CACHE_DIR


# add new modules e.g. pydantic-settings
# uv add pydantic-settings
# uv remove pydantic-settings

# اگر می‌خوای dev-dependency رو پاک کنی
# مثلاً چیزی که قبلاً با uv add --dev نصب کردی:
# uv remove --dev pytest


# alembic init migrates

