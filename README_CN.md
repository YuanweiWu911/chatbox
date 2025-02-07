# Chat Application README

## 1. 项目概述
### Chatbox, 使用本地deepseek模型, 通过搜索引擎的API,实现最新知识的更新.

本聊天应用结合了 FastAPI 后端服务与 Tkinter 构建的图形用户界面（GUI），为用户提供了一个便捷的交互环境。用户在 GUI 界面输入查询内容，应用会先从 Redis 缓存中查找对应结果，若未命中则通过网络搜索获取相关信息，再调用本地的 Ollama 模型生成回答，并将结果缓存起来，以便后续查询使用。

## 2. 功能特性
### 2.1 后端功能
- **缓存机制**：使用 Redis 作为缓存，有效提高查询效率，减少重复查询的开销。
- **网络搜索**：借助 Serper API 进行网络搜索，精准获取相关的网页链接。
- **内容解析**：对搜索到的网页内容进行智能解析，提取有用信息。
- **模型调用**：调用本地的 Ollama 模型生成专业回答。

### 2.2 前端功能
- **图形用户界面（GUI）**：采用 Tkinter 构建直观易用的界面，方便用户输入查询和查看回复。
- **对话显示**：清晰展示用户的查询和机器人的回复，对不同类型的内容进行区分显示。
- **错误处理**：当输入为空、网络连接失败或服务器返回错误时，会弹出相应的错误提示框。

## 3. 安装步骤

### 3.1 克隆仓库
```bash
git clone https://github.com/YuanweiWu911/chatbox.git
cd chatbox
```

### 3.2 创建并激活虚拟环境（可选但推荐）
```bash
python -m venv chatbox
source chatbox/bin/activate  # 对于 Linux/Mac
.\chatbox\Scripts\activate  # 对于 Windows
```

### 3.3 安装依赖
```bash
pip install -r requirements.txt
```

### 3.4 配置环境变量
在项目根目录下创建一个 `.env` 文件，并添加以下内容：
```plaintext
REDIS_URL=redis://localhost:6379
SERPER_API_KEY=your_serper_api_key
PROXY_URL=your_proxy_url  # 如果需要代理，可设置该值
```
请将 `your_serper_api_key` 替换为你自己的 Serper API 密钥，`your_proxy_url` 替换为实际的代理地址（如果不需要代理，可留空）。

### 3.5 启动 Redis 服务
确保 Redis 服务已启动，你可以使用以下命令启动 Redis：
```bash
redis-server
```

### 3.6 启动 Ollama 服务
确保 Ollama 服务已启动，并且监听在 `http://localhost:11434` 端口。

## 4. 使用方法

### 4.1 启动后端服务
```bash
uvicorn app.main:app --reload --port 8000
```

### 4.2 启动前端 GUI
运行包含 GUI 代码的 Python 文件，通常是直接执行该文件：
```bash
python gui/gui.py  # 假设 GUI 代码文件名为 gui.py 且位于 gui 目录下
```

### 4.3  同时启动前端 GUI和后端服务
```bash
```bash
./start
```

### 4.4 与应用交互
- 在 GUI 界面的输入框中输入查询内容。
- 点击 “Send Query” 按钮发送查询请求。
- 查看聊天区域显示的用户查询和机器人回复。

## 5. 代码结构
```plaintext
chatbox/
├── app/
│   ├── __init__.py
│   ├── cache.py
│   ├── main.py
│   ├── parser.py
│   └── search.py
├── gui/
│   └── gui.py
├── tests/
│   ├── test_functions.py
│   └── test_main.py
├── .env
├── requirements.txt
├── test_functions.py
├── test_main.py
└── README.md
```
- `app/`：包含应用的核心后端代码。
  - `__init__.py`：标记该目录为 Python 包。
  - `cache.py`：实现 Redis 缓存管理功能。
  - `main.py`：应用的主入口文件，定义了 FastAPI 应用和路由。
  - `parser.py`：负责解析网页内容。
  - `search.py`：通过 Serper API 进行网络搜索。
- `gui/`：包含前端 GUI 代码。
  - `gui.py`：使用 Tkinter 构建的图形用户界面。
- `tests/`：包含测试代码。
- `.env`：环境变量配置文件。
- `requirements.txt`：项目依赖文件。

## 6. 错误处理与日志记录
### 6.1 后端
应用使用 Python 的 `logging` 模块进行日志记录，所有错误信息和重要事件都会记录在控制台中，方便调试和监控。

### 6.2 前端
在 GUI 界面中，当输入为空、网络连接失败或服务器返回错误时，会弹出相应的错误提示框，帮助用户及时了解问题。

## 7. 注意事项
- 请确保你的 Serper API 密钥有效，否则网络搜索功能将无法正常使用。
- 确保 Redis 服务和 Ollama 服务正常运行，否则缓存和模型调用功能将受影响。
- 若修改了后端服务的运行端口，需要相应地修改 GUI 代码中发送请求的 URL。

## 8. 贡献
如果你想为这个项目做出贡献，请提交 Pull Request 或者提出 Issues。

## 9. 许可证
本项目采用 [具体许可证名称] 许可证，请查看 `LICENSE` 文件获取详细信息。 
