from litestar import Request, Response, status_codes


def not_found(
        _: Request,
        exc: Exception
) -> Response:
    return Response(
        content={
            "status_code": status_codes.HTTP_404_NOT_FOUND,
            "detail": str(exc)
        }
    )
