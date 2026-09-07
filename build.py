#!/usr/bin/env python3
"""Собирает index.html из списка проектов.

Карточки рендерятся статикой, а не из JS, чтобы страница читалась
целиком без JavaScript. Обе локали лежат в одном DOM: у текстовых
узлов data-ru / data-en, переключение — в app.js.
"""
import html, pathlib

GH = "https://github.com/JustBelieve9"
PAGES = "https://justbelieve9.github.io"

# ── Шоурил ───────────────────────────────────────────────
# Видео лежат на YouTube (unlisted) — в репозитории только идентификаторы.
# Плеер грузится по клику: до этого на странице лежит превью, а не iframe,
# поэтому YouTube не тянет свои скрипты, пока их никто не попросил.
#
# poster="имя" — свой кадр из img/reel/имя.jpg вместо превью с ytimg.
# ratio — пропорции плитки: "9:16" для вертикальных креативов, "16:9", "1:1".

REEL_ID = "SiLq6lMpyZw"   # id шоурила: youtu.be/XXXXXXXXXXX → "XXXXXXXXXXX"
REEL_RATIO = "9:16"       # шоурил снят вертикалью, как и сами креативы
CHANNEL = "https://www.youtube.com/@zhaba009"

SHOTS = [
    # dict(id="XXXXXXXXXXX", ratio="9:16",
    #      ru="Название проекта", en="Project name",
    #      dru="Что делал я и что здесь технически сложного.",
    #      den="What I did and what is technically hard here."),
]

