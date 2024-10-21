# Litestar Template

## Description

A small template for creating services using Litestar, which should help you in building services with this framework. I
know that not everything is done perfectly here, so I’m looking forward to your issues and suggestions on what could be
improved.

## Creation of virtual environments

`python -m venv .venv`

[More Detail](https://docs.python.org/3/library/venv.html)

## Install

`pip install -e .`

## Configure env:

```
export DEBUG=false

export DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/task
```

## Apply migrations

`alembic upgrade head`

## Run

`uvicorn --factory app.main:create_app`
