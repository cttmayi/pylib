import pygame

# 初始化Pygame
pygame.init()

# 设置窗口大小
size = (700, 500)
screen = pygame.display.set_mode(size)

# 设置窗口标题
pygame.display.set_caption("My Game")

# 设置矩形位置和大小
rect_x = 50
rect_y = 50
rect_width = 50
rect_height = 50

# 设置颜色
red = (255, 0, 0)

# 游戏循环
done = False
while not done:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 填充窗口颜色
    screen.fill((255, 255, 255))

    # 绘制矩形
    pygame.draw.rect(screen, red, [rect_x, rect_y, rect_width, rect_height])

    # 更新窗口
    pygame.display.update()

# 退出Pygame ß