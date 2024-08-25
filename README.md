# Litestar Template

## Description

A small template for creating services using Litestar, which should help you in building services with this framework. I
know that not everything is done perfectly here, so I’m looking forward to your issues and suggestions on what could be
improved.

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