# cat: blender | macos | web | bots
PROJECTS = [
    dict(
        id="box3d-bake", cat="blender", big=True, img="box3d",
        ru="Box3D Bake", en="Box3D Bake",
        dru="Твёрдые тела считает Box3D через ctypes, а не Bullet: вся симуляция прогоняется заранее и ложится в сцену ключами или кэшем.",
        den="Rigid bodies run on Box3D through ctypes instead of Bullet: the whole sim is computed up front, then written out as keyframes or cache.",
        alt_ru="Раздел Box3D Bake на сайте аддонов: бенчмарк против Bullet",
        alt_en="Box3D Bake section of the addon site: benchmark against Bullet",
        meta="v0.26.0", tags=["Python", "C", "ctypes", "Blender API"],
        links=[("site", f"{PAGES}/box3d-studio-site/#/box3d"),
               ("dl", f"{GH}/box3d-bake-releases/releases/latest")],
    ),
    dict(
        id="creative-studio", cat="blender", img="studio",
        ru="Creative Studio Tools", en="Creative Studio Tools",
        dru="Продакшен видеокреативов под мобильные игры: анимация по пути, направляющие кропов, прокси-текстуры, доктор сцены, сборка проекта.",
        den="Video-creative production for mobile games: path animation, crop guides, proxy textures, a scene doctor and project collect.",
        alt_ru="Раздел Creative Studio Tools на сайте аддонов",
        alt_en="Creative Studio Tools section of the addon site",
        meta="v0.14.0", tags=["Python", "Blender API"],
        links=[("site", f"{PAGES}/box3d-studio-site/#/studio"),
               ("dl", f"{GH}/creative-studio-releases/releases/latest")],
    ),
    dict(
        id="blender-launcher", cat="macos", big=True, img="launcher",
        ru="Blender Launcher", en="Blender Launcher",
        dru="macOS не открывает второй Blender — этот лаунчер открывает. И показывает проекты с автосейвами ещё до запуска.",
        den="macOS refuses to open a second Blender — this launcher does. And it shows your projects and autosaves before Blender even starts.",
        alt_ru="Окно Blender Launcher: слева проекты, справа автосейвы",
        alt_en="Blender Launcher window: projects on the left, autosaves on the right",
        meta="v1.2.0", tags=["Swift", "SwiftUI", "AppKit"],
        links=[("repo", f"{GH}/blender-launcher"),
               ("site", f"{PAGES}/blender-launcher/"),
               ("dl", f"{GH}/blender-launcher/releases/latest")],
    ),
    dict(
        id="gym", cat="web", big=True, img="gym",
        ru="Тренировка", en="Gym",
        dru="Помощник в зале на двоих: программа собрана по метаанализам, отметка подходов, таймер отдыха и звук, который не глохнет в фоне на iOS.",
        den="A gym helper for two: the program is built from meta-analyses, with set tracking, a rest timer and audio that survives iOS backgrounding.",
        alt_ru="Приложение «Тренировка»: список упражнений и таймер отдыха",
        alt_en="The Gym app: exercise list and rest timer",
        tags=["JavaScript", "CSS", "localStorage"],
        links=[("demo", f"{PAGES}/gym/"), ("repo", f"{GH}/gym"),
               ("case", f"{PAGES}/gym-case/")],
    ),
    dict(
        id="golf", cat="web", img="golf",
        ru="Golf 7.5 CZCA", en="Golf 7.5 CZCA",
        dru="Справочник по одной конкретной машине: 253 узла, 318 связей, 192 PR-кода. Плюс офлайн-версия одним файлом, без единого запроса в сеть.",
        den="A reference for one specific car: 253 nodes, 318 links, 192 PR codes. Plus a single-file offline build that makes zero network requests.",
        alt_ru="Справочник Golf 7.5: обзор машины и разделы",
        alt_en="Golf 7.5 reference: car overview and sections",
        tags=["Python", "HTML", "Graph"],
        links=[("demo", f"{PAGES}/golfik_map/"), ("repo", f"{GH}/golfik_map")],
    ),
    dict(
        id="balhash", cat="web", img="balhash",
        ru="Балхаш 2026", en="Balkhash 2026",
        dru="Архив поездки: смонтированный фильм двумя частями, фотографии сериями и исходные клипы. Статический экспорт, живёт на Pages.",
        den="A trip archive: the edited film in two parts, photos in series and the raw clips. Static export, hosted on Pages.",
        alt_ru="Сайт-архив поездки на Балхаш",
        alt_en="The Balkhash trip archive site",
        tags=["Next.js", "TypeScript", "Static Export"],
        links=[("demo", f"{PAGES}/balhash/"), ("repo", f"{GH}/balhash")],
    ),
    dict(
        id="tag-bot", cat="bots", img="tagbot", private=True,
        ru="tag-bot", en="tag-bot",
        dru="Бот, который зовёт всех разом. Переехал с aiogram-поллинга на webhook Cloudflare Worker и KV: сервера нет, есть функция.",
        den="A bot that pings everyone at once. Moved off aiogram polling onto a Cloudflare Worker webhook and KV: no server, just a function.",
        alt_ru="Страница tag-bot: описание команд бота",
        alt_en="The tag-bot page: bot command overview",
        tags=["TypeScript", "Cloudflare Workers", "KV"],
        links=[("site", f"{PAGES}/tag-bot-site/")],
    ),
    dict(
        id="crosspost", cat="bots", img=None, private=True,
        ru="crosspost-worker", en="crosspost-worker",
        dru="Написал один раз — ушло в Telegram, VK, Instagram и Threads. OAuth и загрузка медиа целиком внутри воркера.",
        den="Compose once, and it lands in Telegram, VK, Instagram and Threads. OAuth and media upload live entirely inside the worker.",
        tags=["TypeScript", "Cloudflare Workers", "OAuth"], links=[],
    ),
    dict(
        id="studio-site", cat="web", img="studiosite",
        ru="Box3D · Studio — сайт", en="Box3D · Studio — site",
        dru="Обзорный сайт обоих аддонов: три раздела на клиентском роутинге, один самодостаточный файл, ноль зависимостей.",
        den="The overview site for both addons: three sections on client-side routing, one self-contained file, zero dependencies.",
        alt_ru="Главная сайта двух Blender-аддонов",
        alt_en="Home page of the two-addon site",
        tags=["HTML", "CSS", "Vanilla JS"],
        links=[("demo", f"{PAGES}/box3d-studio-site/"), ("repo", f"{GH}/box3d-studio-site")],
    ),
    dict(
        id="studio103", cat="web", img="studio103",
        ru="Студия полировки 103", en="Detailing studio 103",
        dru="Стратегия выхода на рынок: аудитория, восемь конкурентов, прайс, каналы на 15 000 ₽ и дорожная карта на 12 недель.",
        den="A go-to-market strategy: audience, eight competitors, pricing, a ₽15,000 channel budget and a 12-week roadmap.",
        alt_ru="Страница со стратегией студии полировки кузова",
        alt_en="Strategy page for a car detailing studio",
        tags=["HTML", "CSS", "Research"],
        links=[("demo", f"{PAGES}/103_studio_plan/"), ("repo", f"{GH}/103_studio_plan")],
    ),
]

