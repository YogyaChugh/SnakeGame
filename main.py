from src import encryptor,Snake,Maps

encryptor.start_encrypting()

map_obj = Maps.maps.Map("Map_01")
snake = Snake.snake.Snake("Snake_01",map_obj)
print(snake.locations)
snake.move()
print(snake.locations)