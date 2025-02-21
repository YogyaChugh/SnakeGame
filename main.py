from src import encryptor,Snake
from src.Maps import maps

encryptor.start_encrypting()

map_obj = maps.Map("Map_01")
snake = Snake.snake.Snake("Snake_01",map_obj)
print(snake.locations)
snake.move()
print(snake.locations)