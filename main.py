import os
import sys
from setting import *
import pygame
import requests

server_address = 'https://static-maps.yandex.ru/v1?'
api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
ll_spn = 'll=37.530887,55.703118&spn=1,1'
# Готовим запрос.

map_request = f"{server_address}{ll_spn}&apikey={api_key}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame

pygame.init()
screen = pygame.display.set_mode((WIGHT, HEIGHT))
# Рисуем картинку, загружаемую из только что созданного файла.
a = pygame.image.load(map_file)
pygame.transform.scale(a,(WIGHT, HEIGHT))
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)