import customtkinter as ctk
import json
import os
from tkinter import messagebox

# 设置界面主题和色调
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ModernTodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ZenTask - Personal Manager")
        self.geometry("600x700")
        
        # 数据存储设置
        self.data_file = "tasks.json"
        self.tasks = self.load_data()

        # UI 布局 (Demonstrating Padding/Margin concepts)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 标题栏
        self.label = ctk.CTkLabel(self, text="ZenTask Manager", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 输入区域
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="What needs to be done?", width=350)
        self.entry.pack(side="left", padx=10, pady=10)
        
        self.priority_opt = ctk.CTkOptionMenu(self.input_frame, values=["Low", "Medium", "High"], width=100)
        self.priority_opt.pack(side="left", padx=5)
        self.priority_opt.set("Medium")

        self.add_btn = ctk.CTkButton(self.input_frame, text="+", width=40, command=self.add_task)
        self.add_btn.pack(side="left", padx=10)

        # 任务显示区域
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Your Tasks")
        self.scrollable_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.refresh_list()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self):
        content = self.entry.get()
        priority = self.priority_opt.get()
        if content:
            self.tasks.append({"content": content, "priority": priority, "status": "Active"})
            self.save_data()
            self.entry.delete(0, 'end')
            self.refresh_list()
        else:
            messagebox.showwarning("Empty Task", "Please enter a task description.")

    def delete_task(self, task_obj):
        self.tasks.remove(task_obj)
        self.save_data()
        self.refresh_list()

    def refresh_list(self):
        # 清空当前列表
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 按照优先级排序 (Algorithm)
        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        sorted_tasks = sorted(self.tasks, key=lambda x: priority_map.get(x['priority'], 1))

        for task in sorted_tasks:
            item_frame = ctk.CTkFrame(self.scrollable_frame)
            item_frame.pack(fill="x", pady=5, padx=5)
            
            color = "#ff4d4d" if task['priority'] == "High" else "#ffcc00" if task['priority'] == "Medium" else "#4db8ff"
            
            p_label = ctk.CTkLabel(item_frame, text=f"[{task['priority']}]", text_color=color, font=ctk.CTkFont(size=10, weight="bold"))
            p_label.pack(side="left", padx=10)
            
            content_label = ctk.CTkLabel(item_frame, text=task['content'], font=ctk.CTkFont(size=13))
            content_label.pack(side="left", padx=10, fill="x", expand=True)
            
            del_btn = ctk.CTkButton(item_frame, text="Delete", width=60, fg_color="transparent", border_width=1, 
                                    text_color=("gray10", "#DCE4EE"), command=lambda t=task: self.delete_task(t))
            del_btn.pack(side="right", padx=10, pady=5)

if __name__ == "__main__":
    app = ModernTodoApp()
    app.mainloop()
