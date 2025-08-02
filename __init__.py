import tkinter as tk
from tkinter import ttk, messagebox

from data import enchantments, attribute_types, slot_options, operation_types
class IDK:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft 组件生成器")
        self.root.geometry("800x700")

        # 初始化数据
        self.color_codes = {
            "0": "黑色", "1": "深蓝", "2": "深绿", "3": "湖蓝",
            "4": "深红", "5": "紫色", "6": "金色", "7": "灰色",
            "8": "深灰", "9": "蓝色", "a": "浅绿", "b": "天蓝",
            "c": "红色", "d": "粉红", "e": "黄色", "f": "白色",
            "k": "随机字符", "l": "粗体", "m": "删除线", "n": "下划线",
            "o": "斜体", "r": "重置样式"
        }
        self.enchantments = enchantments
        self.attribute_types = attribute_types
        self.slot_options = slot_options
        self.operation_types = operation_types
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        self.notebook.enable_traversal()
        self.enchant_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.enchant_tab, text="附魔组件")
        
        self.attribute_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.attribute_tab, text="属性组件")
        self.notebook.select(self.enchant_tab)
        self.setup_enchantment_tab()
        self.setup_attribute_tab()
        
        self.name_lore_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.name_lore_tab, text="名称与描述")

        self.setup_name_lore_tab()
        
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(self.result_frame, text="生成的组件:").pack(anchor="w")
        self.result_text = tk.Text(self.result_frame, height=4, wrap="word")
        self.result_text.pack(fill="x", pady=(0, 10))
        tk.Button(self.result_frame, text="复制到剪贴板", command=self.copy_to_clipboard).pack(pady=5)
    
    def setup_enchantment_tab(self):

        self.enchantments = enchantments
        
        self.selected_enchantments = {}
        
        # 创建滚动框架
        self.enchant_canvas = tk.Canvas(self.enchant_tab)
        self.enchant_scrollbar = tk.Scrollbar(self.enchant_tab, orient="vertical", command=self.enchant_canvas.yview)
        self.enchant_scrollable_frame = tk.Frame(self.enchant_canvas)
        
        self.enchant_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.enchant_canvas.configure(
                scrollregion=self.enchant_canvas.bbox("all")
            )
        )
        
        self.enchant_canvas.create_window((0, 0), window=self.enchant_scrollable_frame, anchor="nw")
        self.enchant_canvas.configure(yscrollcommand=self.enchant_scrollbar.set)
        
        # 添加鼠标滚轮支持
        self.enchant_canvas.bind_all("<MouseWheel>", lambda event: self.enchant_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.enchant_canvas.pack(side="left", fill="both", expand=True)
        self.enchant_scrollbar.pack(side="right", fill="y")
        
        # 添加附魔选项
        for i, (enchant_id, enchant_name) in enumerate(self.enchantments.items()):
            frame = tk.Frame(self.enchant_scrollable_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            var = tk.IntVar()
            cb = tk.Checkbutton(frame, text=enchant_name, variable=var)
            cb.pack(side="left")
            
            tk.Label(frame, text="等级:").pack(side="left", padx=(10, 0))
            level_entry = tk.Entry(frame, width=3)
            level_entry.insert(0, "1")
            level_entry.pack(side="left")
            
            self.selected_enchantments[enchant_id] = {"var": var, "entry": level_entry}
        
        tk.Button(self.enchant_tab, text="生成附魔组件", command=self.generate_enchantment, 
                 bg="#4CAF50", fg="white").pack(pady=10)
    
    def setup_attribute_tab(self):

        self.attribute_list = []

        add_frame = tk.Frame(self.attribute_tab)
        add_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(add_frame, text="属性类型:").grid(row=0, column=0, sticky="e")
        self.attr_type_var = tk.StringVar()
        self.attr_type_menu = ttk.Combobox(add_frame, textvariable=self.attr_type_var, 
                                         values=list(self.attribute_types.values()), state="readonly")
        self.attr_type_menu.grid(row=0, column=1, sticky="we")
        self.attr_type_menu.set(list(self.attribute_types.values())[0])
        
        tk.Label(add_frame, text="装备槽位:").grid(row=1, column=0, sticky="e")
        self.slot_var = tk.StringVar()
        self.slot_menu = ttk.Combobox(add_frame, textvariable=self.slot_var, 
                                     values=list(self.slot_options.values()), state="readonly")
        self.slot_menu.grid(row=1, column=1, sticky="we")
        self.slot_menu.set(list(self.slot_options.values())[0])
        
        tk.Label(add_frame, text="操作类型:").grid(row=2, column=0, sticky="e")
        self.op_var = tk.StringVar()
        self.op_menu = ttk.Combobox(add_frame, textvariable=self.op_var, 
                                  values=list(self.operation_types.values()), state="readonly")
        self.op_menu.grid(row=2, column=1, sticky="we")
        self.op_menu.set(list(self.operation_types.values())[0])
        
        tk.Label(add_frame, text="数值:").grid(row=3, column=0, sticky="e")
        self.amount_var = tk.StringVar(value="1.0")
        tk.Entry(add_frame, textvariable=self.amount_var).grid(row=3, column=1, sticky="we")
        
        tk.Button(add_frame, text="添加属性", command=self.add_attribute, 
                 bg="#2196F3", fg="white").grid(row=4, column=0, columnspan=2, pady=5, sticky="we")
        
        self.attribute_listbox = tk.Listbox(self.attribute_tab)
        self.attribute_listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        tk.Button(self.attribute_tab, text="删除选中属性", command=self.remove_attribute, 
                 bg="#f44336", fg="white").pack(pady=5)
        
        tk.Button(self.attribute_tab, text="生成属性组件", command=self.generate_attribute, 
                 bg="#4CAF50", fg="white").pack(pady=10)
    
    def setup_name_lore_tab(self):
        main_frame = ttk.Frame(self.name_lore_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = ttk.Frame(main_frame, width=200)
        right_frame.pack(side="right", fill="y")
        
        ttk.Label(left_frame, text="物品名称:").pack(anchor="w", pady=(5, 0))
        self.item_name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.item_name_var).pack(fill="x", pady=(0, 10))
        
        ttk.Label(left_frame, text="自定义名称(显示名称):").pack(anchor="w", pady=(5, 0))
        self.custom_name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.custom_name_var).pack(fill="x", pady=(0, 10))
        
        ttk.Label(left_frame, text="物品描述(每行一个描述):").pack(anchor="w", pady=(5, 0))
        self.lore_text = tk.Text(left_frame, height=5)
        self.lore_text.pack(fill="x", pady=(0, 10))
        
        ttk.Label(left_frame, text="颜色代码:").pack(anchor="w")
        color_frame = ttk.Frame(left_frame)
        color_frame.pack(fill="x", pady=(0, 10))
        
        row_frame = None
        for i, (code, desc) in enumerate(self.color_codes.items()):
            if i % 4 == 0:
                row_frame = ttk.Frame(color_frame)
                row_frame.pack(fill="x")
            
            btn = ttk.Button(row_frame, text=f"§{code} {desc}", width=10,
                            command=lambda c=code: (self.root.clipboard_clear(), self.root.clipboard_append(f"§{c}")))
            btn.pack(side="left", padx=2, pady=2)
        
        ttk.Button(left_frame, text="生成名称与描述组件", 
                command=self.generate_name_lore).pack(pady=10)
        
        info_text = """组件说明:

1. minecraft:item_name
- 控制物品的默认名称
- 无法通过铁砧修改
- 不能在物品展示框中显示
- 对旗帜地图标记无效

2. minecraft:custom_name
- 自定义显示名称
- 默认为斜体
- 可通过铁砧修改

3. minecraft:lore
- 物品描述信息
- 每行一个元素
- 最多64行
- 支持颜色代码(§)"""
        
        ttk.Label(right_frame, text="组件说明", font=('Arial', 10, 'bold')).pack(pady=(5, 0))
        ttk.Label(right_frame, text=info_text, wraplength=180).pack(pady=5)
    
    def add_attribute(self):
        attr_type = self.get_key_from_value(self.attribute_types, self.attr_type_var.get())
        slot = self.get_key_from_value(self.slot_options, self.slot_var.get())
        operation = self.get_key_from_value(self.operation_types, self.op_var.get())
        amount = self.amount_var.get()
        
        try:
            float(amount)  # 验证是否为数字
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
            return
        
        attr_data = {
            "type": attr_type,
            "slot": slot,
            "operation": operation,
            "amount": amount
        }
        
        self.attribute_list.append(attr_data)
        self.update_attribute_listbox()
    
    def remove_attribute(self):
        selection = self.attribute_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        self.attribute_list.pop(index)
        self.update_attribute_listbox()
    
    def update_attribute_listbox(self):
        self.attribute_listbox.delete(0, tk.END)
        for attr in self.attribute_list:
            display_text = f"{self.attribute_types[attr['type']]} ({self.slot_options[attr['slot']]}) "
            display_text += f"{attr['amount']} ({self.operation_types[attr['operation']]})"
            self.attribute_listbox.insert(tk.END, display_text)
    
    def generate_enchantment(self):
        # 收集选中的附魔
        enchantments = {}
        for enchant_id, data in self.selected_enchantments.items():
            if data["var"].get() == 1:  # 复选框被选中
                try:
                    level = int(data["entry"].get())
                    if level < 1:
                        raise ValueError
                    enchantments[enchant_id] = level
                except ValueError:
                    messagebox.showerror("错误", f"附魔 {self.enchantments[enchant_id]} 的等级必须是正整数")
                    return
        
        if not enchantments:
            messagebox.showerror("错误", "请至少选择一个附魔")
            return
        
        # 构建组件
        component = f"minecraft:enchantments={enchantments}"
        
        # 显示结果
        self.show_result(component)
    
    def generate_attribute(self):
        if not self.attribute_list:
            messagebox.showerror("错误", "请至少添加一个属性")
            return
        
        modifiers = []
        for attr in self.attribute_list:
            modifier = {
                "type": attr["type"],
                "id": "minecraft:base_" + attr["type"],
                "slot": attr["slot"],
                "amount": float(attr["amount"]),
                "operation": attr["operation"]
            }
            modifiers.append(modifier)
        
        # 构建组件
        component = f"attribute_modifiers={modifiers}"

        # 显示结果
        self.show_result(component)
        
    def generate_name_lore(self):
        """生成名称和描述组件"""
        components = []
        
        # 处理item_name
        item_name = self.item_name_var.get().strip()
        if item_name:
            components.append(f"minecraft:item_name='{item_name}'")
        
        # 处理custom_name
        custom_name = self.custom_name_var.get().strip()
        if custom_name:
            components.append(f"minecraft:custom_name='{custom_name}'")
        
        # 处理lore
        lore_lines = self.lore_text.get("1.0", tk.END).strip().split('\n')
        lore_lines = [line.strip() for line in lore_lines if line.strip()]
        if lore_lines:
            lore_str = "[" + ",".join(f"'{line}'" for line in lore_lines) + "]"
            components.append(f"minecraft:lore={lore_str}")
        
        if not components:
            messagebox.showerror("错误", "请至少填写一个名称或描述")
            return
        
        # 构建组件
        component = ",".join(components)
        self.show_result(component)
        
    def show_result(self, component):
        """显示结果并转换颜色代码"""
        formatted_component = component.replace("§", "\\u00a7")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, formatted_component)
    
    def copy_to_clipboard(self):
        component = self.result_text.get(1.0, tk.END).strip()
        if component:
            # 确保颜色代码是 \u00a7 格式
            final_component = component.replace("§", "\\u00a7")
            self.root.clipboard_clear()
            self.root.clipboard_append(final_component)
            messagebox.showinfo("成功", "组件已复制到剪贴板")
        else:
            messagebox.showerror("错误", "没有可复制的内容")
    
    @staticmethod
    def get_key_from_value(dictionary, value):
        for k, v in dictionary.items():
            if v == value:
                return k
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = IDK(root)
    root.mainloop()