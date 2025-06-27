import pygame

#фигуры
SQUARE = 'SQUARE'
CIRCLE = 'CIRCLE'
TRIANGLE = 'TRIANGLE'
EQUILATERAL = 'EQUILATERAL'
RHOMBUS = 'RHOMBUS'
ERASER = 'ERASER'

#размер окна
dis_width = 640
dis_height = 480
main_screen_size = (dis_width, dis_height)

elements_to_draw = [] #пустой список будет запоняться фигурами

#параметры иконок (верхняя панель и правая панель)
icon_size = 50
icon_color_size = 40
icon_top_bar_height = 40

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
orange = (255, 165, 0)
top_tab_color = (100, 100, 100)
right_tab_color = (80, 80, 80)

#добавляе все фигуры
def add_element_rectangle(x, y, color): #список всех нарисованных фигур
    elements_to_draw.append({'shape': SQUARE, 'x': x, 'y': y, 'color': color})

def add_element_circle(x, y, color, radius):
    elements_to_draw.append({'shape': CIRCLE, 'x': x, 'y': y, 'color': color, 'radius': radius})

def add_element_triangle(x, y, color):
    vertices = [(x, y), (x - 25, y + 50), (x + 25, y + 50)]  #прямоуг трегуольник
    elements_to_draw.append({'shape': TRIANGLE, 'vertices': vertices, 'color': color})

def add_element_equilateral_triangle(x, y, color): #равносторонний треугольник 
    side = 50
    height = (3 ** 0.5 / 2) * side
    vertices = [(x, y), (x - side // 2, y + int(height)), (x + side // 2, y + int(height))]
    elements_to_draw.append({'shape': EQUILATERAL, 'vertices': vertices, 'color': color})

def add_element_rhombus(x, y, color):
    size = 40
    vertices = [(x, y - size), (x + size, y), (x, y + size), (x - size, y)]
    elements_to_draw.append({'shape': RHOMBUS, 'vertices': vertices, 'color': color})

#функция стирания объектов по координатам
def erase_element(x, y):
    for element in elements_to_draw[:]:
        if element['shape'] == SQUARE and element['x'] <= x <= element['x'] + 50 and element['y'] <= y <= element['y'] + 50:
            elements_to_draw.remove(element)
        elif element['shape'] == CIRCLE and (x - element['x'])**2 + (y - element['y'])**2 <= element['radius']**2:
            elements_to_draw.remove(element)
        elif 'vertices' in element:
            polygon = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
            pygame.draw.polygon(polygon, (0, 0, 0, 255), element['vertices'])
            if polygon.get_rect().collidepoint(x, y):
                elements_to_draw.remove(element)

#отрисовка всех сохранённых фигур
def draw_all_shapes(screen):
    for element in elements_to_draw:
        if element['shape'] == SQUARE:
            pygame.draw.rect(screen, element['color'], [element['x'], element['y'], 50, 50])
        elif element['shape'] == CIRCLE:
            pygame.draw.circle(screen, element['color'], (element['x'], element['y']), element['radius'])
        elif element['shape'] in (TRIANGLE, EQUILATERAL, RHOMBUS):
            pygame.draw.polygon(screen, element['color'], element['vertices'])

#панель с иконками инструментов
def draw_main_icons(screen):
    pygame.draw.rect(screen, top_tab_color, (0, 0, dis_width, icon_top_bar_height))
    pygame.draw.rect(screen, right_tab_color, (dis_width - 80, 0, 80, dis_height))

    #иконки инструментов (верх)
    pygame.draw.rect(screen, white, (5, 5, 40, 30))     #квадрат
    pygame.draw.circle(screen, (128, 0, 128), (75, 20), 15)  #круг
    pygame.draw.polygon(screen, white, [(130, 5), (120, 35), (140, 35)])  #прям треугольник
    pygame.draw.polygon(screen, white, [(190, 5), (175, 35), (205, 35)])  #равн. треугольник
    pygame.draw.polygon(screen, white, [(250, 20), (270, 5), (290, 20), (270, 35)])  #ромб
    pygame.draw.line(screen, red, (310, 10), (330, 30), 5)  #стиралка

    #панель цветов (право)
    pygame.draw.rect(screen, red, (dis_width - 70, 50, icon_color_size, 30))
    pygame.draw.rect(screen, blue, (dis_width - 70, 100, icon_color_size, 30))
    pygame.draw.rect(screen, orange, (dis_width - 70, 150, icon_color_size, 30))

#Главный цикл программы
def main():
    pygame.init()
    screen = pygame.display.set_mode(main_screen_size)
    clock = pygame.time.Clock()

    current_tool = None
    color = black

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Выбор инструмента по клику сверху
                if y < icon_top_bar_height:
                    if x < 50:
                        current_tool = SQUARE
                    elif x < 100:
                        current_tool = CIRCLE
                    elif x < 150:
                        current_tool = TRIANGLE
                    elif x < 200:
                        current_tool = EQUILATERAL
                    elif x < 250:
                        current_tool = RHOMBUS
                    elif x < 350:
                        current_tool = ERASER
                #выбор цвета (правая панель)
                elif dis_width - 70 <= x <= dis_width - 30:
                    if 50 <= y <= 80:
                        color = red
                    elif 100 <= y <= 130:
                        color = blue
                    elif 150 <= y <= 180:
                        color = orange
                else:
                    #рисование фигур
                    if current_tool == SQUARE:
                        add_element_rectangle(x, y, color)
                    elif current_tool == CIRCLE:
                        add_element_circle(x, y, color, 20)
                    elif current_tool == TRIANGLE:
                        add_element_triangle(x, y, color)
                    elif current_tool == EQUILATERAL:
                        add_element_equilateral_triangle(x, y, color)
                    elif current_tool == RHOMBUS:
                        add_element_rhombus(x, y, color)
                    elif current_tool == ERASER:
                        erase_element(x, y)

        screen.fill(white) #белый экран
        draw_all_shapes(screen)
        draw_main_icons(screen)
        pygame.display.flip()
        clock.tick(60)

main()
