from flask import Flask, request
import requests

app = Flask(name)

주석 없음
REST_API_KEY = "52a818f0d25965b7e96a959adcbe57a0"
REDIRECT_URI = "https://jubilant-potato-j45g997jx5vfj5xj-4000.app.github.dev/redirect"

@app.route("/redirect")
def redirect():
code = request.args.get("code")
if not code:
return "<h1>인가 코드가 없습니다.</h1>", 400

url = "https://kauth.kakao.com/oauth/token"
data = {
"grant_type": "authorization_code",
"client_id": REST_API_KEY,
"redirect_uri": REDIRECT_URI,
"code": code
}

response = requests.post(url, data=data)
result = response.json()

if "access_token" in result:
return f"<h1>토큰 발급 성공!</h1><p>Access Token: {result['access_token']}</p>"
else:
return f"<h1>토큰 발급 실패</h1><p>{result}</p>"

if name == "main":
app.run(host="0.0.0.0", port=4000)






