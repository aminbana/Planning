
from plan import Plan
import cv2
from state import State
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import os

def sorter_func(stack):
    return stack[0]

class Graphic:
    
    def __init__(self):
        self.colors = None 
        self.bg_color = 230
        self.cube_size = 50
        self.horizontal_spacing = 80
    def plot_plan (self, s0:State, plan:Plan, path_to_save = None, filename = None, plot_result = True):
        canvases = []
        canvases.append(self.plot_state(s0))
        s = deepcopy(s0)
        for a in plan.actions:
            s = s.apply_unified_action(a)
            canvases.append(self.plot_state(s))
        
        max_height = max ([c.shape[0] for c in canvases])
        horizontal_spacing = self.horizontal_spacing
        width = sum ([c.shape[1] + horizontal_spacing for c in canvases])
        
        
        total_canvas = self.bg_color * np.ones([max_height, width, 3], dtype=np.uint8)

        last_x = 0
        for q, c in enumerate (canvases):
            y,x,_ = c.shape
            # print (last_x)
            # print ("c.shape:", c.shape)
            # print ("total_canvas[max_height-y:max_height,last_x:last_x+x].shape:", total_canvas[max_height-y:max_height,last_x:last_x+x].shape)
            total_canvas[max_height-y:max_height,last_x:last_x+x] = c
            last_x += x+horizontal_spacing
        
        last_x = 0
        for q, c in enumerate (canvases): 
            y,x,_ = c.shape
            last_x += x+horizontal_spacing   
            if q < len (plan.actions):
                total_canvas = cv2.putText(total_canvas, plan.actions[q].get_short_name(), (last_x - horizontal_spacing - 20, max_height - self.cube_size//2) , color=0, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8 , thickness=2)
                # total_canvas = cv2.arrowedLine(total_canvas, (last_x - horizontal_spacing - 20, 15) , (last_x - horizontal_spacing - 20 + 150, 15), (0, 0, 0), 2)

        
        total_canvas = cv2.putText(total_canvas, "S0", (canvases[0].shape[1]//2 - 10, max_height - (self.cube_size//2)) , color=0, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8 , thickness=2)
        total_canvas = cv2.putText(total_canvas, "Goal", (last_x - horizontal_spacing - (canvases[-1].shape[1]//2) - 15, max_height - (self.cube_size//2)) , color=0, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8 , thickness=2)

        if plot_result:
            plt.imshow(total_canvas)
            plt.axis('off')
            plt.show()

        if path_to_save is not None:
            try:
                os.makedirs(path_to_save)
            except:
                pass

            cv2.imwrite(path_to_save + filename + ".png" , total_canvas)

    def plot_state(self, s:State,):
        cube_size = self.cube_size

        propositions = s.propositions
        on_table_objects = [p.vars[0] for p in propositions if p.name == "on-table"]
        stacks = deepcopy (on_table_objects)
        stacks = [[d] for d in stacks]


        while True:
            last_ = deepcopy(stacks)
            for stack in stacks:
                last_cube = stack[-1]
                for p in propositions:
                    if p.name == "on" and p.vars[1] == last_cube:
                        stack.append(p.vars[0])
            if stacks == last_:
                break
        # print ("stacks:" , stacks)
                    

        # print ("on table objects:" , on_table_objects)

        
        holding_obj = None
        for p in propositions:
            if p.name == "holding":
                holding_obj = p.vars[0]
        
        stacks.sort(key=sorter_func)

        height = cube_size + cube_size * max ([len (stack) for stack in stacks]) + (cube_size * 2 if holding_obj is not None else 0)
        # print ("max height:" , height)

        width = len (on_table_objects) * cube_size * 2 + cube_size

        canvas = self.bg_color * np.ones ([height,width,3], dtype=np.uint8)

        
        
        if self.colors is None:
            self.colors = {}
            self.colors[holding_obj] = (np.random.randint(256), np.random.randint(256), np.random.randint(256))
            for stack in stacks:
                for c in stack:
                    self.colors[c] = (np.random.randint(256), np.random.randint(256), np.random.randint(256))

        for i,stack in enumerate (stacks):
            for j,name in enumerate (stack):
                p1 = ((2*i+1) * cube_size , height - (cube_size + j * cube_size))
                p2 = ((2*i+1) * cube_size + cube_size, height - (2*cube_size + j * cube_size))
                p_text = ((p1[0]+p2[0])//2 - cube_size//7 , (p1[1]+p2[1])//2 + cube_size//10)
                canvas = cv2.rectangle(canvas, p1, p2, self.colors[name], thickness = cv2.FILLED)

                cv2.putText(canvas, name, p_text, color=0, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8 , thickness=2)
        
        if holding_obj is not None:
            p1 = (width//2 - cube_size//2 , 0)
            p2 = (width//2 - cube_size//2 + cube_size, cube_size)
            p_text = ((p1[0]+p2[0])//2 - cube_size//7 , (p1[1]+p2[1])//2 + cube_size//10)
            canvas = cv2.rectangle(canvas, p1, p2, self.colors[holding_obj], thickness = cv2.FILLED)
            cv2.putText(canvas, holding_obj, p_text, color=0, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8 , thickness=2)
        canvas = cv2.line(canvas, (0,height - cube_size) , (width,height - cube_size) , color = 0 , thickness=1)
        
        plt.imshow(canvas)
        plt.show()
        return canvas




