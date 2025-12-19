# Litestar Template

## Description

A small template for creating services using Litestar, which should help you in building services with this framework. I
know that not everything is done perfectly here, so I’m looking forward to your issues and suggestions on what could be
improved.

## Install

`us sync`

## Environment variables

`BASE_CONFIG` - path to the config

## Apply migrations

`uv run alembic upgrade head`

## Run

`uv run uvicorn --factory app.main:create_app`
