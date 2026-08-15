# Typora S3图床上传脚本

一个用于 [Typora](https://typora.io/) 的自定义图床上传脚本，可将本地图片上传至 [S3图床](https://S3图床.net/) ，并返回 Markdown 可用的图片链接。

支持 Windows、macOS、Linux，修复了 Windows 下的中文乱码问题。

---

## 功能特性

- 使用 Cookie 登录 特定S3图床，自动提取 `auth_token`
- 支持多图片上传，返回可直接粘贴到 Markdown 的 URL
- 纯 `requests` 实现，无需浏览器
- 自动处理 Windows 控制台 UTF-8 输出

---

## 环境要求

- Python **3.7+**（使用了 `sys.stdout.reconfigure`）
- 第三方库：`requests`

安装依赖：

```bash
pip install requests
```


## 快速开始

### 1. 下载脚本

将 `upload_img.py` 保存到本地任意目录，例如：

- Windows：`C:\scripts\upload_img.py`
- macOS / Linux：`/home/user/scripts/upload_img.py`

### 2. 获取 S3图床 Cookie

1. 登录 [S3图床](https://S3图床.net/)
2. 打开 S3 图床页面：<https://S3图床网址/>
3. 按 `F12` 打开开发者工具，切换到 **网络（Network）** 选项卡
4. 刷新页面（`F5`）
5. 在请求列表中找到第一个指向 `https://S3图床网址/` 的请求
6. 在 **标头（Headers）** 中找到 `Cookie` 字段，复制其完整值
7. 打开 `upload_img.py`，将 `MY_COOKIE` 变量单引号内的内容替换为你复制的 Cookie

示例：

```python
MY_COOKIE = 'c_secure_pass=你的值; KEEP_LOGIN_GOAUTH=你的值; PHPSESSID=你的值'

> ⚠️ **安全警告**  
> Cookie 等同于你的登录凭证，请勿将包含真实 Cookie 的脚本提交到公开仓库，也不要分享给他人。  
```

### 3. 命令行测试

```bash
python upload_img.py /path/to/your/image.png
```

成功时输出示例：

```
Upload Success:
https://S3图床网址/xxxxx/xxxxx.png
```

---

## Typora 集成

1. 打开 Typora → **文件** → **偏好设置** → **图像**

2. 在 **上传服务** 中选择 **自定义命令**

3. 在 **命令** 输入框中填写（根据实际路径修改）：

   **Windows：**

   ```bash
   python C:\scripts\upload_img.py
   ```

   **macOS / Linux：**

   ```bash
   python3 /home/user/scripts/upload_img.py
   ```

4. 点击 **验证图片上传选项** 测试是否配置成功

5. 之后在 Typora 中插入图片时，会自动调用该脚本上传并替换为图床 URL

---

## 命令行用法

```bash
python upload_img.py <图片路径1> [图片路径2] ...
```

- 支持一次上传多张图片

- 成功时，标准输出为：

  ```
  Upload Success:
  <图片1的URL>
  <图片2的URL>
  ```

- 失败时，错误信息会输出到标准错误（stderr），对应行的标准输出为空字符串

---

## 配置项说明

脚本顶部有三个配置变量：

| 变量         | 说明                                |
| ------------ | ----------------------------------- |
| `HOME_URL`   | S3 图床首页地址，一般无需修改       |
| `UPLOAD_URL` | 上传接口地址，一般无需修改          |
| `MY_COOKIE`  | **必填**，你的 S3图床 Cookie 字符串 |

---

## 常见问题

### 1. 提示 `登录态失效 (GUEST_SESSION)`

Cookie 无效、过期或未正确粘贴。请重新获取 Cookie，并确保复制完整。

### 2. 提示 `TOKEN_NOT_FOUND`

可能原因：

- Cookie 不正确或已过期
- 图床页面结构更新，脚本中的正则表达式需要调整

### 3. Windows 下输出乱码

脚本已强制设置标准输出为 UTF-8。若仍乱码，请确认 Python 版本 ≥ 3.7，并尝试在命令行中执行：

```bash
chcp 65001
```

### 4. 上传失败 HTTP 4xx / 5xx

检查网络是否能访问 `https://S3图床网址/`，并确认 Cookie 有效。

---

## 开源许可

本项目采用 [MIT License](LICENSE) 开源。

你可以自由使用、修改和分发本脚本，但需保留原始版权声明和许可声明。

---

## 贡献

欢迎提交 Issue 和 Pull Request。

---

## 致谢

- [Typora](https://typora.io/) 提供优秀的 Markdown 编辑体验
