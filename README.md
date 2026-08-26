# Портфолио

Одна страница со своими проектами. Статика без сборки и зависимостей,
живёт на GitHub Pages: **https://justbelieve9.github.io/portfolio/**

Форки, копии чужих репозиториев и зеркала релизов сюда не попадают —
только то, что написано самостоятельно.

## Как устроено

| Файл | Назначение |
|---|---|
| `build.py` | список проектов и генератор `index.html` |
| `index.html` | готовая страница, лежит в репозитории собранной |
| `styles.css` | токены, сетка, две темы, появление карточек |
| `app.js` | язык, тема, фильтры, `IntersectionObserver` |
| `img/` | скриншоты проектов в WebP 1200×750 |

Карточки рендерятся статикой, а не из JavaScript: без него страница
читается целиком. Класс `js` ставится в `<head>`, и страховка снимает
его через 2,5 секунды, если `app.js` не загрузился.

Обе локали лежат в одном DOM — у текстовых узлов `data-ru` / `data-en`,
`app.js` только подменяет `textContent`. Поэтому нет ни второго HTML,
ни мигания при переключении.

## Правки

Проекты правятся в `PROJECTS` внутри `build.py`, потом:

```bash
python3 build.py
```

## Локальный запуск

```bash
python3 -m http.server 8801
```

## Скриншоты

Сняты headless-браузером с живых страниц проектов, ужаты в WebP 1200×750:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1440,900 --virtual-time-budget=12000 \
  --screenshot=out.png <url>
```
