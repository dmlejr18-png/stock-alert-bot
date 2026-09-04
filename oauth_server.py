from flask import Flask, request

app = Flask(__name__)

@app.route("/redirect")
def redirect():
    code = request.args.get("code")
    error = request.args.get("error")

    if code:
        return f"<h1>인가코드 받기 성공</h1><p>code가 도착했습니다.</p>"

    return f"<h1>카카오 로그인 실패</h1><p>{error}</p>"

app.run(host="0.0.0.0", port=4000)
