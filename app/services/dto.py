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
        return [
            self.index,
            self.name,
            self.subscribers,
            self.increment,
            self.post_views,
            self.er,
            self.references,
            self.geo,
            self.category,
            self.image,
            self.status,
        ]