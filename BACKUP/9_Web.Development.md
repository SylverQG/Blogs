# [Web Development](https://github.com/SylverQG/Blogs/issues/9)


# 和风天气API使用指南
[和风天气API](https://dev.qweather.com/)

`由腾讯元宝辅助生成`



基于代码分析，和风天气API目前主要使用JWT认证方式，以下是详细使用说明：

## 一、认证方式
和风天气API采用JWT (JSON Web Token) 认证，替代了传统的API Key方式：

1. **密钥生成**：
   - 需要生成Ed25519密钥对（公钥和私钥）
   - 私钥用于签名JWT，公钥需上传到和风天气控制台

    ```bash
    openssl genpkey -algorithm ED25519 -out ed25519-private.pem \
    && openssl pkey -pubout -in ed25519-private.pem > ed25519-public.pem
    ```


2. **JWT生成**：
   ```python
   import jwt
   import time
   from cryptography.hazmat.primitives.serialization import load_pem_private_key
   
   def get_jwt():
       # 加载私钥
       with open('ed25519-private.pem', 'rb') as f:
           private_key = load_pem_private_key(f.read(), password=None)
       
       # 设置payload
       payload = {
           'iat': int(time.time()) - 30,  # 签发时间（提前30秒避免时间误差）
           'exp': int(time.time()) + 900,  # 过期时间（15分钟）
           'sub': PROJECT_ID  # 项目ID
       }
       
       # 设置headers
       headers = {'kid': KEY_ID}  # 密钥ID
       
       # 生成JWT
       encoded_jwt = jwt.encode(payload, private_key, algorithm='EdDSA', headers=headers)
       return encoded_jwt
   ```

3. **使用方式**：
   - 在HTTP请求头中添加：`Authorization: Bearer {JWT令牌}`

## 二、API基本结构

1. **基础URL**：
   ```
   https://{API_HOST}/{version}/{endpoint}
   ```
   - API_HOST: 和风天气分配的专属域名（如`abcd.as.qweatherapi.com`）
   - version: API版本（如`v7`）
   - endpoint: 具体接口（如`weather/now`）

2. **请求方法**：
   - 主要使用GET请求

3. **请求参数**：
   - 通过URL查询字符串传递
   - 必需参数：location（城市ID或经纬度）
   - 可选参数：lang（语言）、number（结果数量）等

## 三、常用接口

1. **城市查询接口**：
   ```python
   def get_city_code(city, jwt_token):
       url = f"https://{API_HOST}/geo/v2/city/lookup?location={city}&number=1&lang=zh"
       headers = {'Authorization': f'Bearer {jwt_token}'}
       r = requests.get(url, headers=headers)
       data = r.json()
       if data.get("code") == "200" and data.get("location"):
           return data["location"][0]["id"]  # 返回城市ID
       return None
   ```

2. **天气查询接口**：
   ```python
   def get_weather(city_id, jwt_token):
       url = f"https://{API_HOST}/v7/weather/now?location={city_id}&lang=zh"
       headers = {'Authorization': f'Bearer {jwt_token}'}
       r = requests.get(url, headers=headers)
       data = r.json()
       if data.get("code") == "200" and data.get("now"):
           return data["now"]  # 返回天气数据
       return None
   ```

## 四、响应处理

API返回JSON格式数据，包含以下主要字段：
- `code`: 响应状态码（200表示成功）
- `location`: 位置信息（城市查询接口返回）
- `now`: 实时天气数据（天气查询接口返回）

天气数据字段说明：
- `temp`: 温度
- `text`: 天气状况
- `windDir`: 风向
- `windScale`: 风力
- `humidity`: 湿度
- `icon`: 天气图标代码

## 五、完整示例流程

1. 生成JWT令牌
2. 使用城市名称获取城市ID
3. 使用城市ID获取天气信息
4. 解析并展示天气数据

```python
# 完整流程示例
jwt_token = get_jwt()
city = "西安"
city_id = get_city_code(city, jwt_token)
weather = get_weather(city_id, jwt_token)

if weather:
    print(f"{city}的天气信息:")
    print(f"温度: {weather.get('temp', '未知')}°C")
    print(f"天气: {weather.get('text', '未知')}")
    print(f"风向: {weather.get('windDir', '未知')}")
    print(f"风力: {weather.get('windScale', '未知')}级")
    print(f"湿度: {weather.get('humidity', '未知')}%")
```

## 六、注意事项

1. JWT令牌有效期为15分钟，过期后需重新生成
2. 确保私钥安全存储，不要泄露
3. 公钥需上传到和风天气控制台
4. 城市查询接口返回的城市ID是获取天气的关键
5. 遇到错误时，检查API_HOST、PROJECT_ID和KEY_ID是否正确
6. 使用`requests`库时，添加异常处理确保程序稳定性

## 七、图

<img width="373" height="198" alt="Image" src="https://github.com/user-attachments/assets/f047b8ae-7e31-4b16-93b0-2a8ed05cc2a0" />

## 八、代码
### `weather_widget.py`
```python
import jwt
import requests
import os
import time

from flask import Flask, jsonify, request
from flask_cors import CORS 

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
CORS(app) # CORS 跨域请求支持
# 配置信息
API_HOST = "" # https://console.qweather.com/setting?lang=zh
PROJECT_ID = "" # 项目ID
KEY_ID = "" # 凭据ID
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), 'ed25519-private.pem')

def get_jwt():
    """生成JWT令牌"""
    with open(PRIVATE_KEY_PATH, 'rb') as f:
        private_key = load_pem_private_key(f.read(), password=None, backend=default_backend())

    payload = {
        'iat': int(time.time()) - 30,
        'exp': int(time.time()) + 900,
        'sub': PROJECT_ID
    }
    headers = {'kid': KEY_ID}
    
    return jwt.encode(payload, private_key, algorithm='EdDSA', headers=headers)

def get_city_code(city, jwt_token):
    """获取城市代码"""
    url = f"https://{API_HOST}/geo/v2/city/lookup?location={city}&number=1&lang=zh"
    headers = {'Authorization': f'Bearer {jwt_token}'}
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        if data.get("code") == "200" and data.get("location"):
            return data["location"][0]["id"]
    except Exception as e:
        app.logger.error(f"获取城市代码失败: {e}")
    return None

def get_weather(city_id, jwt_token):
    """获取天气信息"""
    url = f"https://{API_HOST}/v7/weather/now?location={city_id}&lang=zh"
    headers = {'Authorization': f'Bearer {jwt_token}'}
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        if data.get("code") == "200" and data.get("now"):
            return data["now"]
    except Exception as e:
        app.logger.error(f"获取天气失败: {e}")
    return None

@app.route('/weather', methods=['GET'])
def weather():
    """天气API端点"""
    city = request.args.get('city', '北京')
    
    jwt_token = get_jwt()
    if not jwt_token:
        return jsonify({"error": "JWT生成失败"}), 500
    
    city_id = get_city_code(city, jwt_token)
    if not city_id:
        return jsonify({"error": f"找不到城市: {city}"}), 404
    
    weather_data = get_weather(city_id, jwt_token)
    if not weather_data:
        return jsonify({"error": "天气数据获取失败"}), 500
    
    return jsonify({
        "city": city,
        "temperature": weather_data.get('temp', 'N/A'),
        "condition": weather_data.get('text', 'N/A'),
        "windDir": weather_data.get('windDir', 'N/A'),
        "windScale": weather_data.get('windScale', 'N/A'),
        "humidity": weather_data.get('humidity', 'N/A'),
        "icon": weather_data.get('icon', '100')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### `weather.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>天气小组件</title>
    <style>
        .weather-widget { font-family: Arial, sans-serif; background: rgba(255,255,255,0.9); padding: 16px; border-radius: 24px; font-size: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 280px; margin: 20px auto; }
        .weather-form { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
        .weather-form input { padding: 8px 12px; border: 1px solid #e0e0e0; border-radius: 16px; flex-grow: 1; }
        .weather-form button { padding: 8px 16px; background: #4285f4; color: white; border: none; border-radius: 16px; cursor: pointer; }
        .weather-info { display: flex; align-items: center; gap: 12px; }
        .weather-icon { font-size: 32px; min-width: 40px; text-align: center; }
        .weather-details { line-height: 1.5; }
        .temperature { font-size: 24px; font-weight: bold; }
        .condition { font-size: 16px; }
        .wind-humidity { font-size: 12px; color: #666; }
    </style>
    <link href="https://cdn.jsdelivr.net/npm/qweather-icons@1.7.0/font/qweather-icons.css" rel="stylesheet">
</head>
<body>
    <div class="weather-widget">
        <div class="weather-form">
            <input type="text" id="city-input" placeholder="输入城市名" value="西安">
            <button id="get-weather">查询</button>
        </div>
        <div class="weather-info" id="weather-container">
            <div class="weather-icon"><i class="qi-999" id="weather-icon"></i></div>
            <div class="weather-details">
                <div class="temperature" id="temperature">--°C</div>
                <div class="condition" id="condition">加载中...</div>
                <div class="wind-humidity">
                    <span id="wind">风向: --</span> | <span id="humidity">湿度: --%</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('get-weather').addEventListener('click', fetchWeather);
        window.addEventListener('DOMContentLoaded', fetchWeather);
        
        async function fetchWeather() {
            const city = document.getElementById('city-input').value;
            const container = document.getElementById('weather-container');
            const originalHTML = container.innerHTML;
            
            container.innerHTML = '<div style="text-align:center;padding:10px">加载中...</div>';
            
            try {
                const response = await fetch(`http://127.0.0.1:5000/weather?city=${encodeURIComponent(city)}`);
                const text = await response.text();
                const data = JSON.parse(text);
                
                if (data.error) {
                    container.innerHTML = `<div style="color:red;text-align:center">${data.error}</div>`;
                    return;
                }
                
                if (!data.temperature || !data.condition || !data.windDir || !data.windScale || !data.humidity || !data.icon) {
                    container.innerHTML = '<div style="color:red;text-align:center">数据不完整: 缺少必要字段</div>';
                    return;
                }
                
                container.innerHTML = originalHTML;
                document.getElementById('weather-icon').className = `qi-${data.icon}`;
                document.getElementById('temperature').textContent = `${data.temperature}°C`;
                document.getElementById('condition').textContent = data.condition;
                document.getElementById('wind').textContent = `风向: ${data.windDir} ${data.windScale}级`;
                document.getElementById('humidity').textContent = `湿度: ${data.humidity}%`;
                
            } catch (error) {
                console.error('请求错误:', error);
                container.innerHTML = `<div style="color:red;text-align:center">${error.name === 'SyntaxError' ? '数据格式错误' : '网络请求失败'}: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>
```


---

# Django Channels 基础配置

1. 安装
```bash
pip install channels
```

2. 配置

- 注册`Channels`：`settings.py`

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'wsapp', # 添加 your app
]
```
- 在`settings.py`中添加 `asgi_application`

```python
ASGI_APPLICATION = 'mysite.asgi.application'
```

- 修改`asgi.py`
> 在项目的settings.py同级目录下的asgi.py文件中加入下面的内容：Django2.2是默认没有asgi.py文件，手动创建一个即可。Django3之后，项目默认会生成一个asgi.py文件。

```python
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        routing.websocket_urlpatterns,
    ]),
})
```

- 在`settigs.py` 同级目录下创建`routing.py`

```python

from django.urls import re_path

from wsapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
```

- 在`wsapp`目录下创建`consumers.py`，编写处理websocket的逻辑

```python
from channels.generic.websocket import WebsocketConsumer   
from channels.exceptions import StopConsumer

class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 有客户端向服务端发送websocket请求时，会调用此方法
        # 客户端允许和服务端建立websocket连接
        self.accept()

    def websocket_receive(self, message):
        # 浏览器基于websocket协议，向服务端发送数据时，会调用此方法
        print(message) 
        self.send("不要回复")
        # self.close() 服务端可以主动断掉某个客户端的连接

    def websocket_disconnect(self, message):
        # 客户端断开连接时，会调用此方法
        print("断开连接")
        raise StopConsumer()
```

---

<html><head></head><body>
<h1>Python Web 服务器（Gunicorn、Uvicorn、Daphne）对比解析</h1>
<p>腾讯元宝生成</p>
<p>以下是针对 Gunicorn、Uvicorn 和 Daphne 三类 Python Web 服务器的深度对比解析，综合其核心特性、适用场景及性能表现：</p>
<hr>
<h3>🔧 ​<strong>​1. 协议与架构设计​</strong>​</h3>
<ul class="ybc-ul-component">
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Gunicorn​</strong>​<br>
基于 ​<strong>​WSGI 协议​</strong>​（同步模型），采用​<strong>​预分叉多进程架构​</strong>​（Pre-fork）。每个 Worker 进程独立处理请求，依赖进程数提升并发，适合 CPU 密集型任务。</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Uvicorn​</strong>​<br>
基于 ​<strong>​ASGI 协议​</strong>​（异步模型），核心依赖 ​<strong>​uvloop 事件循环​</strong>​（libuv 的 Python 封装）和 ​<strong>​httptools 解析库​</strong>​，单进程即可高效处理高并发 I/O 操作（如 WebSocket、HTTP长连接）。</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Daphne​</strong>​<br>
同样基于 ​<strong>​ASGI 协议​</strong>​，由 ​<strong>​Django Channels 团队开发​</strong>​，专注支持 HTTP/WebSocket/HTTP2 多协议，内置异步事件循环，适合实时通信场景。</span></li>
</ul>
<hr>
<h3>⚙️ ​<strong>​2. 适用框架与典型场景​</strong>​</h3>
<div class="hyc-common-markdown__table-wrapper" data-has-scroll="false" style="font-size: 14px; color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); border-collapse: separate; border-spacing: 0px; padding: 0px;">
  <table class="hyc-table">
      <thead>
          <tr>
              <th>服务器</th>
              <th>兼容框架</th>
              <th>最佳场景</th>
          </tr>
      </thead>
      <tbody>
          <tr class="gunicorn-row">
              <td>Gunicorn</td>
              <td>Django, Flask, Pyramid</td>
              <td>传统同步应用（CMS、电商后台）</td>
          </tr>
          <tr class="uvicorn-row">
              <td>Uvicorn</td>
              <td>FastAPI, Starlette, Sanic</td>
              <td>异步 API 服务、低延迟实时交互</td>
          </tr>
          <tr class="daphne-row">
              <td>Daphne</td>
              <td>Django Channels, Quart</td>
              <td>WebSocket 实时应用（聊天、推送系统）</td>
          </tr>
      </tbody>
  </table>
</div>

<div class="hyc-common-markdown__table-wrapper" data-has-scroll="false" style="font-size: 14px; color: rgb(0, 0, 0); background-color: rgba(0, 0, 0, 0); border-collapse: separate; border-spacing: 0px; padding: 0px;">
<h3>📊<strong>3. 性能关键指标对比</strong></h3>
  <table class="hyc-table">
      <thead>
          <tr>
              <th>特性</th>
              <th>Gunicorn</th>
              <th>Uvicorn</th>
              <th>Daphne</th>
          </tr>
      </thead>
      <tbody>
          <tr>
              <td>并发模型</td>
              <td>多进程</td>
              <td>单进程异步协程</td>
              <td>单进程异步事件循环</td>
          </tr>
          <tr>
              <td>WebSocket 支持</td>
              <td>❌（需插件）</td>
              <td>✅ 原生</td>
              <td>✅ 原生</td>
          </tr>
          <tr>
              <td>HTTP/2 支持</td>
              <td>❌</td>
              <td>✅</td>
              <td>✅</td>
          </tr>
          <tr>
              <td>请求吞吐量</td>
              <td class="comparison-medium">中（依赖进程数）</td>
              <td class="comparison-high">高（≈10k+/秒）</td>
              <td class="comparison-high">高（≈7k+/秒）</td>
          </tr>
          <tr>
              <td>内存占用</td>
              <td class="comparison-low">高（多进程复制）</td>
              <td class="comparison-high">低</td>
              <td class="comparison-medium">中</td>
          </tr>
      </tbody>
  </table>
</div>
<p>💡 ​<strong>​性能测试参考​</strong>​：在 1000 并发连接下，Uvicorn 处理能力可达 Gunicorn 的 3 倍以上。</p>
</blockquote>
<hr>
<h3>🛠️ ​<strong>​4. 部署实践建议​</strong>​</h3>
<ul class="ybc-ul-component">
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Gunicorn​</strong>​
<ul class="ybc-ul-component">
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">生产环境需搭配 ​<strong>​Nginx​</strong>​ 反向代理（静态文件处理、负载均衡）。</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">启动命令示例：
<pre class="ybc-pre-component ybc-pre-component_not-math"><code>gunicorn -w 4 -b 0.0.0.0:8000 app:app</code></pre>
</span></li>
</ul>
</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Uvicorn​</strong>​
<ul class="ybc-ul-component">
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">开发期用单进程 + <code>--reload</code> 调试。</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">生产环境推荐 ​<strong>​Gunicorn + Uvicorn Worker​</strong>​ 组合（兼顾进程管理与异步性能）：
<pre class="ybc-pre-component ybc-pre-component_not-math"><code>gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app</code></pre>
</span></li>
</ul>
</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Daphne​</strong>​
<ul class="ybc-ul-component">
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">直接作为独立服务器运行，尤其适合 Django Channels 项目：
<pre class="ybc-pre-component ybc-pre-component_not-math"><code>daphne -b 0.0.0.0 -p 8000 project.asgi:application</code></pre>
</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">需通过 ​<strong>​Nginx 配置​</strong>​ WebSocket 代理（<code>Upgrade</code>头处理）。</span></li>
</ul>
</span></li>
</ul>
<hr>
<h3>⚖️ ​<strong>​5. 选型决策树​</strong>​</h3>
<ol class="ybc-ol-component ybc-ol-component_1">
<li class="ybc-li-component ybc-li-component_ol"><span class="ybc-li-component_content">​<strong>​同步框架（Django/Flask） + 高稳定性需求​</strong>​ → ​<strong>​Gunicorn​</strong>​。</span></li>
<li class="ybc-li-component ybc-li-component_ol"><span class="ybc-li-component_content">​<strong>​异步框架（FastAPI/Starlette） + 高并发/低延迟​</strong>​ → ​<strong>​Uvicorn 单机​</strong>​ 或 ​<strong>​Gunicorn+Uvicorn Worker​</strong>​。</span></li>
<li class="ybc-li-component ybc-li-component_ol"><span class="ybc-li-component_content">​<strong>​实时双向通信（WebSocket/HTTP2） + Django 生态​</strong>​ → ​<strong>​Daphne​</strong>​。</span></li>
<li class="ybc-li-component ybc-li-component_ol"><span class="ybc-li-component_content">​<strong>​资源受限场景（如小型 VPS）​</strong>​ → ​<strong>​Uvicorn​</strong>​（内存占用更低）。</span></li>
</ol>
<hr>
<h3>💎 ​<strong>​总结​</strong>​</h3>
<ul class="ybc-ul-component">
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Gunicorn​</strong>​：​<strong>​稳​</strong>​，为传统同步应用提供工业级可靠性。</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Uvicorn​</strong>​：​<strong>​快​</strong>​，异步高性能的首选，开发体验优。</span></li>
<li class="ybc-li-component ybc-li-component_ul"><span class="ybc-li-component_content">​<strong>​Daphne​</strong>​：​<strong>​专​</strong>​，解决 Django 生态实时通信的痛点。</span></li>
</ul>
<blockquote>
<p>⚠️ 注：三者均可与 ​<strong>​Nginx​</strong>​ 反向代理协作提升安全性，生产环境务必禁用调试模式（如 Uvicorn 的 <code>--reload</code>）。</p>
</blockquote></body></html>