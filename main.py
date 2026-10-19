"""나만의 프롬프트 관리 프로그램 (콘솔)

프롬프트를 분류·검색·즐겨찾기로 관리한다.
"""
import json
import os

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

DEFAULT_PROMPTS = [
    {
        "title": "회의록 요약",
        "content": "다음 회의 내용을 핵심 결정사항과 할 일(담당자 포함) 위주로 5줄 이내로 요약해줘.",
        "category": "텍스트 생성",
        "favorite": True,
    },
    {
        "title": "제품 키비주얼",
        "content": "Minimal product photography of a smart mood light, warm amber tone, 35mm lens, shallow depth of field",
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "카메라 푸시인 영상",
        "content": "Slow push-in camera movement in a cozy living room, soft dust particles, 8 seconds, no camera shake",
        "category": "영상 생성",
        "favorite": False,
    },
    {
        "title": "친절한 코드 리뷰어",
        "content": "너는 10년차 시니어 개발자야. 코드의 문제점을 초보자도 이해하게 존댓말로 설명해줘.",
        "category": "페르소나",
        "favorite": False,
    },
    {
        "title": "메일 자동 분류",
        "content": "받은 이메일 본문을 읽고 '업무/광고/개인' 중 하나로만 분류해서 답해줘.",
        "category": "자동화",
        "favorite": False,
    },
]


def input_non_empty(message):
    """빈 값이 아닐 때까지 반복해서 입력받는다."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("입력값이 비어 있습니다. 다시 입력해주세요.")


def input_number(message, min_value, max_value):
    """min_value~max_value 범위의 정수를 입력받는다. 잘못된 입력이면 None을 반환한다."""
    value = input(message).strip()
    try:
        number = int(value)
    except ValueError:
        print("숫자를 입력해주세요.")
        return None
    if number < min_value or number > max_value:
        print(f"{min_value}~{max_value} 사이의 번호를 입력해주세요.")
        return None
    return number


def show_menu():
    """메인 메뉴를 출력한다."""
    print()
    print("=== 나만의 프롬프트 관리 ===")
    for key, label, _ in MENU_ITEMS:
        print(f"{key}. {label}")
    print("0. 종료")


for _prompt in DEFAULT_PROMPTS:
    _prompt.setdefault("views", 0)


MENU_ITEMS = [
]


def main():
    # 기본 데이터를 복사해서 사용한다 (프로그램 실행 중에만 유지)
    prompts = [dict(prompt) for prompt in DEFAULT_PROMPTS]
    actions = {key: func for key, _, func in MENU_ITEMS}

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        if choice in actions:
            actions[choice](prompts)
        else:
            print("잘못된 입력입니다. 메뉴에 있는 번호를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
