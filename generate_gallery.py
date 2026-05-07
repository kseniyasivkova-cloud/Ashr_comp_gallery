import os
import json

ROOT_DIR = "app_screenshots"
OUTPUT = "gallery.html"

CATEGORIES = {
    "Контентные wellness-платформы": [
        "Calm", "Headspace Sleep & Meditation", "Insight Timer Meditate, Sleep",
        "Balance Meditation & Sleep", "Aura Meditation & Sleep, CBT",
        "Better Sleep", "TIDE Sleep, Focus, Meditation",
    ],
    "Функциональный аудио-wellness": [
        "Endel", "Brain.fm Focus & Sleep Music", "Noisli", "Rain Rain Sleep Sounds",
    ],
    "Anti-scroll / Attention control": [
        "Opal Screen Time Control", "one sec screen time + focus",
        "Freedom Screen Time Control", "Forest Focus for Productivity",
        "Stay Focused AppSite Blocker",
    ],
    "Experience-first / Immersive": [
        "Loóna Sleep, reduce anxiety", "Portal - Escape Into Nature",
        "TRIPP Calm Focus Sleep Ascend", "Mesmerize - Visual Meditation",
    ],
}

def get_app_folder(partial):
    entries = os.listdir(ROOT_DIR)
    for e in entries:
        if e == partial or e.startswith(partial):
            return e
    # fuzzy: match by first word
    first = partial.split()[0].lower()
    for e in entries:
        if e.lower().startswith(first):
            return e
    return None

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def get_screenshots(folder):
    path = os.path.join(ROOT_DIR, folder)
    if not os.path.isdir(path):
        return [], [], []
    files = sorted(f for f in os.listdir(path)
                   if os.path.splitext(f)[1].lower() in IMAGE_EXTS)
    iphone = [f for f in files if f.lower().startswith("iphone")]
    ipad   = [f for f in files if f.lower().startswith("ipad")]
    other  = [f for f in files if not f.lower().startswith("iphone")
                                and not f.lower().startswith("ipad")]
    return iphone, ipad, other

# Build sections
html_sections = []
total_shown = 0

for category, apps in CATEGORIES.items():
    cards = []
    for app_partial in apps:
        folder = get_app_folder(app_partial)
        if not folder:
            continue
        iphone_files, ipad_files, other_files = get_screenshots(folder)
        all_files = iphone_files + ipad_files + other_files
        if not all_files:
            continue

        imgs_html = ""
        for fname in all_files:
            rel = f"app_screenshots/{folder}/{fname}"
            if fname.lower().startswith("iphone"):
                label = "iPhone"
            elif fname.lower().startswith("ipad"):
                label = "iPad"
            else:
                label = ""
            label_html = f'<span class="img-label">{label}</span>' if label else ""
            imgs_html += f"""
            <div class="img-wrap">
              <img src="{rel}" loading="lazy" alt="{fname}" onclick="openModal(this.src)">
              {label_html}
            </div>"""
            total_shown += 1

        if iphone_files or ipad_files:
            count_str = f"{len(iphone_files)} iPhone · {len(ipad_files)} iPad"
        else:
            count_str = f"{len(other_files)} скриншотов"

        cards.append(f"""
    <div class="app-card">
      <div class="app-header">
        <span class="app-name">{folder}</span>
        <span class="app-count">{count_str}</span>
      </div>
      <div class="screenshots">{imgs_html}
      </div>
    </div>""")

    if cards:
        html_sections.append(f"""
  <section class="category">
    <h2 class="cat-title">{category}</h2>
    {"".join(cards)}
  </section>""")

html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>App Screenshots Gallery — Competitors</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0f0f13;
    color: #e0e0e6;
    min-height: 100vh;
  }}

  header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 40px 32px 32px;
    border-bottom: 1px solid #ffffff18;
  }}
  header h1 {{ font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }}
  header p {{ margin-top: 8px; color: #8888aa; font-size: 14px; }}
  .badge {{
    display: inline-block;
    margin-top: 12px;
    background: #5c5cff22;
    border: 1px solid #5c5cff55;
    color: #9d9dff;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
  }}

  main {{ max-width: 1600px; margin: 0 auto; padding: 40px 24px 80px; }}

  .category {{ margin-bottom: 60px; }}
  .cat-title {{
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #5c5cff;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #ffffff12;
  }}

  .app-card {{
    background: #16161f;
    border: 1px solid #ffffff0e;
    border-radius: 16px;
    margin-bottom: 24px;
    overflow: hidden;
  }}
  .app-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    background: #1c1c28;
    border-bottom: 1px solid #ffffff0e;
  }}
  .app-name {{ font-weight: 600; font-size: 15px; color: #d0d0e8; }}
  .app-count {{ font-size: 12px; color: #666680; }}

  .screenshots {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding: 16px;
  }}
  .img-wrap {{
    position: relative;
    flex: 0 0 auto;
  }}
  .img-wrap img {{
    display: block;
    height: 220px;
    width: auto;
    border-radius: 10px;
    cursor: zoom-in;
    transition: transform 0.15s, box-shadow 0.15s;
    border: 1px solid #ffffff12;
  }}
  .img-wrap img:hover {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 40px #00000088;
  }}
  .img-label {{
    position: absolute;
    bottom: 6px;
    left: 6px;
    font-size: 10px;
    font-weight: 600;
    background: #000000aa;
    color: #ffffffbb;
    padding: 2px 7px;
    border-radius: 6px;
    pointer-events: none;
  }}

  /* Modal */
  #modal {{
    display: none;
    position: fixed;
    inset: 0;
    background: #000000ee;
    z-index: 1000;
    align-items: center;
    justify-content: center;
    cursor: zoom-out;
  }}
  #modal.open {{ display: flex; }}
  #modal img {{
    max-height: 92vh;
    max-width: 92vw;
    border-radius: 12px;
    box-shadow: 0 24px 80px #000;
  }}
  #modal-close {{
    position: fixed;
    top: 20px;
    right: 24px;
    font-size: 32px;
    color: #fff;
    cursor: pointer;
    line-height: 1;
    opacity: 0.7;
  }}
  #modal-close:hover {{ opacity: 1; }}
</style>
</head>
<body>
<header>
  <h1>Competitors Screenshot Gallery</h1>
  <p>Маркетинговые скриншоты из App Store · данные: iTunes Search API</p>
  <span class="badge">{total_shown} скриншотов · {sum(len(a) for a in CATEGORIES.values())} приложений</span>
</header>

<main>
{"".join(html_sections)}
</main>

<div id="modal" onclick="closeModal()">
  <span id="modal-close" onclick="closeModal()">&times;</span>
  <img id="modal-img" src="" alt="">
</div>

<script>
function openModal(src) {{
  document.getElementById('modal-img').src = src;
  document.getElementById('modal').classList.add('open');
  document.body.style.overflow = 'hidden';
}}
function closeModal() {{
  document.getElementById('modal').classList.remove('open');
  document.body.style.overflow = '';
}}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});
</script>
</body>
</html>"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Галерея сохранена: {OUTPUT}")
print(f"Всего скриншотов в галерее: {total_shown}")
