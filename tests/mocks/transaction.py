class TransactionMock:
    def __init__(self) -> None:
        self.commited = False
        self.rolled_back = False

    async def commit(self) -> None:
        if self.rolled_back:
            raise ValueError('Cannot commit after rolling back')
        self.commited = True

    async def rollback(self) -> None:
        if self.commited:
            raise ValueError('Cannot rollback after commiting')
        self.rolled_back = True
