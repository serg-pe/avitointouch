class Advertisement(object):
    """Advertisement data."""
    def __init__(self, url: str, title: str, price: int, specific_params: str):
        self.url = url
        self.title = title
        self.price = price
        self.specific_params = specific_params

    def __str__(self) -> str:
        return f'{self.title}'
