#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Typora 自定义上传命令 -> 某S3 图床
修复 Windows 乱码，改用直接填写 Cookie 字符串的方式。
"""

import sys
#import os 似乎没用上，报错了再取消注释
import re
import time
import requests
from pathlib import Path

# ============== 配置区 ==============
HOME_URL   = "https://s3.XXXXclub.net/"
UPLOAD_URL = "https://s3.XXXXclub.net/json"
# 在S3页面使用F12打开开发者模式-F5刷新页面-网络选项卡-第一个指向https://s3.XXXXclub.net/的请求-标头下拉找到cookies选项，复制，包含开头的c_secure_pass
# ★★★ 把你刚才复制的 Cookie 粘贴到下面这两个单引号之间 ★★★
MY_COOKIE  = '在这里粘贴你的Cookie字符串'
# ===================================

# 强制设置标准输出为 utf-8，解决 Windows 乱码
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8') # type: ignore
    sys.stderr.reconfigure(encoding='utf-8') # type: ignore


def get_session():
    """构建带 Cookie 的 requests 会话"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0 Safari/537.36"),
        "Referer": HOME_URL,
        "Cookie": MY_COOKIE,  # 直接将 Cookie 放入请求头
    })
    return session


def fetch_auth_token(session):
    """访问首页，正则提取 auth_token，并校验登录态"""
    resp = session.get(HOME_URL, timeout=20)
    html = resp.text
    m = (re.search(r'PF\.obj\.config\.auth_token\s*=\s*["\']([^"\']+)["\']', html)
         or re.search(r'auth_token["\']?\s*[:=]\s*["\']([a-zA-Z0-9]+)["\']', html))
    if not m:
        return None, "TOKEN_NOT_FOUND"
    token = m.group(1)
    # 登录态校验
    if not ("/logout" in html or "action=logout" in html or "sign-out" in html):
        return None, "GUEST_SESSION"
    return token, "OK"


def upload_image(session, token, file_path):
    """单图上传"""
    try:
        with open(file_path, "rb") as f:
            files = {"source": (Path(file_path).name, f, "application/octet-stream")}
            data = {
                "type": "file",
                "action": "upload",
                "timestamp": str(int(time.time() * 1000)),
                "auth_token": token,
                "nsfw": "0",
            }
            resp = session.post(UPLOAD_URL, files=files, data=data, timeout=60)
    except FileNotFoundError:
        return None, f"找不到文件: {file_path}"

    if resp.status_code != 200:
        return None, f"HTTP_{resp.status_code}: {resp.text[:200]}"
    try:
        res = resp.json()
    except Exception:
        return None, "JSON解析失败"

    if res.get("status_code") == 200 and res.get("image"):
        url = res["image"].get("url") or res["image"].get("display_url")
        return url, "OK"
    
    err = (res.get("error") or {}).get("message", "UNKNOWN")
    return None, f"上传失败: {err}"


def main():
    paths = [p for p in sys.argv[1:] if p.strip()]
    if not paths:
        print("Usage: upload_img.py <image1> [image2] ...", file=sys.stderr)
        sys.exit(1)

    if '在这里粘贴你的Cookie字符串' in MY_COOKIE:
        print("[错误] 请先在脚本中填写 Cookie 字符串！", file=sys.stderr)
        sys.exit(1)

    session = get_session()
    token, status = fetch_auth_token(session)
    if not token:
        print(f"[XXXXUploader] 登录态失效 ({status})，请重新获取 Cookie 填入脚本", file=sys.stderr)
        sys.exit(2)

    results = []
    for p in paths:
        url, err = upload_image(session, token, p)
        if url:
            results.append(url)
        else:
            print(f"[XXXXUploader] 上传失败 {p}: {err}", file=sys.stderr)
            results.append("") 

    print("Upload Success:")
    for u in results:
        print(u)


if __name__ == "__main__":
    main()
