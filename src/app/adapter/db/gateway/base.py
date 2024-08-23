from sqlalchemy.ext.asyncio import AsyncSession


class BaseGateway[T]:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

# from typing import TypeVar, Generic
#
# T = TypeVar("T")
#
#
# class BaseGateway(Generic[T]):
#     def __init__(self, session: AsyncSession) -> None:
#         self.session = session
