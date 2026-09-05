from flask import Flask, request
import requests

app = Flask(__name__)

# 카카오 디벨로퍼스에서 발급받은 정보 입력
REST_API_KEY = "52a818f0d25965b7e96a959adcbe57a0"
CLIENT_SECRET = "xUBMdgzDOoL85JcnY0fB8RlGPbavAsGf"  # 보안 설정 안 썼으면 빈값 "" 가능
REDIRECT_URI = "https://ubiquitous-space-fishstick-gx7rvg9g64x43vvgq-4000.app.github.dev/redirect"  # 설정한 Redirect URI 주소

@app.route("/redirect")
def redirect():
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        return f"<h1>카카오 로그인 실패</h1><p>{error}</p>"

    if not code:
        return "<h1>인가코드가 없습니다.</h1>"

    # 1. 인가코드를 카카오 Access Token / Refresh Token으로 교환
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "client_secret": CLIENT_SECRET
    }
    
    response = requests.post(token_url, data=data)

    if response.ok:
        token = response.json()
        access_token = token.get("access_token")
        refresh_token = token.get("refresh_token")

        # 2. 발급받은 Access Token으로 사용자 정보 조회
        user_response = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        if user_response.ok:
            user = user_response.json()
            user_id = user.get("id")
            
            # 터미널 창에 발급받은 토큰을 출력하여 확인 용도로 사용
            print(f"[성공] Access Token: {access_token}")
            print(f"[성공] Refresh Token: {refresh_token}")

            return f"""
            <h1>카카오 로그인 성공!</h1>
            <p><strong>사용자 ID:</strong> {user_id}</p>
            <p><strong>Access Token:</strong> {access_token}</p>
            <p><strong>Refresh Token:</strong> {refresh_token}</p>
            """

        return f"<h1>사용자 정보 조회 실패</h1><p>{user_response.text}</p>"

    return f"<h1>토큰 발급 실패</h1><p>{response.text}</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)

