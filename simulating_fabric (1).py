import pygame as pg 
import math 
import multiprocessing

# vars 
screen_width = 1000 
screen_hight = 600 
xpoints_num = 60
ypoints_num = 30
points_num = xpoints_num * ypoints_num
gravity = 0.07
bouncing_factor = 0.07
ground_frection = 0.9
air_frection = 0.995
curser_power = 3
correction_times = 2
distance = 10
bound_length = distance
init_x_offset = (screen_width / 2) - (xpoints_num * distance / 2)
init_y_offset = 200

win = pg.display.set_mode((screen_width, screen_hight)) 
 
clock = pg.time.Clock() 

class points : 
    def __init__(self, ix, iy) : 
        self.x = ix 
        self.y = iy 
        self.px = ix 
        self.py = iy
     
class bounds : 
    def __init__(self, dot1, dot2): 
        self.p1 = dot1 
        self.p2 = dot2 
 
#initiating points and bounds 

point = []
for j in range(ypoints_num):
    for i in range(xpoints_num):
        point.append(points(init_x_offset + distance * i, init_y_offset + distance * j))

bound = []
for j in range(ypoints_num):
    
    if j == ypoints_num - 1: #if the current point is the last point in y grid it will only establish one bound

        for i in range(xpoints_num):
            if i != xpoints_num - 1:
                bound.append(bounds(i+j*xpoints_num, i+j*xpoints_num + 1))   # a bound with the point next the current point

    else:
        for i in range(xpoints_num):
            if i != xpoints_num - 1:
                bound.append(bounds(i+j*xpoints_num, i+j*xpoints_num + 1))
                bound.append(bounds(i+j*xpoints_num, i+j*xpoints_num+ xpoints_num))
            else:
                bound.append(bounds(i+j*xpoints_num, i+j*xpoints_num+ xpoints_num))

bound_num = len(bound)

def find_watr (p1 = points, p2 = points): 
    return math.sqrt((p1.y - p2.y) **2 + (p1.x - p2.x) **2) 

def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  
    return 1 if val > 0 else 2  

def on_segment(p, q, r):
    if min(p.x, r.x) <= q.x <= max(p.x, r.x) and min(p.y, r.y) <= q.y <= max(p.y, r.y):
        return True
    return False

def do_intersect(A, B, C, D):
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    
    if o1 != o2 and o3 != o4:
        return True
    
    if o1 == 0 and on_segment(A, C, B):
        return True
    if o2 == 0 and on_segment(A, D, B):
        return True
    if o3 == 0 and on_segment(C, A, D):
        return True
    if o4 == 0 and on_segment(C, B, D):
        return True
    
    return False
def in_square(i):
    if point[i].x - distance < mouse_position.px < point[i].x + distance:
        if point[i].y - distance < mouse_position.py < point[i].y + distance:
            return True
    
'''
def thread1_motion():
    for j in range(ypoints_num):
        for i in range(int(xpoints_num / 2 - 1)):

                ytemp = point[i].y 
                point[i].y += (point[i].y - point[i].py)* air_frection + gravity #resisstance and gravity
                point[i].py = ytemp

                xtemp = point[i].x 
                if screen_hight - 2 < point[i].y < screen_hight:
                    point[i].x += (point[i].x - point[i].px) *ground_frection # (if in ground) ground frection
                else:
                    point[i].x += (point[i].x - point[i].px) *air_frection # air resisstance
                point[i].px = xtemp 

def thread2_motion():
    for j in range(ypoints_num):
        for i in range(xpoints_num -1, int(xpoints_num / 2 - 1), -1):

                ytemp = point[i].y 
                point[i].y += (point[i].y - point[i].py)* air_frection + gravity #resisstance and gravity
                point[i].py = ytemp

                xtemp = point[i].x 
                if screen_hight - 2 < point[i].y < screen_hight:
                    point[i].x += (point[i].x - point[i].px) *ground_frection # (if in ground) ground frection
                else:
                    point[i].x += (point[i].x - point[i].px) *air_frection # air resisstance
                point[i].px = xtemp
'''

