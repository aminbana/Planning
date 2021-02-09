import cv2
from state import State
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

def sorter_func(stack):
    return stack[0]

class Graphic:
    
    def __init__(self):
        self.colors = None 

    def plot_state(self, s:State,):
        cube_size = 50

        propositions = s.propositions
        on_table_objects = [p.vars[0] for p in propositions if p.name == "ot"]
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
            if p.name == "hol":
                holding_obj = p.vars[0]
        
        stacks.sort(key=sorter_func)

        height = cube_size + cube_size * max ([len (stack) for stack in stacks]) + (cube_size * 2 if holding_obj is not None else 0)
        # print ("max height:" , height)

        width = len (on_table_objects) * cube_size * 2 + cube_size

        canvas = 230 * np.ones ([height,width,3], dtype=np.uint8)

        
        
        if self.colors is None:
            self.colors = {}
            self.colors[holding_obj] = (np.random.randint(256), np.random.randint(256), np.random.randint(256))
            for stack in stacks:
                for c in stack:
                    self.colors[c] = (np.random.randint(256), np.random.randint(256), np.random.randint(256))
        print (self.colors)
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