LINK_LABELS = {
    "demo": ("Демо", "Live"), "repo": ("Код", "Source"),
    "site": ("Сайт", "Site"), "dl": ("Скачать", "Download"),
    "case": ("Кейс", "Case"),
}
FILTERS = [("all", "Все", "All"), ("blender", "Blender", "Blender"),
           ("macos", "macOS", "macOS"), ("web", "Веб", "Web"),
           ("bots", "Боты", "Bots")]
MARQUEE = ["Python", "Swift", "TypeScript", "Blender API", "Cloudflare Workers",
           "Next.js", "SwiftUI", "ctypes", "Cloudflare KV", "Vanilla JS"]

e = html.escape


def t(tag, ru, en, cls="", extra=""):
    """Двуязычный текстовый узел."""
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c}{extra} data-ru="{e(ru)}" data-en="{e(en)}">{e(ru)}</{tag}>'


def thumb(vid):
    """Превью с ytimg. maxres есть не у всех роликов — проверяем на сборке."""
    import urllib.request
    for name, w, h in (("maxresdefault", 1280, 720), ("hqdefault", 480, 360)):
        url = f"https://i.ytimg.com/vi/{vid}/{name}.jpg"
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    return url, w, h
        except Exception:
            pass
    return f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg", 480, 360


PLAY = ('<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" focusable="false">'
        '<path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>')


def player(vid, ratio, alt_ru, alt_en, lab_ru, lab_en, poster=None, eager=False):
    """Превью со ссылкой на ролик. С JS ссылка превращается в плеер на месте,
    без JS — просто открывает YouTube в новой вкладке."""
    if poster:
        src, w, h = f"img/reel/{poster}", 1280, 720
    else:
        src, w, h = thumb(vid)
    return (
        f'<div class="player" style="--ratio:{ratio.replace(":", "/")}">'
        f'<img class="player__shot" src="{e(src)}" width="{w}" height="{h}"'
        f' loading="{"eager" if eager else "lazy"}" decoding="async"'
        f' alt="{e(alt_ru)}" data-alt-ru="{e(alt_ru)}" data-alt-en="{e(alt_en)}">'
        f'<a class="player__btn" href="https://www.youtube.com/watch?v={e(vid)}"'
        f' target="_blank" rel="noopener" data-yt="{e(vid)}"'
        f' aria-label="{e(lab_ru)}" data-label-ru="{e(lab_ru)}" data-label-en="{e(lab_en)}">'
        f'{PLAY}</a></div>')


def reel_section():
    """Секция с шоурилом. Пока нет id — секции нет вовсе."""
    if not REEL_ID and not SHOTS:
        return ""

    out = ['<section id="reel" class="reel">']
    out.append(t("h2", "Шоурил", "Showreel", "reel__h"))
    out.append(t("p", "Ролики для мобильных игр: сборка сцены, анимация, физика, композ и звук — всё моё.",
                 "Ad creatives for mobile games: scene build, animation, physics, comp and sound — all mine.",
                 "reel__sub"))

    if REEL_ID:
        w, h = (int(x) for x in REEL_RATIO.split(":"))
        vert = w < h
        out.append(f'<div class="reel__main{" reel__main--v" if vert else ""}">')
        out.append(player(REEL_ID, REEL_RATIO,
                          "Превью шоурила", "Showreel preview",
                          "Смотреть шоурил", "Play showreel", eager=True))
        out.append("</div>")
        if CHANNEL:
            out.append(f'<p class="reel__more"><a class="lnk" href="{e(CHANNEL)}"'
                       f' target="_blank" rel="noopener"'
                       f' data-ru="Все ролики на канале" data-en="Every creative on the channel">'
                       f'Все ролики на канале'
                       f'<svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true" focusable="false">'
                       f'<path d="M3 9L9 3M9 3H4.2M9 3v4.8" fill="none" stroke="currentColor"'
                       f' stroke-width="1.6" stroke-linecap="square"/></svg></a></p>')

    if SHOTS:
        out.append('<ul class="shots">')
        for sh in SHOTS:
            out.append('<li class="shot">')
            out.append(player(sh["id"], sh.get("ratio", "9:16"),
                              f'Кадр из ролика: {sh["ru"]}', f'Still from: {sh["en"]}',
                              f'Смотреть: {sh["ru"]}', f'Play: {sh["en"]}',
                              poster=sh.get("poster")))
            out.append('<div class="shot__body">')
            out.append(f'<h3 class="shot__t">{e(sh["ru"])}</h3>' if sh["ru"] == sh["en"]
                       else t("h3", sh["ru"], sh["en"], "shot__t"))
            out.append(t("p", sh["dru"], sh["den"], "shot__d"))
            out.append("</div></li>")
        out.append("</ul>")

    out.append("</section>")
    return "\n".join(out)


