FROM alpine:3.23.2

RUN apk update && apk --no-cache add curl

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

ENV UV_LINK_MODE=copy

ADD . ./app

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev \
