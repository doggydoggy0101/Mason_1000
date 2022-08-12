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

class GRE340:

    def __init__(self):
        self.display_mainpage()

    def display_mainpage(self):
        for widget in gui.winfo_children(): widget.destroy()

        self.display_input()
        self.display_easter()

        title = Label(gui, text="Mason 1000", width=50, bg="#123456",fg="white", font=("ariel",20,"bold"))
        title.place(x=0, y=0)

        start_button = Button(gui, text="開始",command=self.start_btn, width=10, font=("ariel",16,"bold"))  
        start_button.place(x=255,y=355)
         
        quit_button = Button(gui, text="結束", command=gui.destroy, width=5, font=("ariel",16," bold"))
        quit_button.place(x=485,y=355)

    def start_btn(self):
        for widget in gui.winfo_children(): widget.destroy()

        with open(data_json) as f: data = json.load(f)
        english, chinese = data["english"], data["chinese"]

        NUM = int(self.num.get()) if self.num.get().isdigit() == True else 10
        MODE = "R" if self.mode.get() == "R" else "N"

        if self.language.get() == "C": QUESTION,ANSWER = chinese,english
        else: QUESTION,ANSWER = english,chinese
        self.question,self.answer,self.options = generate_gre(QUESTION, ANSWER, NUM, MODE)   

        self.q_no = 0
        self.display_title()
        self.display_easter()
        self.display_question()
        self.opt_selected = IntVar()
        self.opts = self.radio_buttons()
        self.display_options()
        self.buttons()
        self.data_size = len(self.question)
        self.correct = 0     

    def display_input(self):

        self.num, self.mode, self.language = StringVar(), StringVar(), StringVar()

        label_num = Label(gui, text="Number of Questions? (default: 10)", font=("ariel",16,"bold"))
        label_num.place(x=100, y=85)
        label_num = Label(gui, text="Please enter a number: ", font=("ariel",16))
        label_num.place(x=100, y=115)
        input_num = Entry(gui, width=16, textvariable=self.num)
        input_num.place(x=300, y=115)
 
        label_mode = Label(gui, text="Question in Normal or Random order? (default: Normal)", font=("ariel",16,"bold"))
        label_mode.place(x=100, y=165)
        label_mode = Label(gui, text="Please enter \"N\" or \"R\": ", font=("ariel",16))
        label_mode.place(x=100, y=195)
        input_mode = Entry(gui, width=16, textvariable=self.mode)
        input_mode.place(x=300, y=195)

        label_language = Label(gui, text="Question is in English or Chinese? (default: English)", font=("ariel",16,"bold"))
        label_language.place(x=100, y=245)
        label_language = Label(gui, text="Please enter \"E\" or \"C\": ", font=("ariel",16))
        label_language.place(x=100, y=275)
        input_language = Entry(gui, width=16, textvariable=self.language)
        input_language.place(x=300, y=275) 

    def display_result(self):
        for widget in gui.winfo_children(): widget.destroy()
         
        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"
         
        score = int(self.correct / self.data_size * 100)
        result = f"Score: {score}%"
         
        mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")
 
    def check_ans(self, q_no):

        if self.opt_selected.get() == self.answer[q_no]: return True
 
    def next_btn(self):

        if self.check_ans(self.q_no): self.correct += 1
        else: mb.showinfo("Wrong", f"{self.question[self.q_no]} {self.options[self.q_no][self.answer[self.q_no]-1]}")
         
        self.q_no += 1
        self.display_title()
         
        if self.q_no == self.data_size:
            self.display_result()
            self.display_mainpage()
        else:
            self.display_question()
            self.display_options()

    def buttons(self):
         
        next_button = Button(gui, text="下一題",command=self.next_btn, width=10, font=("ariel",16,"bold"))  
        next_button.place(x=255,y=355)
         
        quit_button = Button(gui, text="主畫面", command=self.display_mainpage, width=5, font=("ariel",16," bold"))
        quit_button.place(x=485,y=355)
 
    def display_options(self):
        val = 0
        self.opt_selected.set(0)
         
        for option in self.options[self.q_no]:
            self.opts[val]['text'] = option
            val += 1
 
    def display_question(self):
         
        q_no = Label(gui, text=self.question[self.q_no], width=60, font=('ariel',18,'bold'), anchor= 'w' )
        q_no.place(x=70, y=80)
 
    def display_title(self):
         
        title = Label(gui, text="第{}題 (共{}題)".format(self.q_no+1,len(self.question)), width=50, bg="#123456",fg="white", font=("ariel",20,"bold"))
        title.place(x=0, y=0)

    def display_easter(self):
        title = Label(gui, text="Made by 狗狗 & 歐拉", width=50, bg="#123456",fg="white", font=("ariel",20,"bold"))
        title.place(x=0, y=450)

    def radio_buttons(self):
         
        q_list = []
        y_pos = 145
         
        while len(q_list) < 4:
             
            radio_btn = Radiobutton(gui,text=" ",variable=self.opt_selected, value = len(q_list)+1,font = ("ariel",16))
            q_list.append(radio_btn)
            radio_btn.place(x = 100, y = y_pos)
            y_pos += 45

        return q_list

gui = Tk()
gui.title("GRE 340")
gui.geometry("650x420")
gui.minsize(650,420)
gui.maxsize(650,479)
gui.resizable(False, True)

data_json = "Mason_1000.json" # 1097

GRE340()
gui.mainloop()