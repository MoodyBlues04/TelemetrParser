class TableRow:
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CLOSED = 'closed'

    index: int
    name: str
    subscribers: int
    increment: int
    post_views: int
    er: float
    references: int
    geo: str
    category: str
    image: str
    status: str

    def __str__(self):
        return str(self.__dict__)

    def to_array(self) -> list:
        return list(self.__dict__.values())