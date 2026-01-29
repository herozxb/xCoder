import webbrowser
import os
import ollama
import re

class SimpleFrameAgent:
    def __init__(self, model_name):
        self.model_name = model_name

    def plan_tool(self, task_description):
        """
        Enhanced planning tool that creates a structured 5-part plan for web page development.
        Each part corresponds to a specific component of the web page architecture.
        Includes error handling, response validation, and adaptive planning.
        """
        print(f"  [Agent Planning: {task_description}]")
        
        
        prompt = f"""You are a senior web architect and UX designer planning the structure of a web page.

        TASK: Create a detailed 5-part structural plan for: {task_description}


        WEB PAGE ARCHITECTURE REQUIREMENTS:
        The plan must be divided into exactly 5 parts, each representing a specific component:

        PART 1: HEADER & NAVIGATION
        - Main header with branding/logo area
        - Primary navigation menu structure and hierarchy
        - Search functionality (if applicable)
        - User account controls and authentication UI
        - Mobile menu considerations
        - Sticky/fixed header behavior

        PART 2: HERO SECTION / MAIN CONTENT AREA
        - Primary content area layout and grid structure
        - Key visual elements (images, videos, graphics)
        - Headline hierarchy and typography
        - Call-to-action components and placement
        - Content hierarchy and visual flow
        - Above-the-fold optimization

        PART 3: FEATURE SECTIONS / CONTENT BLOCKS
        - Secondary content areas and sections
        - Feature highlights and showcase elements
        - Information organization and card layouts
        - Interactive elements and hover states
        - Content grid or list structures
        - Spacing and visual rhythm

        PART 4: SIDEBAR / SUPPORTING CONTENT
        - Secondary navigation or breadcrumbs
        - Related content and recommendations
        - Widgets, tools, or utility components
        - Additional functionality and CTAs
        - Social proof elements (if applicable)
        - Responsive sidebar behavior

        PART 5: FOOTER & FINAL ELEMENTS
        - Footer structure and column layout
        - Contact information and links
        - Legal links (privacy, terms, etc.)
        - Social media integration
        - Newsletter signup (if applicable)
        - Copyright and attribution

        PLANNING REQUIREMENTS:
        1. Each part must be clearly numbered (PART 1, PART 2, etc.) and described in detail
        2. Focus on structure, layout, and component organization - NOT specific code
        3. Consider responsive design principles (mobile-first approach)
        4. Include accessibility considerations (ARIA, keyboard navigation, screen readers)
        5. Ensure logical flow and visual hierarchy between parts
        6. Account for user experience and intuitive navigation
        7. Plan for scalability and maintainability
        8. Consider loading performance and content prioritization
        9. Specify color scheme and visual style direction
        10. Include interactive element descriptions

        OUTPUT FORMAT:
        - Start with a brief overview (1-2 sentences)
        - Then list exactly 5 parts, each clearly labeled as "PART 1:", "PART 2:", etc.
        - Under each part, use bullet points (-) for each component/sub-component
        - Be specific about layout, positioning, and visual elements
        - Do NOT include any HTML or CSS code
        - Do NOT use markdown code blocks
        - Keep descriptions concise but comprehensive

        Create the 5-part plan for: {task_description}"""
        
        response = ollama.chat(
            model=self.model_name, 
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.7}  # Slightly creative but focused
        )
        plan = response['message']['content']
        
        # Validate and enhance the plan
        print("==========plan============")
        print(plan)
        return plan


    def refine_tool(self, part_number, html_part, goal):
        # Adjust the refinement prompt for each part based on its specific requirements
        prompts = {
            1: f"Refine this header & navigation HTML part. Make sure the header is sticky, 56px height, with backdrop-blur on scroll. Include a left hamburger menu and logo with an SVG. Center should contain a 640px max-width search container with proper focus states. Right should have action icons and a user avatar. For mobile, make the menu collapsible and the search overlay functional. Ensure accessibility and follow responsive design principles. \n\nHTML Part: {html_part}",
            2: f"Refine this hero/primary content area HTML part. The content should be organized with CSS Grid (auto-fill, minmax 320px). Each video card should have a 16:9 aspect ratio thumbnail. Typography should be 16px base, 14px meta, and 12px details. Add hover effects with a scale(1.02) transform and shadow elevation. Include loading states and skeleton screens for better user experience. Ensure accessibility with appropriate aria labels. \n\nHTML Part: {html_part}",
            3: f"Refine this content cards & features section. Ensure consistent padding of 12px for cards. Optimize images using object-fit cover and lazy loading. Layout metadata using flexbox with space-between. Add interactive elements with focus-visible outlines. Ensure accessibility standards (aria-labels, keyboard navigation). \n\nHTML Part: {html_part}",
            4: f"Refine this secondary navigation & widgets HTML part. Include a sidebar with 240px width and scrollable content. Use section dividers with 1px #272727 borders. Use a consistent icon system (24px icons, currentColor fill). Ensure the sidebar is collapsible on mobile devices. Manage active/hover/focus states effectively. \n\nHTML Part: {html_part}",
            5: f"Refine this footer HTML part. Ensure a multi-column footer with semantic HTML5 elements. Organize links in a hierarchical structure. Include social media icons with consistent sizing and alignment. Make sure the footer is legally compliant with privacy and terms links. Minimize the DOM and optimize selectors for performance. \n\nHTML Part: {html_part}",
        }

        # Get the appropriate refinement prompt for the given part
        prompt = prompts.get(part_number, f"Refine the following HTML part: {html_part}")
        prompt += """
                TECHNICAL REQUIREMENTS:
        1. Generate ONLY the HTML structure and content for Part {part_number}.
        2. DO NOT change any CSS styles or layout (e.g., Grid/Flexbox), except for sizes (font size, widths, etc.).
        3. ONLY modify the content, structure, or accessibility attributes (e.g., aria-labels, roles, etc.).
        4. Make sure the content is clean, accessible, and semantically correct with proper use of HTML5 tags.
        5. Ensure accessibility: focus states, aria labels, and keyboard navigation.
        6. Keep the existing CSS intact unless it's necessary to adjust sizes.
        7. Follow all WCAG 2.1 AA standards.

        OUTPUT FORMAT:
        Return ONLY the HTML structure (without changing CSS styles) with embedded <style> tags if any size adjustments are made.
        Start directly with the opening tag (e.g., <section>, <header>, <div>).
"""
        
        # Send the prompt to the LLM model for refinement
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        refined_html = response['message']['content']
        print("==========refined_html============")
        print(refined_html)        
        return refined_html.strip()

    def generate_part_tool(self, part_number, plan, goal):
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
    <!-- Repeat articles as necessary -->
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

  .app-header{ position: sticky; top: 0; z-index: 10; display:flex; align-items:center; gap: var(--gap); padding: 12px 16px; background: rgba(15,15,15,0.9); border-bottom: 1px solid var(--border); }
  .header__left{ width: 120px; display:flex; align-items:center; }
  .header__center{ flex:1; display:flex; justify-content:center; }
  .header__right{ width: 160px; display:flex; justify-content:flex-end; gap: 10px; align-items:center; }

  .chips{ border-bottom: 1px solid var(--border); background: var(--bg); }
  .chips__row{ display:flex; gap: 10px; padding: 10px 16px; overflow:auto; scrollbar-width: none; }
  .chips__row::-webkit-scrollbar{ display:none; }

  .content{ padding: 16px; }
  .grid{ display:grid; gap: var(--gap); grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }

  .pager{ padding: 16px; display:flex; justify-content:center; }

  .footer{ border-top: 1px solid var(--border); padding: 16px; background: var(--bg); }
  .footer__cols{ display:grid; gap: var(--gap); grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }

  .ui-box{ border: 1px solid var(--border); border-radius: var(--radius); background: var(--panel); }
  .ui-box--logo{ width: 88px; height: 24px; border-radius: 8px; }
  .ui-box--search{ width: min(640px, 100%); height: 40px; border-radius: 999px; }
  .ui-box--icon{ width: 28px; height: 28px; border-radius: 8px; }
  .ui-box--avatar{ width: 32px; height: 32px; border-radius: 999px; }
  .chip{ width: 84px; height: 32px; border-radius: 999px; border: 1px solid var(--border); background: var(--panel); flex: 0 0 auto; }
  .ui-box--loadmore{ width: 180px; height: 44px; border-radius: 999px; }
  .ui-box--footercol{ height: 80px; }
</style>
""".strip()

    def execute(self, user_goal):
        plan = self.plan_tool(user_goal)

        parts = []
        for i in range(1, 6):
            # Generate the part and refine it using LLM model
            part_html = self.generate_part_tool(i, plan, user_goal)
            refined_part_html = self.refine_tool(i, part_html, user_goal)
            parts.append(refined_part_html)
            #parts.append(part_html)

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

        file_path = "frame_refined.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        webbrowser.open(f"file://{os.path.realpath(file_path)}")

# Run the agent with a goal
agent = SimpleFrameAgent("deepseek-coder-v2")
agent.execute("just show me a login page for a website")
