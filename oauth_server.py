from flask import Flask, request
import requests

app = Flask(__name__)

REST_API_KEY = "52a818f0d25965b7e96a959adcbe57a0"
CLIENT_SECRET = "7z3zDOpoiSGoWm2RXRdL4JGwF9Vlj8OV"
REDIRECT_URI = "https://ubiquitous-space-fishstick-gx7rvg9g64x43vvgq-4000.app.github.dev/redirect"


@app.route("/redirect")
def redirect():
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        return f"<h1>카카오 로그인 실패</h1><p>{error}</p>"

    if not code:
        return "<h1>인가코드가 없습니다.</h1>"

    # 인가코드를 카카오 토큰으로 교환
    response = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": REST_API_KEY,
            "redirect_uri": REDIRECT_URI,
            "code": code,
            "client_secret": CLIENT_SECRET
        }
    )

    if response.ok:
        token = response.json()

        return f"""
        <h1>토큰 발급 성공!</h1>
        <p>Access Token 발급 완료</p>
        <p>Refresh Token 발급 완료</p>
        """

    return f"""
    <h1>토큰 발급 실패</h1>
    <p>{response.text}</p>
    """


app.run(host="0.0.0.0", port=4000)
