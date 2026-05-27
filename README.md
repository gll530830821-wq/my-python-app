# 量化系统账号管理工具

一个使用 Python Tkinter 构建的图形化账号管理应用，支持用户的增删改查操作。

## 功能特性

- ✓ 用户账号管理（创建、更新、删除）
- ✓ 密码使用 bcrypt 加密存储
- ✓ 账号到期时间管理
- ✓ 账号启用/禁用状态
- ✓ SQLite 数据库存储
- ✓ 图形化用户界面

## 系统要求

- Python 3.7+
- Windows、macOS 或 Linux

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

### 方式一：直接运行 Python 脚本

```bash
python app.py
```

### 方式二：打包成可执行程序

#### 第一步：安装依赖
```bash
pip install -r requirements.txt
```

#### 第二步：运行打包脚本
```bash
python build.py
```

或使用 PyInstaller 直接打包：
```bash
pyinstaller --onefile --windowed --name AccountManager --collect-all bcrypt app.py
```

#### 第三步：找到可执行文件
- **Windows**: `dist/AccountManager.exe`
- **macOS/Linux**: `dist/AccountManager`

## 使用说明

1. **添加新账号**
   - 填写用户名和密码
   - 设置到期时间（默认为 2026-12-31）
   - 点击"保存/更新账号"按钮

2. **修改账号**
   - 在列表中选择账号
   - 修改相应信息
   - 点击"保存/更新账号"按钮

3. **删除账号**
   - 在列表中选择账号
   - 点击"删除选中账号"按钮
   - 确认删除

## 数据存储

- 数据库文件：`quant_system.db`
- 密码使用 bcrypt 加密存储，加密安全

## 文件结构

```
.
├── app.py              # 主应用程序
├── build.py            # 打包脚本
├── requirements.txt    # Python 依赖
├── README.md           # 说明文档
└── quant_system.db     # 数据库文件（首次运行时创建）
```

## 打包输出

运行 `python build.py` 后会生成：
- `dist/` - 包含可执行程序的目录
- `build/` - 构建中间文件
- `AccountManager.spec` - PyInstaller 规范文件

## 常见问题

### Q: 如何在没有 Python 的电脑上运行？
A: 按照上述打包步骤生成可执行文件，即可在任何相同操作系统的电脑上直接运行。

### Q: 数据库文件在哪里？
A: 首次运行程序后，`quant_system.db` 文件会在程序所在目录创建。

### Q: 如何修改应用名称或图标？
A: 编辑 `build.py` 中的 `--name` 参数修改名称，添加 `icon.ico` 文件修改图标。

## 许可证

MIT