left_click_time = 0
right_button_held = 0
left_button_held = False
right_button_held = False
mouse_in_motion = False
mouse_pos = (0, 0)
mouse_position = points(0, 0)
temp_mouse_pos = points(0, 0)
mouse_dx = 0
mouse_dy = 0
locked_position = (0, 0)
dragged_point = (xpoints_num)*(ypoints_num-1) + (xpoints_num)/2

running = True
while running:
    #print(point[0].x, point[0].y)
    
    mouse_in_motion = False
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
        if pg.MOUSEMOTION :
            mouse_in_motion = True #mouse in motion
        else:
            mouse_in_motion = False

        # Check for left-click pressed and get the dragged point
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            left_button_held = True   # Left button is pressed
            
            #get the dragged point index
            for i in range(points_num):
                if in_square(i):
                    dragged_point = i
                    break


        # Check for right-click pressed
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            right_button_held = True   # right button is pressed

        # Check for left-click released
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            left_button_held = False  # Left button is released
            left_click_time = 0       # Reset click time
            mouse_dx = 0
            mouse_dy = 0
        
        # Check for right-click released
        if event.type == pg.MOUSEBUTTONUP and event.button == 3:
            right_button_held = False  # right button is released
            right_click_time = 0       # Reset click time

        # mouse motion while left button is held
        if event.type == pg.MOUSEMOTION and left_button_held:
            if left_click_time != 0:
                prev_mouse_pos = mouse_pos
                mouse_pos = pg.mouse.get_pos()

                #change in x and y
                mouse_dx = (mouse_pos[0] - prev_mouse_pos[0]) * curser_power
                mouse_dy = (mouse_pos[1] - prev_mouse_pos[1]) * curser_power
                left_click_time += 1

            else:
                #mouse position on first movement
                mouse_pos = pg.mouse.get_pos()
                left_click_time += 1
                

    if left_button_held == True:    #if left click was in hold
        #x and y motion changement and gravity, frection effects
        for i in range(points_num):
            if i == dragged_point : #draged points
                if mouse_in_motion:
                    ytemp = point[i].y
                    point[i].y += point[i].y - point[i].py + mouse_dy
                    point[i].py = ytemp

                    xtemp = point[i].x 
                    point[i].x += point[i].x - point[i].px + mouse_dx
                    point[i].px = xtemp

                    locked_position = (point[i].x, point[i].y) #mouse stop moving last coords
                else:
                    point[i].x = locked_position[0]
                    point[i].y = locked_position[1]
            else: #not draged ones
                ytemp = point[i].y 
                point[i].y += (point[i].y - point[i].py)* air_frection + gravity
                point[i].py = ytemp

                xtemp = point[i].x 
                if screen_hight - 2 < point[i].y < screen_hight:
                    
                    point[i].x += (point[i].x - point[i].px) *ground_frection # (if in ground) ground frection
                else:
                    point[i].x += (point[i].x - point[i].px) *air_frection # air resisstance
                point[i].px = xtemp 
    else: #if left click was not in hold
        
        for i in range(points_num):

            ytemp = point[i].y 
            point[i].y += (point[i].y - point[i].py)* air_frection + gravity #resisstance and gravity
            point[i].py = ytemp

            xtemp = point[i].x 
            if screen_hight - 2 < point[i].y < screen_hight:
                point[i].x += (point[i].x - point[i].px) *ground_frection # (if in ground) ground frection
            else:
                point[i].x += (point[i].x - point[i].px) *air_frection # air resisstance
            point[i].px = xtemp 
        
        
        '''
        num_processes = multiprocessing.cpu_count()  # Get number of CPU cores
        processes1 = multiprocessing.Process(target=thread1_motion)
        processes1.start()
        processes2 = multiprocessing.Process(target=thread2_motion)
        processes2.start()

        processes1.join()
        processes2.join()
        '''

    #ground collision  
    for i in range(points_num): 
        if point[i].y > screen_hight: 
            velocity = point[i].y - point[i].py 
            point[i].y = 2* screen_hight - point[i].y 
            point[i].py = point[i].y + velocity *bouncing_factor 

    '''
    #roof collision
    for i in range(points_num): 
        if point[i].y < 0: 
            velocity = point[i].y - point[i].py 
            point[i].y = - point[i].y 
            point[i].py = point[i].y - velocity *bouncing_factor
    
    #right wall collision
    for i in range(points_num):
        if point[i].x > screen_width:
            velocity = point[i].x - point[i].px
            point[i].x = 2* screen_width - point[i].x
            point[i].px = point[i].x + velocity *bouncing_factor

    #left wall colission
    for i in range(points_num): 
        if point[i].x < 0: 
            velocity = point[i].x - point[i].px
            point[i].x = - point[i].x
            point[i].px = point[i].x - velocity *bouncing_factor
    '''

