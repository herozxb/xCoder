import webbrowser
import os
import re
import ollama

class SimpleFrameAgent:
    def __init__(self, model_name):
        self.model_name = model_name

    def plan_tool(self, task_description):
        # 最简：固定 5 part，不需要 LLM 规划
        return f"""PLAN FOR: {task_description}
PART 1: HEADER (logo + search + actions)
PART 2: CHIPS ROW (categories)
PART 3: MAIN GRID (video cards)
PART 4: LOAD MORE / PAGINATION
PART 5: FOOTER (links)"""

    def generate_part_tool(self, part_number, plan, goal):
        # 最简：直接模板，不需要 LLM 生成（更稳定）
        templates = {
            1: """
<header class="app-header" role="banner" aria-label="Top navigation">
  <div class="header__left" aria-label="Brand">
    <div class="ui-box ui-box--logo" aria-hidden="true"></div>
  </div>

  <div class="header__center" role="search" aria-label="Search">
    <div class="ui-box ui-box--search" aria-hidden="true"></div>
  </div>

  <div class="header__right" aria-label="Actions">
    <div class="ui-box ui-box--icon" aria-hidden="true"></div>
    <div class="ui-box ui-box--icon" aria-hidden="true"></div>
    <div class="ui-box ui-box--avatar" aria-hidden="true"></div>
  </div>
</header>
""",
            2: """
<section class="chips" aria-label="Category filters">
  <div class="chips__row">
    <div class="chip" aria-hidden="true"></div>
    <div class="chip" aria-hidden="true"></div>
    <div class="chip" aria-hidden="true"></div>
    <div class="chip" aria-hidden="true"></div>
    <div class="chip" aria-hidden="true"></div>
    <div class="chip" aria-hidden="true"></div>
  </div>
</section>
""",
            3: """
<main class="content" role="main" aria-label="Main content">
  <section class="grid" aria-label="Video grid">
    <article class="card" aria-label="Video card">
      <div class="card__thumb" aria-hidden="true"></div>
      <div class="card__meta">
        <div class="card__avatar" aria-hidden="true"></div>
        <div class="card__text">
          <div class="card__title" aria-hidden="true"></div>
          <div class="card__sub" aria-hidden="true"></div>
        </div>
      </div>
    </article>

    <article class="card" aria-label="Video card">
      <div class="card__thumb" aria-hidden="true"></div>
      <div class="card__meta">
        <div class="card__avatar" aria-hidden="true"></div>
        <div class="card__text">
          <div class="card__title" aria-hidden="true"></div>
          <div class="card__sub" aria-hidden="true"></div>
        </div>
      </div>
    </article>

    <article class="card" aria-label="Video card">
      <div class="card__thumb" aria-hidden="true"></div>
      <div class="card__meta">
        <div class="card__avatar" aria-hidden="true"></div>
        <div class="card__text">
          <div class="card__title" aria-hidden="true"></div>
          <div class="card__sub" aria-hidden="true"></div>
        </div>
      </div>
    </article>

    <article class="card" aria-label="Video card">
      <div class="card__thumb" aria-hidden="true"></div>
      <div class="card__meta">
        <div class="card__avatar" aria-hidden="true"></div>
        <div class="card__text">
          <div class="card__title" aria-hidden="true"></div>
          <div class="card__sub" aria-hidden="true"></div>
        </div>
      </div>
    </article>

    <article class="card" aria-label="Video card">
      <div class="card__thumb" aria-hidden="true"></div>
      <div class="card__meta">
        <div class="card__avatar" aria-hidden="true"></div>
        <div class="card__text">
          <div class="card__title" aria-hidden="true"></div>
          <div class="card__sub" aria-hidden="true"></div>
        </div>
      </div>
    </article>

    <article class="card" aria-label="Video card">
      <div class="card__thumb" aria-hidden="true"></div>
      <div class="card__meta">
        <div class="card__avatar" aria-hidden="true"></div>
        <div class="card__text">
          <div class="card__title" aria-hidden="true"></div>
          <div class="card__sub" aria-hidden="true"></div>
        </div>
      </div>
    </article>
  </section>
</main>
""",
            4: """
<section class="pager" aria-label="Pagination">
  <div class="ui-box ui-box--loadmore" aria-hidden="true"></div>
</section>
""",
            5: """
<footer class="footer" role="contentinfo" aria-label="Footer">
  <div class="footer__cols">
    <div class="ui-box ui-box--footercol" aria-hidden="true"></div>
    <div class="ui-box ui-box--footercol" aria-hidden="true"></div>
    <div class="ui-box ui-box--footercol" aria-hidden="true"></div>
  </div>
</footer>
"""
        }
        return templates[part_number].strip()

    def build_min_css(self):
        # “最小框架 CSS”：只画线、间距、基本布局
        return """
<style>
  :root{
    --bg: #0f0f0f;
    --panel: #151515;
    --border: #272727;
    --text: #e5e5e5;
    --muted: #9aa0a6;
    --gap: 16px;
    --radius: 12px;
  }

  *{ box-sizing: border-box; }
  html,body{ height:100%; }
  body{
    margin:0;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
  }

  /* Part 1 */
  .app-header{
    position: sticky;
    top: 0;
    z-index: 10;
    display:flex;
    align-items:center;
    gap: var(--gap);
    padding: 12px 16px;
    background: rgba(15,15,15,0.9);
    border-bottom: 1px solid var(--border);
  }
  .header__left{ width: 120px; display:flex; align-items:center; }
  .header__center{ flex:1; display:flex; justify-content:center; }
  .header__right{ width: 160px; display:flex; justify-content:flex-end; gap: 10px; align-items:center; }

  /* Part 2 */
  .chips{
    border-bottom: 1px solid var(--border);
    background: var(--bg);
  }
  .chips__row{
    display:flex;
    gap: 10px;
    padding: 10px 16px;
    overflow:auto;
    scrollbar-width: none;
  }
  .chips__row::-webkit-scrollbar{ display:none; }

  /* Part 3 */
  .content{ padding: 16px; }
  .grid{
    display:grid;
    gap: var(--gap);
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  }
  .card{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow:hidden;
    min-height: 220px;
  }
  .card__thumb{
    height: 140px;
    border-bottom: 1px solid var(--border);
    background: #101010;
  }
  .card__meta{
    display:flex;
    gap: 12px;
    padding: 12px;
  }
  .card__avatar{
    width: 36px;
    height: 36px;
    border-radius: 999px;
    border: 1px solid var(--border);
  }
  .card__text{ flex:1; display:flex; flex-direction:column; gap: 10px; }
  .card__title{ height: 14px; border: 1px solid var(--border); border-radius: 6px; }
  .card__sub{ height: 12px; border: 1px solid var(--border); border-radius: 6px; opacity: 0.7; }

  /* Part 4 */
  .pager{
    padding: 16px;
    display:flex;
    justify-content:center;
  }

  /* Part 5 */
  .footer{
    border-top: 1px solid var(--border);
    padding: 16px;
    background: var(--bg);
  }
  .footer__cols{
    display:grid;
    gap: var(--gap);
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }

  /* Generic placeholders */
  .ui-box{
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--panel);
  }
  .ui-box--logo{ width: 88px; height: 24px; border-radius: 8px; }
  .ui-box--search{ width: min(640px, 100%); height: 40px; border-radius: 999px; }
  .ui-box--icon{ width: 28px; height: 28px; border-radius: 8px; }
  .ui-box--avatar{ width: 32px; height: 32px; border-radius: 999px; }
  .chip{ width: 84px; height: 32px; border-radius: 999px; border: 1px solid var(--border); background: var(--panel); flex: 0 0 auto; }
  .ui-box--loadmore{ width: 180px; height: 44px; border-radius: 999px; }
  .ui-box--footercol{ height: 80px; }

  /* Minimal responsive tweak */
  @media (max-width: 480px){
    .header__left{ width: 72px; }
    .header__right{ width: 120px; }
    .content{ padding: 12px; }
    .grid{ grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); }
  }
</style>
""".strip()

    def execute(self, user_goal):
        plan = self.plan_tool(user_goal)

        parts = []
        for i in range(1, 6):
            parts.append(self.generate_part_tool(i, plan, user_goal))

        html = "\n".join([
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "  <meta charset='utf-8' />",
            "  <meta name='viewport' content='width=device-width, initial-scale=1' />",
            "  <title>Frame</title>",
            self.build_min_css(),
            "</head>",
            "<body>",
            "\n".join(parts),
            "</body>",
            "</html>",
        ])

        file_path = "frame_only.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        webbrowser.open(f"file://{os.path.realpath(file_path)}")

# Run
agent = SimpleFrameAgent("deepseek-coder-v2")
agent.execute("just show me a youtube.com front page no sidebar")
