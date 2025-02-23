import os
import sys
from setting import *
import pygame
import requests
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


def search(x, y, z=20):
    server_address = "https://static-maps.yandex.ru/v1?"
    api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    ll_spn = f"ll={str(x)},{str(y)}&spn=1,1"
    mash_tab = f"z={z}"
    # Готовим запрос.
    # x, y = "37.530887", "55.703118"
    map_request = f"{server_address}{ll_spn}&{mash_tab}&apikey={api_key}"
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
    return map_file


# СТАНДАРТНОЕ ИЗОБРОЖЕНИЕ
map_file = search(37.530887, 55.703118, z=20)
# Инициализируем pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIGHT, HEIGHT))

# Заготовка для поля ввода
user_text = ""
base_font = pygame.font.Font(None, 40)
input_rect = pygame.Rect(10, 500, 140, 32)
color_active = pygame.Color("lightskyblue")
color_passive = pygame.Color("white")
color = color_passive

# Заготовка для клавиши Start
small_font = pygame.font.SysFont("Corbel", 35)
text = small_font.render("Start", True, (0, 0, 0))

# Заготовка для слайдера
slider = Slider(screen, 250, 500, 150, 20, min=0, max=21, step=1)
output = TextBox(screen, 300, 550, 50, 40, fontSize=20)
output.disable()

running = True
active = False
button_click = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
            if button_rect.collidepoint(event.pos):
                button_click = True
            # if the key is physically pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # stores text except last letter
                user_text = user_text[0:-1]
            else:
                user_text += event.unicode
    screen.fill((0, 0, 0))
    screen.blit(pygame.image.load(map_file), (0, 0))
    if active:
        color = color_active
    else:
        color = color_passive
    # Вывод текста на экран
    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    input_rect.w = max(100, text_surface.get_width() + 10)

    # Вывод кнопки Start на экран
    button_rect = pygame.Rect(500, 500, 140, 40)
    pygame.draw.rect(screen, (255, 255, 255), button_rect)
    screen.blit(text, (500, 500))

    # Вывод слайдера
    output.setText(slider.getValue())
    events = pygame.event.get()
    pygame_widgets.update(events)

    if button_click:
        button_click = False
        try:
            z1 = str(slider.getValue())
            x = user_text.split(",")[0]
            y = user_text.split(",")[1]
            search(x, y, z=z1)
        except:
            print("В ЗАПРСОЕ ЕСТЬ ОШИБКА ВВЕДИТЕ X И Y ЧЕРЕЗ ЗАПЯТУЮ БЕЗ ПРОБЕЛОВ")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
