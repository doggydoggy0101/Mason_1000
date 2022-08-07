from tkinter import *
from tkinter import messagebox as mb
import random
import json

def generate_gre(question, answer, num,  mode):

    if mode == "R": 
        zz = list(zip(question,answer))
        random.shuffle(zz)
        question,answer = zip(*zz)
    question = question[:num]

    ans, opt = [], []
    for i in range(len(question)):

        options = [0,0,0,0]  
        while True:
            rand_label = random.sample(range(len(answer)), 4)
            check = 0
            for cc in rand_label:
                if cc != i: check += 1
            if check == 4: break

        for ii in range(4): options[ii] = answer[int(rand_label[ii])]

        label = random.randint(0,3)
        options[label] = answer[i]

        ans.append(label+1)
        opt.append(options)

    return question, ans, opt

class Quiz:

    def __init__(self):

        self.q_no = 0
        self.display_title()
        self.display_question()
        self.opt_selected = IntVar()
        self.opts = self.radio_buttons()
        self.display_options()
        self.buttons()
        self.data_size = len(question)
        self.correct = 0

    def display_result(self):
         
        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"
         
        score = int(self.correct / self.data_size * 100)
        result = f"Score: {score}%"
         
        mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")
 
    def check_ans(self, q_no):

        if self.opt_selected.get() == answer[q_no]: return True
 
    def next_btn(self):

        if self.check_ans(self.q_no): self.correct += 1
        else: mb.showinfo("Wrong", f"{question[self.q_no]} {options[self.q_no][answer[self.q_no]-1]}")
         
        self.q_no += 1
        self.display_title()
         
        if self.q_no == self.data_size:
            self.display_result()
            gui.destroy()
        else:
            self.display_question()
            self.display_options()

    def buttons(self):
         
        next_button = Button(gui, text="下一題",command=self.next_btn, width=10, font=("ariel",16,"bold"))  
        next_button.place(x=255,y=330)
         
        quit_button = Button(gui, text="結束", command=gui.destroy, width=5, font=("ariel",16," bold"))
        quit_button.place(x=480,y=330)
 
    def display_options(self):
        val = 0
        self.opt_selected.set(0)
         
        for option in options[self.q_no]:
            self.opts[val]['text'] = option
            val += 1
 
    def display_question(self):
         
        q_no = Label(gui, text=question[self.q_no], width=60, font=('ariel',16,'bold'), anchor= 'w' )
        q_no.place(x=70, y=80)
 
    def display_title(self):
         
        title = Label(gui, text="第{}題".format(self.q_no+1), width=50, bg="#123456",fg="white", font=("ariel",20,"bold"))
        title.place(x=0, y=0)
 
    def radio_buttons(self):
         
        q_list = []
        y_pos = 140
         
        while len(q_list) < 4:
             
            radio_btn = Radiobutton(gui,text=" ",variable=self.opt_selected, value = len(q_list)+1,font = ("ariel",14))
            q_list.append(radio_btn)
            radio_btn.place(x = 100, y = y_pos)
            y_pos += 40

        return q_list


with open('mason_1000.json') as f: data = json.load(f)
english, chinese = data["english"], data["chinese"]

input_num = input("\nNumber of Questions? (default: 10)\nPlease enter number: ")
input_mode = input("\nQuestion in Normal or Random order? (default: Normal)\nPlease enter \"N\" or \"R\": ")
input_language = input("\nQuestion is in English or Chinese order? (default: English)\nPlease enter \"E\" or \"C\": ")

NUM = int(input_num) if input_num.isdigit() == True else 10
MODE = "R" if input_mode == "R" else "N"

if input_language == "C":
    QUESTION = chinese
    ANSWER = english
else: 
    QUESTION = english
    ANSWER = chinese


question,answer,options =generate_gre(QUESTION, ANSWER, NUM, MODE)   

gui = Tk()
gui.geometry("650x420")
gui.resizable(False, False)
gui.title("GRE 340")
quiz = Quiz()
gui.mainloop()
