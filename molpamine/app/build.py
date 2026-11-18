"""몰파민 원고를 생성기의 시작 데이터로 넣어 ebook-generator.html을 만든다.

사용법: python3 molpamine/app/build.py
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "app"
MS = ROOT / "03_원고"


def chapter(fname):
    text = (MS / fname).read_text(encoding="utf-8")
    text = re.sub(r"^> 상태:.*\n+", "", text.split("\n", 1)[1].lstrip("\n"))
    title = (MS / fname).read_text(encoding="utf-8").split("\n", 1)[0].lstrip("# ").strip()
    body = text.lstrip("-\n")
    return title, f"# {title}\n\n{body.strip()}\n"


def done(fname, questions, memo, card, goal):
    title, draft = chapter(fname)
    return dict(title=title, card=card, goal=goal, questions=questions, memo=memo, draft=draft, done=True)


toc = [
    done("00_프롤로그.md",
         ["중요한 일을 앞두면 어떻게 되나요?", "그때 대신 하고 싶어지는 건?", "그때 나에게 했던 생각은?"],
         ["중요한 할 일을 공부하려면 하기가 싫어진다 / 쇼핑 앱",
          "오히려 다른 걸 하고 싶어진다",
          "나는 왜 이럴까? 처음엔 ADHD인 줄 알았다. 검사는 세 곳에서 받아 봤다. 한 곳은 맞다, 두 곳은 아니다"],
         "겪은 약점", "집중 못 하는 게 내 탓이 아니라는 걸 알게 된다"),
    done("01_1장_브레인포그의_정체.md",
         ["머리가 가장 뿌옇다고 느낀 순간은?", "그때 몸이나 머리는 어떤 느낌이었나요?", "그때 자신에게 했던 말 한 문장은?"],
         ["공부하려고 책 펴면 글자가 안 들어온다", "머리는 답답이라고 해야 하나", "난 왜 중요한 순간마다 이럴까"],
         "재밌게 할 수 있는 분야", "글자가 안 들어오는 진짜 이유를 안다"),
    done("02_2장_도파민은_죄가_없다.md",
         ["쇼핑 앱을 열기 직전 기분은?", "앱을 보는 동안 기분은?", "앱을 닫고 난 뒤 기분은?"],
         ["할 일이 막막하고 불안했다", "잠깐 편했다", "후회됐다"],
         "재밌게 할 수 있는 분야", "빠른 도파민과 느린 도파민을 구분한다"),
    done("03_3장_몰파민이란_무엇인가.md",
         ["시간 가는 줄 모르고 빠져든 일은?", "그 일은 쉬웠나요, 적당히 어려웠나요?", "끝나고 나서 기분은?"],
         ["게임", "적당히 어려웠다", "이기면 기분 좋고 지면 짜증나고, 시간 지난 걸 보면 현타 온다"],
         "알고 싶었던 것: 몰입", "몰입이 일어나는 조건을 내 일에 옮긴다"),
    done("04_4장_감정기복은_뇌의_날씨다.md",
         ["최근 감정이 크게 흔들린 순간은?", "그때 몸이나 행동은?", "그 기분이 얼마나 갔고 할 일에 어떤 영향을 줬나요?"],
         ["사소한 일에도 감정적이 된다", "아무 말도 하기 싫고, 핸드폰을 보거나 핸드폰도 잘 안 보고 만사 귀찮고 무기력하다",
          "미루는 습관이 생기기 시작했고 행동을 잘 하지 않게 됐다"],
         "지금 힘든 것", "무기력한 날에도 할 수 있는 한 가지를 안다"),
    dict(title="5장 – 상처도 뇌의 해석이다: 내 해석을 다시 쓰는 법", card="이제는 아닌 상처",
         goal="지나간 상처를 다르게 해석하는 연습을 한다",
         questions=["예전에 나를 가장 아프게 했던 말이나 일은?",
                    "그때 나는 그 일을 보고 '나는 ___한 사람이다'라고 생각했나요?",
                    "지금은 그 일을 어떻게 다르게 보나요?"],
         memo=["", "", ""], draft="", done=False),
    dict(title="6장 – 몰파민 루틴 7일: 하루 1시간 몰입 만들기", card="실천",
         goal="7일 동안 따라 할 수 있는 루틴을 얻는다",
         questions=["7일 동안 매일 한 행동과 기분 전/후는?", "가장 효과가 있었던 행동은?", "7일 뒤 달라진 점은?"],
         memo=["1일차: 창문 열기, 세수 → 기분이 확실히 전보다 좋아짐", "", ""], draft="", done=False),
    dict(title="에필로그 – 이제는 아닌 상처", card="전체",
         goal="책을 덮고도 남는 한 문장을 얻는다",
         questions=["이 책을 쓰기 전과 후, 나는 무엇이 달라졌나요?", "지금 감정기복과 어떻게 지내고 있나요?",
                    "독자에게 꼭 하고 싶은 한 문장은?"],
         memo=["", "", ""], draft="", done=False),
]

plan = (ROOT / "01_기획서.md").read_text(encoding="utf-8")
research = plan.split("## ② 리서치: 쓸 수 있는 근거 / 피할 주장", 1)[1].split("## 진행 체크", 1)[0].strip()

seed = dict(
    v=1, step=3, cur=5, mode="edit",
    cards=dict(know="몰입하는 방법",
               fun="요새 브레인포그, 도파민 중독 등 집중력 저하가 많은데 이것을 뇌과학으로 재밌게 풀어내 보는 것",
               weak="우울증, 지인들의 뒤통수, 마음 약한 약점, 대인기피증, 불안장애 등",
               healed="뇌가 어떻게 해석하느냐에 따라 달린 것",
               hard="감정기복"),
    topic=dict(core="뇌의 해석을 바꿔 흐려진 집중과 흔들리는 감정을 되찾는다",
               promise="이 책을 다 읽은 사람은 폰 도파민 대신 몰파민으로 하루 1시간 깊이 몰입할 수 있게 된다.",
               title="몰파민", subtitle="폰에 빼앗긴 뇌를 몰입으로 되찾는 법",
               reader="퇴근하고 누우면 폰만 보다가 '오늘도 아무것도 못 했다'며 자책하는 20~30대",
               author=""),
    topicDraft=None, research=research, toc=toc,
    cover=dict(bg="#0F3D36", ink="#F3F0E6", accent="#F3D35B", confirmed=False),
    coverIdeas=None, exported=False,
)

blob = json.dumps(seed, ensure_ascii=False).replace("</", "<\\/")
html = (APP / "template.html").read_text(encoding="utf-8").replace("/*SEED*/", blob)
(APP / "ebook-generator.html").write_text(html, encoding="utf-8")
print("wrote", APP / "ebook-generator.html", len(html.encode()), "bytes")
