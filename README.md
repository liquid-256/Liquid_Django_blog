# Liquid_Django_blog

## 项目简介

基于 **Django 5 + MySQL** 开发的个人博客系统，包含：

- 用户注册 / 登录
- 邮箱验证码
- 博客发布、评论、搜索
- 个人资料管理
- 后台管理

---


## 技术栈

- **后端**：Python 3.x、Django 5.x
- **数据库**：MySQL
- **前端**：Bootstrap 5、jQuery、HTML、CSS
- **富文本**：WangEditor、highlight.js
- **配置管理**：python-decouple + `.env`
- **部署**：Gunicorn + Nginx

---

## 项目结构

```text
Liquid_Django_blog/
├─ Django_blog/
│  ├─ settings/
│  │  ├─ base.py
│  │  ├─ dev.py
│  │  └─ prod.py
│  ├─ urls.py
│  └─ wsgi.py
├─ blog/
├─ liauth/
├─ templates/
├─ static/
├─ media/           # 含 .keep
├─ logs/            # 含 .keep
├─ gunicorn_conf.py
├─ requirements.txt
├─ .env.example
└─ manage.py
```

---

## 本地运行

### 1️⃣ 创建虚拟环境并安装依赖

```bash
python -m venv .venv
# Windows
.venvScriptsactivate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 2️⃣ 配置数据库与环境变量

**创建数据库：**

```sql
CREATE DATABASE django_blog CHARSET utf8mb4;
```

**配置环境变量：**

```bash
cp .env.example .env
```

**修改 `.env` 文件（示例）：**

```ini
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=django_blog
DB_USER=root
DB_PASSWORD=123456
DB_HOST=127.0.0.1
DB_PORT=3306

ALLOWED_HOSTS=127.0.0.1,localhost
```

### 3️⃣ 初始化数据库

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4️⃣ 启动项目

```bash
python manage.py runserver
```

访问地址：

```text
http://127.0.0.1:8000/
```

---

## 邮箱验证码配置（可选）

在 `.env` 中配置 SMTP 服务：

```ini
EMAIL_USE_TLS=True
EMAIL_HOST=smtp.qq.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@qq.com
EMAIL_HOST_PASSWORD=your-email-auth-code
DEFAULT_FROM_EMAIL=your-email@qq.com
```

---

## 生产环境部署（简要）

```bash
# 设置环境变量指向生产配置
export DJANGO_SETTINGS_MODULE=Django_blog.settings.prod

# 使用 Gunicorn 启动
gunicorn -c gunicorn_conf.py Django_blog.wsgi:application
```

最后使用 Nginx 反向代理到 `127.0.0.1:8000` 即可。
