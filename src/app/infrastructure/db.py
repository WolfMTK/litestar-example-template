from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession


def get_engine(url: str) -> AsyncEngine:
    engine = create_async_engine(url)
    return engine


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    return session_maker
