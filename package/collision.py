from package.Point import Point

class collision():
    amount: int = 0
    lines: list[list[Point]]
    
    def __init__(self) -> None:
        self.amount = 0
        self.lines = []
        
    def __eq__(self, __value: "collision") -> bool:
        return self.amount == __value.amount and self.lines == __value.lines

    def __str__(self):
        return str(self.amount)
    
    def __repr__(self) -> str:
        return str(self)
    
    def __gt__(self, __value: "collision") -> bool:
        return self.amount > __value.amount
    
    def __ge__(self, __value: "collision") -> bool:
        return self.amount >= __value.amount
    
    def __le__(self, __value: "collision") -> bool:
        return self.amount <= __value.amount
    
    def __lt__(self, __value: "collision") -> bool:
        return self.amount < __value.amount