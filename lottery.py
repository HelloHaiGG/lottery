import tkinter as tk
from tkinter import font
import yaml
import random
import time

class LotteryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("抽奖程序")
        
        # 加载配置
        with open('config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 初始化轮次和中奖记录
        self.current_round = 1
        self.total_rounds = self.config['total_rounds']
        self.winners = {}  # 存储每轮中奖号码
        self.used_numbers = set()  # 存储已经中奖的号码
        
        # 设置窗口
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#FF0000')
        
        self.is_running = False
        self.current_number = tk.StringVar(value="???")
        self.is_exiting = False  # 添加退出标志
        self.showing_result = False  # 初始化显示结果标志
        
        self.setup_ui()
        self.root.bind('<space>', self.toggle_lottery)
        self.root.bind('<Button-1>', self.toggle_lottery)
        
    def setup_ui(self):
        # 创建主Frame
        self.main_frame = tk.Frame(self.root, bg='#FF0000')
        self.main_frame.pack(expand=True, fill='both')
        
        # 创建左右两个Frame，并设置固定宽度
        screen_width = self.root.winfo_screenwidth()
        left_width = screen_width // 2
        
        left_frame = tk.Frame(self.main_frame, bg='#FF0000', width=left_width)
        right_frame = tk.Frame(self.main_frame, bg='#FF0000', width=left_width)
        
        # 防止Frame自动调整大小
        left_frame.pack_propagate(False)
        right_frame.pack_propagate(False)
        
        # 使用pack布局，确保左右两边固定
        left_frame.pack(side='left', fill='both', expand=True)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # 左边：大"囍"字
        xi_font = font.Font(family='SimHei', size=900, weight='bold')
        xi_label = tk.Label(
            left_frame,
            text="囍",
            font=xi_font,
            bg='#FF0000',
            fg='#FFD700'
        )
        xi_label.pack(expand=True)
        
        # 右边：创建一个固定大小的容器
        right_container = tk.Frame(right_frame, bg='#FF0000')
        right_container.pack(expand=True, fill='both', padx=50)
        
        # 轮次显示
        round_font = font.Font(family='SimHei', size=30)
        self.round_label = tk.Label(
            right_container,
            text=f"第{self.current_round}个 / 共{self.total_rounds}个",
            font=round_font,
            bg='#FF0000',
            fg='#FFD700'
        )
        self.round_label.pack(pady=30)
        
        # 创建中间显示区域的Frame
        self.display_frame = tk.Frame(right_container, bg='#FF0000')
        self.display_frame.pack(expand=True)
        
        # 数字显示（初始不显示）
        number_font = font.Font(family='Arial', size=256, weight='bold')
        self.number_label = tk.Label(
            self.display_frame,
            textvariable=self.current_number,
            font=number_font,
            bg='#FF0000',
            fg='#FFD700'
        )
        
        # 开始/结果提示标签
        self.message_font = font.Font(family='SimHei', size=100, weight='bold')
        self.message_label = tk.Label(
            self.display_frame,
            text=f"开始第{self.current_round}个抽奖",
            font=self.message_font,
            bg='#FF0000',
            fg='#FFD700'
        )
        self.message_label.pack(expand=True)
    
    def update_number(self):
        if self.is_running and not self.is_exiting:
            # 获取所有可用号码
            available_numbers = [
                str(i).zfill(3) 
                for i in range(1, self.config['number_range']['end'] + 1)
                if str(i).zfill(3) not in self.used_numbers
            ]
            
            # 如果还有可用号码
            if available_numbers:
                self.current_number.set(random.choice(available_numbers))
                self.root.after(50, self.update_number)
            else:
                # 如果没有可用号码，停止抽奖并显示提示
                self.is_running = False
                self.message_label.configure(text="已无可用号码")
                self.message_label.pack(expand=True)
    
    def show_final_results(self):
        # 清除主界面
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # 获取屏幕宽度并计算左右Frame宽度
        screen_width = self.root.winfo_screenwidth()
        left_width = screen_width // 2
        
        # 创建左右Frame并设置固定宽度
        left_frame = tk.Frame(self.main_frame, bg='#FF0000', width=left_width)
        right_frame = tk.Frame(self.main_frame, bg='#FF0000', width=left_width)
        
        # 防止Frame自动调整大小
        left_frame.pack_propagate(False)
        right_frame.pack_propagate(False)
        
        # 使用pack布局
        left_frame.pack(side='left', fill='both', expand=True)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # 左边：大"囍"字
        xi_font = font.Font(family='SimHei', size=900, weight='bold')
        xi_label = tk.Label(
            left_frame,
            text="囍",
            font=xi_font,
            bg='#FF0000',
            fg='#FFD700'
        )
        xi_label.pack(expand=True)
        
        # 右边：创建固定大小的容器
        right_container = tk.Frame(right_frame, bg='#FF0000')
        right_container.pack(expand=True, fill='both', padx=50)
        
        # 显示结果标题
        title_font = font.Font(family='SimHei', size=60, weight='bold')
        title_label = tk.Label(
            right_container,
            text="抽 奖 结 束",
            font=title_font,
            bg='#FF0000',
            fg='#FFD700'
        )
        title_label.pack(pady=50)
        
        # 创建一个Frame来容纳中奖名单
        winners_frame = tk.Frame(right_container, bg='#FF0000')
        winners_frame.pack(expand=True)
        
        # 显示中奖名单
        result_font = font.Font(family='SimHei', size=36)
        
        # 计算网格布局的行列数（每行4个）
        COLS = 4
        total_winners = len(self.winners)
        ROWS = (total_winners + COLS - 1) // COLS  # 向上取整
        
        # 使用网格布局显示中奖名单
        for round_num in sorted(self.winners.keys(), key=int):
            idx = int(round_num) - 1  # 转换为0基索引
            row = idx // COLS
            col = idx % COLS
            
            winner = self.winners[round_num]
            result_label = tk.Label(
                winners_frame,
                text=f"第{round_num}个: {winner}号",
                font=result_font,
                bg='#FF0000',
                fg='#FFD700'
            )
            result_label.grid(row=row, column=col, padx=30, pady=15)
        
        # 添加祝贺文本
        congrats_font = font.Font(family='SimHei', size=40, weight='bold')
        congrats_label = tk.Label(
            right_container,
            text="恭喜中奖！",
            font=congrats_font,
            bg='#FF0000',
            fg='#FFD700'
        )
        congrats_label.pack(pady=30)
        
        # 添加提示文本
        hint_font = font.Font(family='SimHei', size=24)
        hint_label = tk.Label(
            right_container,
            text="按空格键退出程序",
            font=hint_font,
            bg='#FF0000',
            fg='#FFD700'
        )
        hint_label.pack(pady=10)
    
    def quit_app(self):
        """优雅退出程序"""
        self.is_exiting = True
        self.root.quit()
    
    def toggle_lottery(self, event=None):
        if self.is_exiting:
            return
        
        if hasattr(self, 'winners') and len(self.winners) == self.total_rounds:
            # 如果所有轮次都已完成，按空格键退出
            self.quit_app()
            return
        
        if not self.is_running:
            if self.showing_result:
                self.showing_result = False
                self.prepare_next_round()
            else:
                # 检查是否还有可用号码
                available_count = self.config['number_range']['end'] - len(self.used_numbers)
                if available_count > 0:
                    self.message_label.pack_forget()
                    self.number_label.pack(expand=True)
                    self.is_running = True
                    self.update_number()
                else:
                    self.message_label.configure(text="已无可用号码")
        else:
            # 停止抽奖
            self.is_running = False
            
            # 获取中奖号码
            current_number = self.current_number.get()
            
            # 检查是否是固定中奖轮次
            fixed_winner_config = self.config.get('fixed_winner', {})
            if (fixed_winner_config.get('round') == self.current_round and 
                fixed_winner_config.get('number')):
                current_number = fixed_winner_config['number']
                self.current_number.set(current_number)
            
            # 记录中奖号码并添加到已使用集合
            self.winners[str(self.current_round)] = current_number
            self.used_numbers.add(current_number)
            
            # 显示本轮中奖结果
            self.number_label.pack_forget()
            self.message_label.configure(text=f"中奖号码：{current_number}号")
            self.message_label.pack(expand=True)
            
            # 标记正在显示结果
            self.showing_result = True
    
    def prepare_next_round(self):
        """准备下一轮抽奖"""
        if self.current_round < self.total_rounds:
            # 检查是否还有可用号码
            available_count = self.config['number_range']['end'] - len(self.used_numbers)
            if available_count > 0:
                self.current_round += 1
                self.round_label.config(text=f"第{self.current_round}个 / 共{self.total_rounds}个")
                
                # 显示下一轮开始提示
                self.message_label.configure(text=f"开始第{self.current_round}个抽奖")
                self.message_label.pack(expand=True)
            else:
                # 如果没有可用号码，直接显示最终结果
                self.show_final_results()
        else:
            # 所有轮次结束，显示最终结果
            self.show_final_results()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LotteryApp()
    app.run() 