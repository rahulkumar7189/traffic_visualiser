import pygame

pygame.init()

screen = pygame.display.set_mode((250,800))
running = True
lastTimeChange = pygame.time.get_ticks()
LightColors = ['red','yellow','green','yellow']
LightDuration = [6000,3000,6000,3000]
currentLightOn = 0
emerygencyButton = pygame.Rect(60,570,80,20)
emerygencyButtonPressed = False
corrdinates = [(100,100),(100,180),(100,260),(100,180)]
font_timer = pygame.font.Font(None, 36)

def drawTrafficLight(color, remaining_ms):
    pygame.draw.rect(screen,'gray',(50, 50, 100, 300),border_radius=10)
    pygame.draw.line(screen, 'gray', (100, 350), (100, 700), 15)
    
    lights = [('red', (100,100)), ('yellow', (100,180)), ('green', (100,260))]
    for ind, (c, pos) in enumerate(lights):
        circle_color = c if c == color else (100,0,0) if c=='red' else (100,100,0) if c=='yellow' else (0,100,0)
        pygame.draw.circle(screen, circle_color, pos, 30)
        pygame.draw.circle(screen, 'black', pos, 30, 2)
        
        if c == color:
            seconds = max(0, (remaining_ms // 1000))
            timer_text = font_timer.render(str(seconds), True, 'white')
            text_rect = timer_text.get_rect(center=pos)
            screen.blit(timer_text, text_rect)

def drawTrafficArrow(color, pos, direction='left'):
    x, y = pos
    arrow_length = 25
    arrow_tip_size = 15
    if direction == 'left':
        pygame.draw.line(screen, color, (x, y), (x - arrow_length, y), 4)
        points = [(x - arrow_length, y),
                  (x - arrow_length + arrow_tip_size, y - arrow_tip_size//2),
                  (x - arrow_length + arrow_tip_size, y + arrow_tip_size//2)]
    else:
        pygame.draw.line(screen, color, (x, y), (x + arrow_length, y), 4)
        points = [(x + arrow_length, y),
                  (x + arrow_length - arrow_tip_size, y - arrow_tip_size//2),
                  (x + arrow_length - arrow_tip_size, y + arrow_tip_size//2)]
    border_color = 'black' if color == 'white' else color
    pygame.draw.polygon(screen, border_color, points, 2)
    pygame.draw.polygon(screen, color, points)

def drawBox():
    pygame.draw.rect(screen,'gray',(70,430,60,100),border_radius=10)
    pygame.draw.rect(screen,(96,96,96),(80,440,40,80),border_radius=10)
    pygame.draw.rect(screen,'red',emerygencyButton,border_radius=5)
    pygame.draw.rect(screen,'gray',(60,570,80,20),2,border_radius=5)
    pygame.draw.rect(screen,'green' if currentLightOn == 0 else 'red',(85,450,30,60),border_radius=5)
    font = pygame.font.Font(None,16)
    fontt = pygame.font.Font(None,20)
    str_text = "Go" if currentLightOn == 0 else "Stop"
    displayText = fontt.render(str_text,True,'black')
    screen.blit(displayText,(88,470))
    text = font.render("EMERGENCY",True,'black')
    screen.blit(text,(emerygencyButton.x + 5 , emerygencyButton.y + 5))
        
while running:
    curTime = pygame.time.get_ticks()
    elapsed = curTime - lastTimeChange
    remaining = LightDuration[currentLightOn] - elapsed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if emerygencyButton.collidepoint(event.pos):
                emerygencyButtonPressed = not emerygencyButtonPressed
                if emerygencyButtonPressed:
                    currentLightOn = 0
                lastTimeChange = pygame.time.get_ticks()
                elapsed = 0
                remaining = LightDuration[currentLightOn]

    if not emerygencyButtonPressed :
        if elapsed >= LightDuration[currentLightOn]:
            currentLightOn =( currentLightOn + 1) % len(LightColors)
            lastTimeChange = curTime
            remaining = LightDuration[currentLightOn]

    screen.fill('black')

    drawTrafficLight(LightColors[currentLightOn], remaining)
    drawBox()

    arrow_y = 320 
    arrow_offset = 15
    arrow_left_x = 100 - arrow_offset
    arrow_right_x = 100 + arrow_offset

    arrow_color = 'green' if LightColors[currentLightOn] == 'green' else 'white'

    drawTrafficArrow(arrow_color, (arrow_left_x, arrow_y), 'left')
    drawTrafficArrow(arrow_color, (arrow_right_x, arrow_y), 'right')
    pygame.display.update()

pygame.quit()