# TechNews

此项目是一个通过飞书机器人每日推送科技和 AI 资讯的自动化脚本，数据来源于 NewsAPI。

项目支持通过不同的飞书 Webhook 分别推送科技资讯与
AI 资讯。

## 目录结构

```
TechNews/
├── config/
│   ├── __init__.py
│   └── settings.py             # 加载环境变量
├── news/
│   ├── __init__.py
│   ├── fetcher.py               # 获取新闻
│   └── filter.py                # 过滤新闻
├── feishu/
│   ├── __init__.py
│   ├── sender.py               # 向飞书 Webhook 推送消息
│   └── signature.py            # 计算飞书签名
├── main.py                     # 主入口文件
└── README.md                   # 项目文档
```

## 环境需求

- Python 3.10+
- 自定义飞书机器人（拥有 Webhook 及签名密钥）
- NewsAPI API 密钥，用于获取新闻数据

## 安装

1. **克隆代码库**

   ```bash
   git clone https://github.com/qiu121/TechNews.git
   cd TechNews
   ```
2. **配置虚拟环境**

   ```bash
   python -m venv .venv
   ```
   Linux
   ```bash
   source .venv/bin/activate
   ```
   windows
   ```bash
   ./venv/Scripts/activate
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

4. **Github Actions 配置**

   本项目通过 GitHub Actions 定时推送新闻资讯，
   需要在 GitHub 项目的 `Settings` > `Secrets and variables `> `Actions` 中配置以下
   secrets：
   以便在运行工作流时使用

   - `FEISHU_WEBHOOK_URL`：飞书科技资讯 Webhook URL
   - `FEISHU_SIGNING_KEY`：飞书科技资讯签名密钥
   - `FEISHU_AI_WEBHOOK_URL`：飞书 AI 资讯 Webhook URL
   - `FEISHU_AI_SIGNING_KEY`：飞书 AI 资讯签名密钥
   - `NEWS_API_KEY`：NewsAPI key
   
   获取 NewsAPI key 请访问：
   https://newsapi.org/register

   请注意，这些变量在 GitHub Actions 的工作流中通过 `secrets` 设置，而不是在本地 `.env` 文件中设置。

## 使用说明

### 运行主程序

在项目根目录下运行以下命令（用于本地开发调试）：

```bash
python main.py
```

### 主要文件说明

- `config/settings.py`：从环境变量加载配置
- `news/fetcher.py`：从 NewsAPI 获取新闻数据
- `news/fetcher.py`：过滤科技和 AI 资讯
- `feishu/sender.py`：将筛选后的新闻推送至飞书
- `feishu/signature.py`：计算飞书 Webhook 所需签名

## 示例输出

程序会打印每条新闻的标题、描述、链接和发布日期，并将它们发布到指定的飞书 Webhook。

## 常见问题

1. **NewsAPIException**：请检查 API 密钥是否有效，日期格式是否正确。
2. **签名错误**：确保 GitHub Actions 中的签名密钥正确。
3. **Webhook 错误**：请确认 Webhook 设置及飞书机器人权限配置。