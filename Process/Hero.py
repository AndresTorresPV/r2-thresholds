from pydantic import BaseModel

class Hero(BaseModel):
    name: str
    description: str = None
    price: float = None
    tax: float = None

ironman = Hero(name="IronMan", description="A superhero in a suit of armor", price=100.0, tax=10.0)
captain_america = Hero(name="Captain America", description="A superhero with a shield", price=120.0, tax=12.0)
falcon = Hero(name="Falcon", description="A superhero with wings", price=80.0, tax=8.0)
wanda = Hero(name="Wanda", description="A superhero with magical powers", price=90.0, tax=9.0)
hulk = Hero(name="Hulk", description="A superhero with incredible strength", price=150.0, tax=15.0)
heroes = [ironman, captain_america, falcon, wanda, hulk]    