from flask import Flask
from flask_cors import CORS
from app.routes import main  # 导入 Blueprint
from app.musicSdk.routes import music

app = Flask(__name__)
CORS(app)  # 开启全局 CORS
app.config.from_object('config.Config')  # 加载配置

app.register_blueprint(main)
app.register_blueprint(music)  # 注册 Blueprint

@app.route('/geturl')
def getURL():
    paths = []
    for rule in app.url_map.iter_rules():
        # rule.endpoint 以 Blueprint 名开头的就是 Blueprint 路由
        paths.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "rule": str(rule)
        })
        print(f"{rule.endpoint}: {rule.methods} -> {rule}")
    return {"routes": paths}

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "127.0.0.1"),
        port=app.config.get("PORT", 5000),
        debug=app.config.get("DEBUG", True)
    )

# flask run -h "0.0.0.0" -p 80 --debug