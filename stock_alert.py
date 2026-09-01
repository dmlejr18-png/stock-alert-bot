import os
import json
import requests

token = os.getenv("KAKAO_ACCESS_TOKEN")

if not token:
    raise Exception("KAKAO_ACCESS_TOKEN이 없습니다.")

template = {
    "object_type": "text",
    "text": "📊 주식알림봇 테스트\n\n🔵 [스윙] 자동 브리핑 테스트\n🔴 [단타] 자동 브리핑 테스트\n\n카카오톡 발송 테스트 성공!",
    "link": {
        "web_url": "https://github.com",
        "mobile_web_url": "https://github.com"
    }
}

response = requests.post(
    "https://kapi.kakao.com/v2/api/talk/memo/default/send",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    },
    data={
        "template_object": json.dumps(template)
    }
)

print("카카오 응답:", response.status_code, response.text)

if response.status_code != 200:
    raise Exception("카카오 메시지 전송 실패")

result = response.json()

if result.get("result_code") != 0:
    raise Exception(f"카카오 메시지 전송 실패: {result}")

print("✅ 카카오톡 발송 성공")