def card(p, i):
    cls = "card" + (" card--big" if p.get("big") else "")
    out = [f'<article class="{cls}" data-cat="{p["cat"]}" style="--i:{i}">']

    if p["img"]:
        out.append(
            f'<div class="card__shot"><img src="img/{p["img"]}.webp" width="1200" height="750"'
            f' loading="{"eager" if i < 2 else "lazy"}" decoding="async"'
            f' alt="{e(p["alt_ru"])}" data-alt-ru="{e(p["alt_ru"])}" data-alt-en="{e(p["alt_en"])}"></div>')
    else:
        glyphs = "".join(f'<span aria-hidden="true">{e(x)}</span>' for x in
                         ["TG", "VK", "IG", "TH", "→", "//", "OAuth", "KV", "fetch", "R2", "202", "→"])
        out.append(f'<div class="card__shot card__shot--blank"><div class="glyphs">{glyphs}</div></div>')

    out.append('<div class="card__body">')
    out.append('<div class="card__head">')
    out.append(f'<h3 class="card__title">{e(p["ru"])}</h3>' if p["ru"] == p["en"]
               else t("h3", p["ru"], p["en"], "card__title"))
    badges = []
    if p.get("meta"):
        badges.append(f'<span class="badge badge--ver">{e(p["meta"])}</span>')
    if p.get("private"):
        badges.append(t("span", "приватный", "private", "badge badge--priv"))
    if badges:
        out.append(f'<div class="card__badges">{"".join(badges)}</div>')
    out.append("</div>")

    out.append(t("p", p["dru"], p["den"], "card__desc"))
    out.append('<ul class="tags">' + "".join(f"<li>{e(x)}</li>" for x in p["tags"]) + "</ul>")

    if p["links"]:
        ls = []
        for kind, href in p["links"]:
            ru, en = LINK_LABELS[kind]
            ls.append(f'<li><a class="lnk" href="{e(href)}" target="_blank" rel="noopener"'
                      f' data-ru="{e(ru)}" data-en="{e(en)}">{e(ru)}'
                      f'<svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true" focusable="false">'
                      f'<path d="M3 9L9 3M9 3H4.2M9 3v4.8" fill="none" stroke="currentColor"'
                      f' stroke-width="1.6" stroke-linecap="square"/></svg></a></li>')
        out.append(f'<ul class="links">{"".join(ls)}</ul>')

    out.append("</div></article>")
    return "\n".join(out)


chips = "\n".join(
    f'<button class="chip" type="button" role="tab" aria-selected="{"true" if k == "all" else "false"}"'
    f' data-filter="{k}" data-ru="{e(ru)}" data-en="{e(en)}">{e(ru)}</button>'
    for k, ru, en in FILTERS)

strip = "".join(f'<span>{e(x)}</span><i aria-hidden="true">◆</i>' for x in MARQUEE)
cards = "\n".join(card(p, i) for i, p in enumerate(PROJECTS))
reel = reel_section()

