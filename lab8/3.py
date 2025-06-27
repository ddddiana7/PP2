import pygame

SQUARE = 'SQUARE'
CIRCLE = 'CIRCLE'
TRIANGLE = 'TRIANGLE'
ERASER = 'ERASER'

dis_width = 640
dis_height = 480
main_screen_size = (dis_width, dis_height)
elements_to_draw = [] #список всех нарисованных объектов

icon_top_bar_height = 50
icon_top_bar_width = 50

#rоординаты панелей инструментов и кнопок
icon_rectangle_start_x = 0
icon_rectangle_end_x = 50
icon_circle_start_x = 50
icon_circle_end_x = 100
icon_eraser_start_x = 100
icon_eraser_end_x = 150

icon_red_color_start_y = 50
icon_red_color_end_y = 100
icon_blue_color_start_y = 100
icon_blue_color_end_y = 150
icon_color_shape_width = 40
icon_color_shape_height = 30
icon_orange_color_start_y = 150
icon_orange_color_end_y = 200

#COLORS
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
orange = (255, 165, 0)

#цвета и панели
top_tab_color = (100, 100, 100)
right_tab_color = (80, 80, 80)

#функция перерисовывает все фигуры, которые пользователь уже нарисовал
def draw_all_shapes(screen):
    for element in elements_to_draw:
        if element['shape'] == SQUARE:
            pygame.draw.rect(screen, element['color'],
                             [element['x'], element['y'], 50, 50])
        elif element['shape'] == CIRCLE:
            pygame.draw.circle(screen, element['color'],
                               (element['x'], element['y']), element['radius'])
        elif element['shape'] == TRIANGLE:
            pygame.draw.polygon(screen, element['color'], element['vertices'])


# Adds a square element to the drawing
def add_element_rectangle(x, y, color):
    elements_to_draw.append({'shape': SQUARE, 'x': x, 'y': y, 'color': color})

# Adds a circle element to the drawing
def add_element_circle(x, y, color, radius):
    elements_to_draw.append({
        'shape': CIRCLE,
        'x': x,
        'y': y,
        'color': color,
        'radius': radius
    })

def add_element_circle(x, y, color, radius):
    elements_to_draw.append({
        'shape': CIRCLE,
        'x': x,
        'y': y,
        'color': color,
        'radius': radius
    })

def add_element_triangle(x, y, color): #добавляет dictionry с параметрами фигуры в список elements_to_draw
    vertices = [(x, y), (x - 25, y + 50), (x + 25, y + 50)]
    elements_to_draw.append({'shape': TRIANGLE, 'vertices': vertices, 'color': color})

def erase_element(x, y): #удаляет фигуры если клик был внутри нее
    for element in elements_to_draw[:]:  #прохожусь по копии списка elements_to_draw
        if element['shape'] == SQUARE and element['x'] <= x <= element['x'] + 50 and element['y'] <= y <= element['y'] + 50:
            elements_to_draw.remove(element)
        elif element['shape'] == CIRCLE and (x - element['x'])**2 + (y - element['y'])**2 <= element['radius']**2: #расстояние от центра
            elements_to_draw.remove(element)
        elif element['shape'] == TRIANGLE:
            if pygame.draw.polygon(pygame.Surface((dis_width, dis_height), pygame.SRCALPHA), (0, 0, 0, 0), element['vertices']).get_rect().collidepoint(x, y):
                elements_to_draw.remove(element)
                #рисует невидимую поверхность, получает ограничивающий треугольник, проверяет попадает ли (х, у) в области фигуры


#рисует все иконки инструментов и цветов
def draw_main_icons(screen):
    pygame.draw.rect(screen, top_tab_color, (0, 0, dis_width, 40))
    pygame.draw.rect(screen, right_tab_color, (dis_width - 80, 0, 80, dis_height))
    pygame.draw.rect(screen, white, (icon_rectangle_start_x + 5, 5, 40, 30))
    pygame.draw.rect(screen, white, (icon_circle_start_x + 5, 5, 40, 30))
    pygame.draw.circle(screen, (128, 0, 128), (icon_circle_start_x + 25, 20), 10)
    pygame.draw.rect(screen, white, (icon_eraser_start_x + 5, 5, 40, 30))
    pygame.draw.line(screen, black, (icon_eraser_start_x + 10, 10), (icon_eraser_start_x + 30, 30), 5)
    pygame.draw.rect(screen, red, (dis_width - 70, icon_red_color_start_y, icon_color_shape_width, icon_color_shape_height))
    pygame.draw.rect(screen, blue, (dis_width - 70, icon_blue_color_start_y, icon_color_shape_width, icon_color_shape_height))
    pygame.draw.rect(screen, orange, (dis_width - 70, icon_orange_color_start_y, icon_color_shape_width, icon_color_shape_height))


#запускает главный цикл программы 
def main():
    pygame.init()
    screen = pygame.display.set_mode(main_screen_size)
    clock = pygame.time.Clock() #для фпс
    
    is_rectangle_drawer = False
    is_circle_drawer = False
    is_eraser = False
    color = black
    position = (0, 0)#начальная позиция, обновляется после клика мышки

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos #настоящие координаты клика
                if icon_rectangle_start_x <= position[0] < icon_rectangle_end_x and position[1] < icon_top_bar_height:
                    is_rectangle_drawer = True
                    is_circle_drawer = False
                    is_eraser = False
                elif icon_circle_start_x <= position[0] < icon_circle_end_x and position[1] < icon_top_bar_height:
                    is_circle_drawer = True
                    is_rectangle_drawer = False
                    is_eraser = False
                elif icon_eraser_start_x <= position[0] < icon_eraser_end_x and position[1] < icon_top_bar_height:
                    is_eraser = True
                    is_rectangle_drawer = False
                    is_circle_drawer = False
                elif dis_width - 70 <= position[0] < dis_width - 30:
                    if icon_red_color_start_y <= position[1] < icon_red_color_end_y:
                        color = red
                    elif icon_blue_color_start_y <= position[1] < icon_blue_color_end_y:
                        color = blue
                    elif icon_orange_color_start_y <= position[1] < icon_orange_color_end_y:
                        color = orange
                elif is_rectangle_drawer:
                    add_element_rectangle(position[0], position[1], color)
                elif is_circle_drawer:
                    add_element_circle(position[0], position[1], color, 20)
                elif is_eraser:
                    erase_element(position[0], position[1])

        screen.fill(white) #белый экран
        draw_all_shapes(screen) #отрисовывает все фигуры, которые сохранены в списке elements_to_draw
        draw_main_icons(screen) #отрисовывает верхнюю панель инструментов и правую панель выбора цвета
        pygame.display.flip() #shows all changes 
        clock.tick(60) #limits 

main()