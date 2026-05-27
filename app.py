import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

DB_FILE = 'quant_system.db'

class AccountManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("量化系统后台 - 账号管理工具")
        self.root.geometry("600x400")
        
        self.init_db()
        self.setup_ui()
        self.load_users()

    def init_db(self):
        """初始化数据库和用户表"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                expire_date TEXT NOT NULL,
                is_active INTEGER DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()

    def setup_ui(self):
        """配置图形界面"""
        # 顶部表单区域
        frame_top = tk.Frame(self.root, pady=10)
        frame_top.pack(fill=tk.X)

        tk.Label(frame_top, text="用户名:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(frame_top)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_top, text="密码:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_password = tk.Entry(frame_top, show="*")
        self.entry_password.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_top, text="到期时间(YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_expire = tk.Entry(frame_top)
        self.entry_expire.insert(0, "2026-12-31")
        self.entry_expire.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_top, text="状态:").grid(row=1, column=2, padx=5, pady=5)
        self.status_var = tk.IntVar(value=1)
        tk.Checkbutton(frame_top, text="启用", variable=self.status_var).grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        # 按钮区域
        frame_btn = tk.Frame(self.root, pady=10)
        frame_btn.pack(fill=tk.X)
        tk.Button(frame_btn, text="保存/更新账号", command=self.save_user, bg="#1890ff", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_btn, text="删除选中账号", command=self.delete_user, bg="#ff4d4f", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_btn, text="清空输入框", command=self.clear_inputs, width=15).pack(side=tk.LEFT, padx=10)

        # 底部数据列表
        columns = ("ID", "用户名", "到期时间", "状态")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def save_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        expire_date = self.entry_expire.get().strip()
        is_active = self.status_var.get()

        if not username or not expire_date:
            messagebox.showwarning("验证失败", "用户名和到期时间不能为空")
            return

        try:
            datetime.strptime(expire_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("验证失败", "日期格式错误，请使用 YYYY-MM-DD")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # 更新已存在用户
            if password:
                pwd_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute("UPDATE users SET password_hash=?, expire_date=?, is_active=? WHERE username=?",
                               (pwd_hash, expire_date, is_active, username))
            else:
                cursor.execute("UPDATE users SET expire_date=?, is_active=? WHERE username=?",
                               (expire_date, is_active, username))
            msg = "账号更新成功"
        else:
            # 新建用户
            if not password:
                messagebox.showwarning("验证失败", "新建用户必须设置密码")
                conn.close()
                return
            pwd_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("INSERT INTO users (username, password_hash, expire_date, is_active) VALUES (?, ?, ?, ?)",
                           (username, pwd_hash, expire_date, is_active))
            msg = "账号添加成功"

        conn.commit()
        conn.close()
        messagebox.showinfo("成功", msg)
        self.clear_inputs()
        self.load_users()

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("提示", "请先在列表中选中一个账号")
            return
            
        username = self.tree.item(selected_item)['values'][1]
        if messagebox.askyesno("确认", f"确定要删除账号 '{username}' 吗？"):
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            conn.close()
            self.load_users()
            self.clear_inputs()

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, expire_date, is_active FROM users")
        for row in cursor.fetchall():
            status = "启用" if row[3] == 1 else "禁用"
            self.tree.insert("", tk.END, values=(row[0], row[1], row[2], status))
        conn.close()

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.clear_inputs()
            self.entry_username.insert(0, values[1])
            self.entry_expire.insert(0, values[2])
            self.status_var.set(1 if values[3] == "启用" else 0)

    def clear_inputs(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_expire.delete(0, tk.END)
        self.status_var.set(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountManagerApp(root)
    root.mainloop()
