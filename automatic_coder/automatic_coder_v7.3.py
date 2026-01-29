import webbrowser
import os
import ollama
import re

class SimpleFrameAgent:
    def __init__(self, model_name):
        self.model_name = model_name

    def plan_tool(self, task_description):
        # Simplified plan that outlines the basic structure of the page
        return f"""PLAN FOR: {task_description}
PART 1: HEADER (logo + search + actions)
PART 2: CHIPS ROW (categories)
PART 3: MAIN GRID (video cards)
PART 4: LOAD MORE / PAGINATION
PART 5: FOOTER (links)"""

    def generate_part_tool(self, plan):
        # Generate HTML based on the simplified plan using the LLM model (ollama)
        prompt = f"""
Generate a complete HTML structure and layout based on the following plan. The HTML should be clean, accessible, and semantic.
DO NOT use predefined templates. Instead, generate the HTML dynamically based on the given plan:

{plan}

TECHNICAL REQUIREMENTS:
1. Use only semantic HTML5 elements: <header>, <nav>, <main>, <section>, <article>, <aside>, <footer>, etc.
2. Implement CSS Grid or Flexbox for layouts (prefer Grid for 2D layouts, Flexbox for 1D).
3. Include mobile-first responsive design with media queries.
4. Use CSS custom properties (variables) for colors, spacing, and typography.
5. Follow BEM naming convention for class names: block__element--modifier.
6. Ensure accessibility standards are met: aria-labels, roles, keyboard navigation.
7. Use smooth transitions (e.g., transition: all 0.3s ease) for interactive elements.
8. Apply focus and hover states for interactive elements.

CODE QUALITY:
- No explanatory text or comments
- Production-ready code


OUTPUT FORMAT:
- Return ONLY the HTML structure with embedded <style> tags.
- Ensure the HTML structure includes the necessary sections (header, main, footer, etc.).
"""

        # Send the prompt to the LLM model for generating HTML
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        refined_html = response['message']['content']
        refined_html = self._clean_generated_code(refined_html) 
        return refined_html

    def _clean_generated_code(self, code):
        """
        Cleans up common formatting issues from LLM-generated code.
        """
        # Remove markdown code blocks
        code = re.sub(r'```html\s*', '', code)
        code = re.sub(r'```\s*', '', code)
        
        # Remove common explanatory prefixes
        code = re.sub(r'^(Here\'s|Here is|Here\'s the|The code|Code for).*?:\s*', '', code, flags=re.IGNORECASE | re.MULTILINE)
        
        # Remove leading/trailing whitespace but preserve structure
        code = code.strip()
        
        # Ensure it starts with an HTML tag
        if not code.strip().startswith('<'):
            # Try to find first HTML tag
            match = re.search(r'<[^>]+>', code)
            if match:
                code = code[match.start():]
        
        return code

    def execute(self, user_goal):
        plan = self.plan_tool(user_goal)
        html = self.generate_part_tool(plan)

        # Save the generated HTML to a file and open it in a browser
        file_path = "generated_page.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        webbrowser.open(f"file://{os.path.realpath(file_path)}")

# Run the agent with a goal
agent = SimpleFrameAgent("deepseek-coder-v2")
agent.execute("just show me a youtube.com front page with sidebar")