#bound force and correction loop
    for n in range(correction_times):
        for i in range(len(bound) ):
            bound_dist = find_watr(point[bound[i].p1], point[bound[i].p2])

            if bound_dist != bound_length:
                dist_diff = (bound_length - bound_dist) / 2
                
                dx = (point[bound[i].p2].x - point[bound[i].p1].x) * dist_diff / bound_dist
                dy = (point[bound[i].p2].y - point[bound[i].p1].y) * dist_diff / bound_dist

                point[bound[i].p1].x -= dx
                point[bound[i].p1].y -= dy
                point[bound[i].p2].x += dx
                point[bound[i].p2].y += dy
        '''
        for i in range(len(bound) -1, -1, -1):
            bound_dist = find_watr(point[bound[i].p1], point[bound[i].p2])

            if bound_dist != bound_length:
                dist_diff = (bound_length - bound_dist) / 2
                
                dx = (point[bound[i].p2].x - point[bound[i].p1].x) * dist_diff / bound_dist
                dy = (point[bound[i].p2].y - point[bound[i].p1].y) * dist_diff / bound_dist

                point[bound[i].p1].x -= dx
                point[bound[i].p1].y -= dy
                point[bound[i].p2].x += dx
                point[bound[i].p2].y += dy
        '''

    #locking the first and the last point of the first line
    point[0].x = init_x_offset
    point[0].y = init_y_offset
    point[int((xpoints_num-1)/2)].x = (int((xpoints_num-1)/2)) * distance  + init_x_offset
    point[int((xpoints_num-1)/2)].y = init_y_offset
    point[xpoints_num-1].x = (xpoints_num-1) * distance  + init_x_offset
    point[xpoints_num-1].y = init_y_offset
    
    #cutting bounds when right-click is held
    keys = pg.key.get_pressed()
    if right_button_held or keys[pg.K_SPACE]:
        ind = 0  
        while ind < len(bound):
            
            mouse_position.x = pg.mouse.get_pos()[0]
            mouse_position.y = pg.mouse.get_pos()[1]
            temp_mouse_pos.x = mouse_position.px
            temp_mouse_pos.y = mouse_position.py
            if do_intersect(point[bound[ind].p1], point[bound[ind].p2], mouse_position, temp_mouse_pos):
                bound.pop(ind)  
                bound_num -= 1 
            else:
                ind += 1 

    mouse_position.px = pg.mouse.get_pos()[0]
    mouse_position.py = pg.mouse.get_pos()[1]


    #clear screen
    win.fill((0, 0, 0))
    #drawing lines
    for i in range(bound_num):
        pg.draw.line(win , (255,255,255), (point[bound[i].p1].x, point[bound[i].p1].y), (point[bound[i].p2].x, point[bound[i].p2].y)) 
    
    for i in range(points_num):
        pg.draw.circle(win, (255, 0, 0), (point[i].x, point[i].y), 1) 

    #render
    pg.display.update() 
    clock.tick(60) 
