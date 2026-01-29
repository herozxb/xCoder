import webbrowser
import os
import ollama
import re

class RecursiveHTMLAgent:
    def __init__(self, model_name):
        self.model_name = model_name
        self.parts = {}

    def plan_tool(self, task_description):
        """
        Enhanced planning tool that creates a structured 5-part plan for web page development.
        Each part corresponds to a specific component of the web page architecture.
        Includes error handling, response validation, and adaptive planning.
        """
        print(f"  [Agent Planning: {task_description}]")
        
        # Analyze task type for more contextual planning
        task_type = self._analyze_task_type(task_description)
        
        prompt = f"""You are a senior web architect and UX designer planning the structure of a web page.

        TASK: Create a detailed 5-part structural plan for: {task_description}

        TASK CONTEXT: {task_type['context']}

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
        
        try:
            response = ollama.chat(
                model=self.model_name, 
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.7}  # Slightly creative but focused
            )
            plan = response['message']['content']
            
            # Validate and enhance the plan
            plan = self._validate_and_enhance_plan(plan, task_description)
            print("==========plan============")
            print(plan)
            return plan
            
        except Exception as e:
            print(f"  [Planning Error: {str(e)}]")
            # Return a fallback structured plan
            return self._generate_fallback_plan(task_description)
    
    def _analyze_task_type(self, task_description):
        """Analyzes the task description to provide contextual planning guidance."""
        desc_lower = task_description.lower()
        
        if any(word in desc_lower for word in ['landing', 'homepage', 'home page']):
            return {
                'context': 'This is a landing/homepage - focus on strong hero section, clear value proposition, and conversion elements.',
                'priority': 'hero_and_cta'
            }
        elif any(word in desc_lower for word in ['dashboard', 'admin', 'panel']):
            return {
                'context': 'This is a dashboard/admin interface - focus on data visualization, navigation, and utility components.',
                'priority': 'navigation_and_data'
            }
        elif any(word in desc_lower for word in ['blog', 'article', 'post']):
            return {
                'context': 'This is a content/blog page - focus on readability, typography, and content organization.',
                'priority': 'content_and_readability'
            }
        elif any(word in desc_lower for word in ['ecommerce', 'shop', 'store', 'product']):
            return {
                'context': 'This is an e-commerce page - focus on product display, shopping cart, and conversion optimization.',
                'priority': 'products_and_checkout'
            }
        elif any(word in desc_lower for word in ['portfolio', 'gallery', 'showcase']):
            return {
                'context': 'This is a portfolio/gallery page - focus on visual presentation and media display.',
                'priority': 'visuals_and_media'
            }
        else:
            return {
                'context': 'This is a general web page - ensure balanced structure with clear navigation and content organization.',
                'priority': 'balanced_structure'
            }
    
    def _validate_and_enhance_plan(self, plan, task_description):
        """Validates that the plan contains 5 parts and enhances if needed."""
        # Check if plan has all 5 parts
        part_count = sum(1 for i in range(1, 6) if f"PART {i}" in plan.upper() or f"PART {i}:" in plan.upper())
        
        if part_count < 5:
            print(f"  [Warning: Plan has only {part_count} parts, expected 5. Enhancing...]")
            # Try to add missing parts
            plan = self._enhance_plan_with_missing_parts(plan, part_count)
        
        # Clean up common formatting issues
        plan = re.sub(r'```[a-z]*\s*\n?', '', plan)  # Remove markdown code blocks
        plan = plan.strip()
        
        return plan
    
    def _enhance_plan_with_missing_parts(self, plan, current_count):
        """Adds missing parts to complete the 5-part structure."""
        missing_parts = []
        part_templates = {
            1: "PART 1: HEADER & NAVIGATION\n- Main header with branding/logo\n- Navigation menu structure\n- Search functionality (if applicable)\n- User account controls",
            2: "PART 2: HERO SECTION / MAIN CONTENT AREA\n- Primary content area layout\n- Key visual elements\n- Call-to-action components\n- Content hierarchy",
            3: "PART 3: FEATURE SECTIONS / CONTENT BLOCKS\n- Secondary content areas\n- Feature highlights\n- Information organization\n- Interactive elements",
            4: "PART 4: SIDEBAR / SUPPORTING CONTENT\n- Secondary navigation\n- Related content\n- Widgets or tools\n- Additional functionality",
            5: "PART 5: FOOTER & FINAL ELEMENTS\n- Footer structure\n- Contact information\n- Legal links\n- Social media integration"
        }
        
        for i in range(1, 6):
            if f"PART {i}" not in plan.upper():
                missing_parts.append(part_templates[i])
        
        if missing_parts:
            plan += "\n\n" + "\n\n".join(missing_parts)
        
        return plan
    
    def _generate_fallback_plan(self, task_description):
        """Generates a basic fallback plan if the API call fails."""
        return f"""PLAN FOR: {task_description}

        PART 1: HEADER & NAVIGATION
        - Main header with branding/logo area
        - Primary navigation menu
        - Search functionality
        - User account controls

        PART 2: HERO SECTION / MAIN CONTENT AREA
        - Primary content area layout
        - Key visual elements
        - Call-to-action components
        - Content hierarchy

        PART 3: FEATURE SECTIONS / CONTENT BLOCKS
        - Secondary content areas
        - Feature highlights
        - Information organization
        - Interactive elements

        PART 4: SIDEBAR / SUPPORTING CONTENT
        - Secondary navigation
        - Related content
        - Widgets or tools
        - Additional functionality

        PART 5: FOOTER & FINAL ELEMENTS
        - Footer structure
        - Contact information
        - Legal links
        - Social media integration"""

    def generate_part_tool(self, part_number, plan):
        """
        Enhanced prompt generation for creating specific parts of a web page.
        Uses structured prompting to ensure high-quality, consistent output.
        """
        print(f"  [Agent Generating Part {part_number}]")
        
        # Extract part-specific context from plan
        part_context = self._extract_part_context(plan, part_number)
        
        # Enhanced prompt with clear structure and requirements
        prompt = f"""You are an expert front-end developer. Generate Part {part_number} of a web page.

        CONTEXT FROM PLAN:
        {part_context}

        FULL PLAN REFERENCE:
        {plan}

        TECHNICAL REQUIREMENTS:
        1. Generate ONLY the HTML structure and CSS styles for Part {part_number}
        2. Use semantic HTML5: <header>, <nav>, <main>, <section>, <article>, <aside>, <footer>, etc.
        3. CSS must be wrapped in <style> tags within the component
        4. Use CSS Grid or Flexbox for layouts (prefer Grid for 2D layouts, Flexbox for 1D)
        5. Implement mobile-first responsive design with media queries
        6. Use CSS custom properties (variables) for colors, spacing, and typography
        7. Apply BEM naming convention: block__element--modifier
        8. Include smooth transitions (transition: all 0.3s ease) for interactive elements
        9. Add hover states for clickable elements
        10. Include proper ARIA attributes: aria-label, aria-labelledby, role where needed
        11. Use rem/em units for scalable typography and spacing
        12. Ensure proper color contrast (WCAG AA minimum)
        13. Include focus states for keyboard navigation

        CODE QUALITY:
        - No JavaScript code
        - No markdown code blocks (no ```html or ```)
        - No explanatory text or comments
        - Self-contained component (all styles included)
        - Valid HTML5 syntax
        - Clean, readable indentation (2 spaces)
        - Production-ready code

        OUTPUT FORMAT:
        Return ONLY the HTML code with embedded <style> tags. Start directly with the opening tag (e.g., <section>, <header>, <div>).

        Generate Part {part_number} now:"""
        
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        content = response['message']['content']
        
        # Clean up common LLM formatting issues
        content = self._clean_generated_code(content)
        print("==========content============")
        print(content)
        return content
    
    def _extract_part_context(self, plan, part_number):
        """
        Extracts the relevant section from the plan for the specific part number.
        Helps the LLM focus on the right component.
        """
        # Look for part-specific mentions in the plan
        part_keywords = {
            1: ["PART 1", "HEADER", "NAVIGATION", "header", "navigation", "logo", "menu"],
            2: ["PART 2", "HERO", "MAIN CONTENT", "hero", "main", "primary", "call-to-action"],
            3: ["PART 3", "FEATURE", "CONTENT BLOCKS", "feature", "secondary", "highlights"],
            4: ["PART 4", "SIDEBAR", "SUPPORTING", "sidebar", "widget", "related"],
            5: ["PART 5", "FOOTER", "FINAL", "footer", "contact", "legal", "social"]
        }
        
        keywords = part_keywords.get(part_number, [])
        lines = plan.split('\n')
        relevant_lines = []
        
        for i, line in enumerate(lines):
            if any(keyword.lower() in line.lower() for keyword in keywords):
                # Include this line and next few lines for context
                relevant_lines.extend(lines[max(0, i-1):min(len(lines), i+5)])
        
        if relevant_lines:
            return '\n'.join(relevant_lines[:15])  # Limit to 15 lines
        else:
            return f"Part {part_number} component based on the overall plan structure."
    
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

    # --- NEW LLM-BASED DEBUG TOOL ---
    def debug_tool(self, code):
        """Uses the LLM to scan for syntax and structural errors."""
        print("  [LLM is inspecting the code for bugs...]")
        
        prompt = f"""
        Act as a Senior Web Developer. Review the following HTML code for errors.
        If the code is valid, respond with exactly: "VALID".
        If there are errors (missing tags, broken CSS, logic flaws), respond with "ERROR:" followed by a brief instruction on how to fix it.
        
        CODE TO REVIEW:
        {code}
        """
        
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        review = response['message']['content'].strip()
        return review

    def run_recursive_logic(self, goal):
        # 1. Plan
        full_plan = self.plan_tool(goal)
        
        # 2. Generate Parts
        for i in range(1, 6):
            self.parts[i] = self.generate_part_tool(i, full_plan)
        
        # 3. Combine
        full_html = "<!DOCTYPE html>\n<html>\n" + "\n".join(self.parts.values()) + "\n</html>"
        
        # 4. LLM Debug Loop
        debug_feedback = self.debug_tool(full_html)
        
        if "ERROR" in debug_feedback.upper():
            print(f"  [Bug Found]: {debug_feedback}")
            # Recursively call the generator with the feedback to fix it
            print("  [Attempting automatic fix...]")
            prompt = f"Fix this HTML based on this feedback: {debug_feedback}\n\nHTML:\n{full_html}"
            fix_response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
            full_html = fix_response['message']['content']
        else:
            print("  [Code Verified by LLM]")

        return full_html

    def execute(self, user_goal):
        final_code = self.run_recursive_logic(user_goal)
        
        file_path = "llm_debugged_page.html"
        with open(file_path, "w") as f:
            # Clean up potential markdown formatting from LLM response
            clean_code = final_code.replace("```html", "").replace("```", "")
            f.write(clean_code)
        
        webbrowser.open(f"file://{os.path.realpath(file_path)}")

# Start
#agent = RecursiveHTMLAgent("qwen3-coder")
agent = RecursiveHTMLAgent("deepseek-coder-v2")
agent.execute("just show me a youtube.com front page")