page = f'''<!doctype html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Константин — 3D motion designer</title>
<meta name="description" content="3D-креативы для мобильных игр и инструменты под них: аддоны для Blender, приложения под macOS, сайты и боты.">
<meta name="color-scheme" content="dark light">
<meta property="og:title" content="Константин — 3D motion designer">
<meta property="og:description" content="3D-креативы для мобильных игр и инструменты под них: аддоны, приложения, боты.">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&family=Unbounded:wght@700;800&display=swap">
<link rel="stylesheet" href="styles.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23DFE104'/%3E%3Ctext x='16' y='24' font-family='monospace' font-size='22' font-weight='700' text-anchor='middle' fill='%23000'%3EK%3C/text%3E%3C/svg%3E">
<script>
  // Тему и язык ставим до первой отрисовки, чтобы не мигало.
  (function () {{
    var d = document.documentElement;
    d.classList.add('js');
    try {{
      var th = localStorage.getItem('theme');
      if (th === 'light' || th === 'dark') d.dataset.theme = th;
      else if (matchMedia('(prefers-color-scheme: light)').matches) d.dataset.theme = 'light';
      var lg = localStorage.getItem('lang');
      d.lang = (lg === 'en' || lg === 'ru') ? lg
        : ((navigator.language || 'ru').slice(0, 2) === 'ru' ? 'ru' : 'en');
    }} catch (err) {{ /* приватный режим — остаёмся на дефолте */ }}
    // Если app.js не доехал, снимаем .js и показываем всё как есть.
    setTimeout(function () {{
      if (!d.classList.contains('ready')) d.classList.remove('js');
    }}, 2500);
  }})();
</script>
</head>
<body>
<a class="skip" href="#work" data-ru="К проектам" data-en="Skip to work">К проектам</a>

<header class="top">
  <a class="top__name" href="#top"><span data-ru="Константин" data-en="Konstantin">Константин</span></a>
  <div class="top__ctl">
    <a class="top__cv" href="cv/" data-ru="Резюме" data-en="CV">Резюме</a>
    <div class="seg" role="group" aria-label="Язык / Language">
      <button type="button" class="seg__b" data-lang="ru" aria-pressed="true">RU</button>
      <button type="button" class="seg__b" data-lang="en" aria-pressed="false">EN</button>
    </div>
    <button type="button" class="icon-b" id="theme" aria-label="Сменить тему"
            data-label-ru="Сменить тему" data-label-en="Toggle theme">
      <svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true" focusable="false">
        <circle cx="10" cy="10" r="4.4" fill="none" stroke="currentColor" stroke-width="1.7"/>
        <path d="M10 1.4v2.2M10 16.4v2.2M1.4 10h2.2M16.4 10h2.2M4 4l1.6 1.6M14.4 14.4L16 16M16 4l-1.6 1.6M5.6 14.4L4 16"
              stroke="currentColor" stroke-width="1.7" stroke-linecap="square"/>
      </svg>
    </button>
  </div>
</header>

<main id="top">
  <section class="hero">
    <p class="hero__kicker" data-ru="Портфолио · 2026" data-en="Portfolio · 2026">Портфолио · 2026</p>
    <h1 class="hero__h">
      <span class="hero__l1" data-ru="Делаю" data-en="I make">Делаю</span>
      <span class="hero__l2" data-ru="ролики" data-en="the ads">ролики</span>
      <span class="hero__l3" data-ru="и то, чем" data-en="and the tools">и то, чем</span>
      <span class="hero__l4" data-ru="их делают" data-en="that make them">их делают</span>
    </h1>
    <p class="hero__sub"
       data-ru="3D-креативы для мобильных игр: локация, персонажи, физика, композ и звук. И то, чем я их собираю: аддоны для Blender, приложения и боты — всё своё, без форков."
       data-en="3D ad creatives for mobile games: environments, characters, physics, comp and sound. Plus what I build them with: Blender addons, apps and bots — all mine, no forks.">
      3D-креативы для мобильных игр: локация, персонажи, физика, композ и звук. И то, чем я их собираю: аддоны для Blender, приложения и боты — всё своё, без форков.
    </p>
  </section>

{reel}

  <div class="marquee" aria-hidden="true">
    <div class="marquee__row"><div class="marquee__grp">{strip}</div><div class="marquee__grp">{strip}</div></div>
  </div>

  <section id="work" class="work">
    <div class="chips" role="tablist" aria-label="Фильтр проектов">
{chips}
    </div>
    <div class="grid" id="grid">
{cards}
    </div>
    <p class="empty" id="empty" hidden data-ru="Здесь пусто." data-en="Nothing here.">Здесь пусто.</p>
  </section>
</main>

<footer class="foot">
  <p class="foot__t" data-ru="Написать" data-en="Say hi">Написать</p>
  <a class="foot__tg" href="https://t.me/zhustbie" target="_blank" rel="noopener">
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">
      <path d="M21.6 4.3 18.4 20c-.24 1.06-.87 1.32-1.77.82l-4.9-3.6-2.36 2.27c-.26.26-.48.48-.99.48l.35-5 9.1-8.22c.4-.35-.09-.55-.62-.2L5.96 13.63l-4.84-1.5c-1.05-.33-1.07-1.05.22-1.56L20.24 2.9c.88-.32 1.65.2 1.36 1.4Z" fill="currentColor"/>
    </svg>
    <span>@zhustbie</span>
  </a>
  <p class="foot__c">© 2026</p>
</footer>

<script src="app.js" defer></script>
</body>
</html>
'''

pathlib.Path("index.html").write_text(page, encoding="utf-8")
print(f"index.html — {len(PROJECTS)} проектов, {len(page)} байт")
