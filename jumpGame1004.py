import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 定义屏幕大小
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("小球爬楼梯")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 定义小球的属性
player_radius = 20
player_speed = 5
normal_jump_height = 12       # 正常跳跃高度
boosted_jump_height = 18      # 增强后的跳跃高度
jump_height = normal_jump_height  # 当前跳跃高度
gravity = 0.5  # 重力加速度

# 跳跃次数控制
max_jumps = 2  # 允许双跳

# 定义楼梯属性
stair_width = 100
stair_height = 20
stair_spacing = 120  # 楼梯之间的垂直间距

# 跳跃增强效果管理
jump_boost_end_time = 0        # 跳跃增强效果结束的时间
jump_boost_duration = 5000     # 跳跃增强效果持续时间（毫秒），例如5秒

# 分数和字体设置
font = pygame.font.SysFont(None, 36)

class Stair:
    def __init__(self, x, y, width=stair_width, height=stair_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.scored = False  # 新增属性，标记是否已计分

    def draw(self, surface, camera_offset):
        stair_draw_rect = pygame.Rect(
            self.x,
            self.y - camera_offset,
            self.width,
            self.height
        )
        pygame.draw.rect(surface, BLACK, stair_draw_rect)

class Box:
    def __init__(self, x, y, width=30, height=30):
        self.x = x  # 箱子的 x 坐标
        self.y = y  # 箱子的 y 坐标
        self.width = width  # 箱子的宽度
        self.height = height  # 箱子的高度
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # 创建用于碰撞检测的矩形
        self.collected = False  # 标记箱子是否被收集

    def draw(self, surface, camera_offset):
        if not self.collected:
            box_draw_rect = pygame.Rect(
                self.x,
                self.y - camera_offset,
                self.width,
                self.height
            )
            pygame.draw.rect(surface, BLUE, box_draw_rect)  # 绘制箱子

    def check_collision(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True  # 标记箱子已被收集
            return True  # 返回 True 表示发生了碰撞
        return False  # 返回 False 表示没有碰撞

def game_loop():
    global jump_height  # 声明全局变量，以便在函数内部修改
    global player_speed  # 如果您在后续增加了速度增强效果

    # 初始化游戏参数
    y_velocity = 0  # 垂直速度
    jump_count = 0

    # 初始化楼梯列表和箱子列表
    stairs = []
    boxes = []

    # 创建第一个楼梯，位置固定
    first_stair_x = (SCREEN_WIDTH - stair_width) // 2
    first_stair_y = SCREEN_HEIGHT - 100  # 距离底部100像素
    first_stair = Stair(first_stair_x, first_stair_y)
    stairs.append(first_stair)

    # 将小球放在第一个楼梯上
    player_x = first_stair_x + stair_width / 2
    player_y = first_stair_y - player_radius

    # 初始化最高到达位置
    highest_y_reached = player_y

    # 初始化 current_highest_stair_y
    current_highest_stair_y = first_stair_y

    # 使用新的变量 stair_y 来生成初始楼梯和箱子
    stair_y = first_stair_y

    # 生成初始的楼梯和箱子，填满屏幕上方
    while stair_y > -SCREEN_HEIGHT:
        stair_y -= stair_spacing
        stair_x = random.randint(0, SCREEN_WIDTH - stair_width)
        stair = Stair(stair_x, stair_y)
        stairs.append(stair)

        # 以30%的概率生成箱子
        if random.random() < 0.3:
            box_x = stair_x + (stair_width - 30) / 2
            box_y = stair_y - 30
            box = Box(box_x, box_y)
            boxes.append(box)

    # 更新 current_highest_stair_y
    current_highest_stair_y = stair_y

    # 摄像机偏移量
    camera_offset = 0

    # 分数
    score = 0

    # 游戏主循环
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(WHITE)

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 按下空格键进行跳跃
                if event.key == pygame.K_SPACE and jump_count < max_jumps:
                    y_velocity = -jump_height
                    jump_count += 1

        # 控制小球左右移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # 边界检查
        if player_x - player_radius < 0:
            player_x = player_radius
        if player_x + player_radius > SCREEN_WIDTH:
            player_x = SCREEN_WIDTH - player_radius

        # 保存小球上一帧的位置
        previous_player_y = player_y
        previous_player_rect = pygame.Rect(
            player_x - player_radius,
            previous_player_y - player_radius,
            player_radius * 2,
            player_radius * 2
        )

        # 重力作用
        y_velocity += gravity
        player_y += y_velocity

        # 更新最高到达位置
        if player_y < highest_y_reached:
            highest_y_reached = player_y

        # 更新摄像机偏移量
        if player_y < SCREEN_HEIGHT / 2:
            camera_offset = player_y - SCREEN_HEIGHT / 2
        else:
            camera_offset = 0  # 当小球在屏幕下半部分时，不移动摄像机

        # 更新小球矩形，用于碰撞检测（不考虑 camera_offset）
        player_rect = pygame.Rect(
            player_x - player_radius,
            player_y - player_radius,
            player_radius * 2,
            player_radius * 2
        )

        # 碰撞检测与跳跃逻辑
        on_platform = False
        for stair in stairs:
            stair_rect = stair.rect
            if player_rect.colliderect(stair_rect):
                # 检查小球是否正在下落
                if y_velocity > 0:
                    # 检查小球是否从上方落到楼梯上
                    if previous_player_rect.bottom <= stair_rect.top and player_rect.bottom >= stair_rect.top:
                        player_y = stair_rect.top - player_radius
                        y_velocity = 0
                        on_platform = True
                        jump_count = 0  # 重置跳跃次数

                        # 仅在首次接触该楼梯时计分
                        if not stair.scored:
                            score += 1  # 增加分数
                            stair.scored = True  # 标记该楼梯已被计分

                        break

        # 检测箱子碰撞
        for box in boxes:
            if box.check_collision(player_rect):
                score += 10  # 每捡到一个箱子增加10分
                # 激活跳跃增强效果
                jump_height = boosted_jump_height
                jump_boost_end_time = pygame.time.get_ticks() + jump_boost_duration
                break  # 处理一个箱子后退出循环，避免一次性捡多个

        # 检查跳跃增强效果是否结束
        current_time = pygame.time.get_ticks()
        if jump_height > normal_jump_height and current_time > jump_boost_end_time:
            jump_height = normal_jump_height

        # 检测是否掉落到屏幕底部
        if player_y - player_radius > highest_y_reached + SCREEN_HEIGHT:
            # 游戏结束，返回得分
            running = False
            return score  # 返回得分

        # 移除超出屏幕下方的楼梯和箱子
        stairs = [stair for stair in stairs if stair.y - camera_offset < SCREEN_HEIGHT + stair_height]
        boxes = [box for box in boxes if box.y - camera_offset < SCREEN_HEIGHT + box.height and not box.collected]

        # 根据玩家的位置生成新的楼梯和箱子
        while current_highest_stair_y > player_y - SCREEN_HEIGHT:
            stair_x = random.randint(0, SCREEN_WIDTH - stair_width)
            current_highest_stair_y -= stair_spacing
            new_stair = Stair(stair_x, current_highest_stair_y)
            stairs.append(new_stair)

            # 以30%的概率生成箱子
            if random.random() < 0.3:
                box_x = stair_x + (stair_width - 30) / 2
                box_y = current_highest_stair_y - 30
                box = Box(box_x, box_y)
                boxes.append(box)

        # 绘制楼梯
        for stair in stairs:
            stair.draw(screen, camera_offset)

        # 绘制箱子
        for box in boxes:
            box.draw(screen, camera_offset)

        # 绘制小球
        player_draw_y = player_y - camera_offset
        pygame.draw.circle(screen, RED, (int(player_x), int(player_draw_y)), int(player_radius))

        # 显示分数
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 显示跳跃增强效果的剩余时间（可选）
        if jump_height > normal_jump_height:
            remaining_time = max(0, (jump_boost_end_time - current_time) // 1000)  # 秒
            boost_text = font.render(f"Jump Boost: {remaining_time}s", True, RED)
            screen.blit(boost_text, (10, 50))

        # 更新显示
        pygame.display.flip()

        # 帧率控制
        clock.tick(60)

    # 游戏结束后返回得分
    return score

def game_over_screen(score):
    # 显示游戏结束界面和分数
    game_over = True
    while game_over:
        screen.fill(WHITE)

        # 显示"Game Over"文本
        game_over_text = font.render("Game Over!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # 显示最终得分
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(score_text, score_rect)

        # 显示提示信息
        restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    return  # 返回到 main() 函数，重新开始游戏
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    while True:
        score = game_loop()
        game_over_screen(score)

# 开始游戏
main()
