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


def new_prompt(title, content, category):
    """프롬프트 딕셔너리를 만든다. 즐겨찾기는 기본 해제, 조회수는 0이다."""
    return {
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
    }


def choose_category():
    """미리 정의된 카테고리 중 하나를 고르거나 직접 입력받는다."""
    custom_number = len(CATEGORIES) + 1
    while True:
        print("카테고리 선택:")
        for number, category in enumerate(CATEGORIES, start=1):
            print(f"{number}) {category}")
        print(f"{custom_number}) 직접 입력")

        number = input_number("선택: ", 1, custom_number)
        if number is None:
            continue
        if number == custom_number:
            return input_non_empty("카테고리 이름: ")
        return CATEGORIES[number - 1]


def title_exists(prompts, title, ignore=None):
    """같은 제목(대소문자 무시)이 이미 있으면 True. ignore는 검사에서 제외할 프롬프트."""
    return any(
        p is not ignore and p["title"].lower() == title.lower() for p in prompts
    )


def input_unique_title(prompts, ignore=None):
    """중복되지 않는 제목을 입력받는다. 중복이면 다시 입력받는다."""
    while True:
        title = input_non_empty("제목: ")
        if not title_exists(prompts, title, ignore):
            return title
        print("이미 같은 제목의 프롬프트가 있습니다. 다른 제목을 입력해주세요.")


def add_prompt(prompts):
    """새 프롬프트를 입력받아 목록에 추가한다."""
    print("\n=== 프롬프트 추가 ===")
    title = input_unique_title(prompts)
    content = input_non_empty("내용: ")
    print()
    category = choose_category()

    prompts.append(new_prompt(title, content, category))
    print("\n프롬프트가 추가되었습니다!")


def print_prompt_line(number, prompt):
    """'번호. [카테고리] 제목 ⭐' 형식으로 한 줄 출력한다."""
    star = " ⭐" if prompt["favorite"] else ""
    print(f"{number}. [{prompt['category']}] {prompt['title']}{star}")


def show_list(prompts):
    """저장된 모든 프롬프트를 번호와 함께 출력한다."""
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다. 먼저 프롬프트를 추가해주세요.")
        return

    for number, prompt in enumerate(prompts, start=1):
        print_prompt_line(number, prompt)
    print(f"\n총 {len(prompts)}개의 프롬프트")


def find_prompts(prompts, condition):
    """condition(prompt)가 참인 프롬프트를 (전체 목록 기준 번호, 프롬프트) 목록으로 반환한다.

    전체 목록 기준 번호를 유지해서, 결과에 보이는 번호를
    상세 보기/즐겨찾기 관리에 그대로 입력할 수 있게 한다.
    """
    return [
        (number, prompt)
        for number, prompt in enumerate(prompts, start=1)
        if condition(prompt)
    ]


def print_matches(matches):
    """find_prompts()의 결과를 출력한다."""
    for number, prompt in matches:
        print_prompt_line(number, prompt)


def get_all_categories(prompts):
    """기본 카테고리에 사용자가 직접 입력한 카테고리를 더한 목록을 반환한다."""
    categories = list(CATEGORIES)
    for prompt in prompts:
        if prompt["category"] not in categories:
            categories.append(prompt["category"])
    return categories


def show_by_category(prompts):
    """선택한 카테고리의 프롬프트만 출력한다."""
    print("\n=== 카테고리별 조회 ===")
    categories = get_all_categories(prompts)
    for number, category in enumerate(categories, start=1):
        print(f"{number}) {category}")

    number = input_number("선택: ", 1, len(categories))
    if number is None:
        return
    category = categories[number - 1]

    matches = find_prompts(prompts, lambda prompt: prompt["category"] == category)
    print(f"\n[{category}] 카테고리 프롬프트:")
    if not matches:
        print("이 카테고리에 등록된 프롬프트가 없습니다.")
        return
    print_matches(matches)
    print(f"\n총 {len(matches)}개의 프롬프트")


def search_prompt(prompts):
    """키워드가 제목 또는 내용에 포함된 프롬프트를 찾는다 (대소문자 무시)."""
    print("\n=== 프롬프트 검색 ===")
    keyword = input_non_empty("검색어: ").lower()

    matches = find_prompts(
        prompts,
        lambda prompt: keyword in prompt["title"].lower()
        or keyword in prompt["content"].lower(),
    )
    print("\n검색 결과:")
    if not matches:
        print("검색 결과가 없습니다.")
        return
    print_matches(matches)
    print(f"\n{len(matches)}개의 프롬프트를 찾았습니다.")


def select_prompt(prompts):
    """번호를 입력받아 해당 프롬프트를 반환한다. 잘못된 번호면 None."""
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return None
    number = input_number(f"번호 입력 (1~{len(prompts)}): ", 1, len(prompts))
    if number is None:
        return None
    return prompts[number - 1]


def show_detail(prompts):
    """선택한 프롬프트의 전체 내용을 출력하고 조회수를 1 올린다."""
    print("\n=== 프롬프트 상세 보기 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    prompt["views"] = prompt.get("views", 0) + 1
    line = "─" * 40
    print()
    print(line)
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '-'}")
    print(f"조회수: {prompt['views']}")
    print(line)
    print("내용:")
    print(prompt["content"])
    print(line)


def toggle_favorite(prompts):
    """선택한 프롬프트의 즐겨찾기 상태를 추가/해제한다."""
    print("\n=== 즐겨찾기 관리 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    prompt["favorite"] = not prompt["favorite"]
    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다! ⭐")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다.")


def show_favorites(prompts):
    """즐겨찾기된 프롬프트만 모아서 출력한다."""
    print("\n=== 즐겨찾기 목록 ===")
    matches = find_prompts(prompts, lambda prompt: prompt["favorite"])
    if not matches:
        print("즐겨찾기한 프롬프트가 없습니다. (즐겨찾기 관리 메뉴에서 추가할 수 있습니다)")
        return
    print_matches(matches)
    print(f"\n총 {len(matches)}개의 즐겨찾기")


MENU_ITEMS = [
    ("1", "프롬프트 추가", add_prompt),
    ("2", "프롬프트 목록", show_list),
    ("3", "카테고리별 조회", show_by_category),
    ("4", "프롬프트 검색", search_prompt),
    ("5", "프롬프트 상세 보기", show_detail),
    ("6", "즐겨찾기 관리", toggle_favorite),
    ("7", "즐겨찾기 목록", show_favorites),
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
