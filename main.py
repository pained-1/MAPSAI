import os, sys, pygame, requests, pygame_widgets
from setting import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import requests


def search_maps(address):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    address_ll = "37.588392,55.734036"

    search_params = {
        "apikey": api_key,
        "text": address,
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if response:
        json_response = response.json()
        # Получаем первую найденную организацию.
        organization = json_response["features"][0]
        # Название организации.
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        # Адрес организации.
        org_address = organization["properties"]["CompanyMetaData"]["address"]

        # Получаем координаты ответа.
        point = organization["geometry"]["coordinates"]
        org_address = f"{point[0]},{point[1]}"
    return org_address


def search(x, y, z=20, points_x="", points_y=""):
    server_address = "https://static-maps.yandex.ru/v1?"
    api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    ll = f"ll={x},{y}"

    if points_x and points_y:
        point = f"450&l=map&pt={points_x},{points_y},pm2ntm"
    else:
        point = ""
    # Готовим запрос.
    # x, y = "37.530887", "55.703118 (37.530887,55.703118)"
    map_request = f"{server_address}{ll}&z={z}&theme={theme}&{point}&apikey={api_key}"
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
z1 = 10
x, y = 37.530887, 55.703118
theme = "light"
map_file = search(x, y, z=z1)
# Инициализируем pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIGHT, HEIGHT))

# Заготовка для поля ввода координат
user_text = ""
base_font = pygame.font.Font(None, 40)
input_rect = pygame.Rect(10, 500, 140, 32)
color_passive = pygame.Color("grey")
color = color_passive

# Заготовка для поля ввода адреса с использованием прошлых заготовок
input_rect_objects = pygame.Rect(10, 550, 140, 32)
user_text_objects = ""

# Заготовка для клавиши Start
small_font_start = pygame.font.SysFont("Corbel", 35)
text_start = small_font_start.render("Start", True, (0, 0, 0))
button_rect_start = pygame.Rect(500, 500, 140, 40)

# Заготовка для клавиши change theme
small_font_theme = pygame.font.SysFont("Corbel", 25)
text_theme = small_font_theme.render("Change theme", True, (0, 0, 0))
button_rect_theme = pygame.Rect(450, 550, 150, 40)

# Заготовка для слайдера
slider = Slider(screen, 250, 500, 150, 20, min=0, max=21, step=1)
output = TextBox(screen, 300, 550, 50, 40, fontSize=20)
output.disable()

running = True
active = False
button_click = False
click_input_coordinates = False
click_input_objects = False
screen.blit(pygame.image.load(map_file), (0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if button_rect_start.collidepoint(event.pos):
                button_click = True
            if input_rect_objects.collidepoint(mouse_x, mouse_y):
                click_input_objects = True
                click_input_coordinates = False
            if input_rect.collidepoint(mouse_x, mouse_y):
                click_input_coordinates = True
                click_input_objects = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect_theme.collidepoint(event.pos):
                theme = "light" if theme == "dark" else "dark"
                search(x, y, z=z1)
                screen.blit(pygame.image.load(map_file), (0, 0))
            # if the key is physically pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # при нажатии на enter отключается ввод текста и производиться обработка данных из нижнего поля для объектов
                click_input_coordinates = False
                click_input_objects = False
                try:
                    coord = search_maps(user_text_objects).split(",")
                    x = float(coord[0])
                    y = float(coord[1])
                    search(x, y, z=z1, points_x=x, points_y=y)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                except:
                    print("ЗАПРОС НЕ КОРЕКТЕН")
            if event.key == pygame.K_BACKSPACE:
                # stores text except last letter
                if click_input_coordinates:
                    user_text = user_text[0:-1]
                elif click_input_objects:
                    user_text_objects = user_text_objects[0:-1]
            elif event.key == pygame.K_PAGEUP:
                if z1 < 21:
                    slider.setValue(z1 + 1)
            elif event.key == pygame.K_PAGEDOWN:
                if z1 > 0:
                    slider.setValue(z1 - 1)
            elif event.key == pygame.K_UP:
                y += 0.1
                search(x, y, z=z1)
                screen.blit(pygame.image.load(map_file), (0, 0))
            elif event.key == pygame.K_DOWN:
                y -= 0.1
                search(x, y, z=z1)
                screen.blit(pygame.image.load(map_file), (0, 0))
            elif event.key == pygame.K_RIGHT:
                x += 0.1
                search(x, y, z=z1)
                screen.blit(pygame.image.load(map_file), (0, 0))
            elif event.key == pygame.K_LEFT:
                x -= 0.1
                search(x, y, z=z1)
                screen.blit(pygame.image.load(map_file), (0, 0))
            else:
                if click_input_coordinates:
                    user_text += event.unicode
                if click_input_objects:
                    user_text_objects += event.unicode

    # Вывод текста координат на экран
    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    input_rect.w = max(100, text_surface.get_width() + 10)

    # Вывод текста адреса на экран
    pygame.draw.rect(screen, color, input_rect_objects)
    text_surface_objects = base_font.render(user_text_objects, True, (255, 255, 255))
    screen.blit(text_surface_objects, (input_rect_objects.x + 5, input_rect_objects.y + 5))
    input_rect_objects.w = max(100, text_surface_objects.get_width() + 10)

    # Вывод кнопки Start на экран
    pygame.draw.rect(screen, (255, 255, 255), button_rect_start)
    screen.blit(text_start, (500, 500))

    # Вывод кнопки theme на экран
    pygame.draw.rect(screen, (255, 255, 255), button_rect_theme)
    screen.blit(text_theme, (450, 550))

    # Вывод слайдера
    output.setText(slider.getValue())
    events = pygame.event.get()
    pygame_widgets.update(events)

    if button_click:
        button_click = False
        try:
            x, y = user_text.split(",")
            search(x, y, z=z1)
            screen.blit(pygame.image.load(map_file), (0, 0))
        except:
            print("В ЗАПРСОЕ ЕСТЬ ОШИБКА ВВЕДИТЕ X И Y ЧЕРЕЗ ЗАПЯТУЮ БЕЗ ПРОБЕЛОВ")

    if z1 != slider.getValue():
        z1 = slider.getValue()
        search(x, y, z=z1)
        screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
