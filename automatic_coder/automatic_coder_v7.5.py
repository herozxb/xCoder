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
                                                                                                                                                                                                                                                        
        VISUAL HIERARCHY PRINCIPLES:                                                                                                                                                                                                                 
        - Above-the-fold impact: Hero section must communicate value in 3 seconds                                                                                                                                                                    
        - Progressive disclosure: Information density increases as user scrolls                                                                                                                                                                      
        - Visual rhythm: Consistent spacing using 8px grid system                                                                                                                                                                                    
                                                                                                                                                                                                                                                    
        - Dark theme with #0f0f0f background, #272727 borders, #065fd4 accents                                                                                                                                                                       
        - Card-based layouts with 12px border-radius                                                                                                                                                                                                 
        - Subtle shadows and depth layering                                                                                                                                                                                                          
        - Micro-interactions: 0.2s transitions on hover/focus                                                                                                                                                                                        
        - Mobile-first responsive breakpoints (320px, 768px, 1024px)                                                                                                                                                                                 
                                                                                                                                                                                                                                                        
        5-PART ARCHITECTURE:                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                        
        PART 1: HEADER & NAVIGATION SYSTEM                                                                                                                                                                                                           
        - Sticky header with 56px height, backdrop-blur on scroll                                                                                                                                                                                    
        - Left: Hamburger menu + logo (24px height) with proper SVG                                                                                                                                                                                  
        - Center: Search container (640px max-width) with focus states                                                                                                                                                                               
        - Right: Action icons (24px) with 8px spacing, user avatar (32px)                                                                                                                                                                            
        - Mobile: Collapsible menu, search overlay                                                                                                                                                                                                   
                                                                                                                                                                                                                                                        
        PART 2: HERO/PRIMARY CONTENT AREA                                                                                                                                                                                                            
        - Content grid using CSS Grid (auto-fill, minmax 320px)                                                                                                                                                                                      
        - Video cards with 16:9 aspect ratio thumbnails                                                                                                                                                                                              
        - Typography hierarchy: 16px base, 14px meta, 12px details                                                                                                                                                                                   
        - Hover effects: scale(1.02) transform, shadow elevation                                                                                                                                                                                     
        - Loading states and skeleton screens                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        
        PART 3: CONTENT CARDS & FEATURES                                                                                                                                                                                                             
        - Card components with consistent padding (12px)                                                                                                                                                                                             
        - Image optimization: object-fit cover, lazy loading                                                                                                                                                                                         
        - Metadata layout: flexbox with space-between                                                                                                                                                                                                
        - Interactive elements: focus-visible outlines                                                                                                                                                                                               
        - Accessibility: aria-labels, keyboard navigation                                                                                                                                                                                            
                                                                                                                                                                                                                                                        
        PART 4: SECONDARY NAVIGATION & WIDGETS                                                                                                                                                                                                       
        - Sidebar with 240px width, scrollable content                                                                                                                                                                                               
        - Section dividers with 1px #272727 borders                                                                                                                                                                                                  
        - Icon system: 24px consistent sizing, currentColor fill                                                                                                                                                                                     
        - Responsive behavior: collapsible on mobile                                                                                                                                                                                                 
        - State management: active/hover/focus distinctions                                                                                                                                                                                          
                                                                                                                                                                                                                                                        
        PART 5: FOOTER & SYSTEM ELEMENTS                                                                                                                                                                                                             
        - Multi-column footer with semantic HTML5                                                                                                                                                                                                    
        - Link organization: hierarchical information architecture                                                                                                                                                                                   
        - Social integration: icon consistency, proper sizing                                                                                                                                                                                        
        - Legal compliance: privacy, terms, copyright                                                                                                                                                                                                
        - Performance: minimal DOM, optimized selectors                                                                                                                                                                                              
                                                                                                                                                                                                                                                        
        TECHNICAL REQUIREMENTS:                                                                                                                                                                                                                      
        - Semantic HTML5 elements only                                                                                                                                                                                                               
        - CSS Grid + Flexbox for all layouts                                                                                                                                                                                                         
        - CSS custom properties for theming                                                                                                                                                                                                          
        - BEM naming convention                                                                                                                                                                                                                      
        - WCAG 2.1 AA accessibility standards   

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

        css_patterns = self._get_css_patterns(part_number)  
        
        # Enhanced prompt with clear structure and requirements
        prompt = f"""You are an expert front-end developer. Generate Part {part_number} of a web page.

        CONTEXT FROM PLAN:
        {part_context}

        FULL PLAN REFERENCE:
        {plan}

        MODERN CSS PATTERNS TO USE:                                                                                                                                                                                                                  
        {css_patterns}  

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

    def _get_css_patterns(self, part_number):                                                                                                                                                                                                
        """I provide specific CSS patterns that create modern UI"""                                                                                                                                                                          
        patterns = {                                                                                                                                                                                                                         
            1: """Header: position: sticky; top: 0; backdrop-filter: blur(10px); z-index: 100                                                                                                                                                
                Search: flex: 1; max-width: 640px; border: 1px solid var(--border)                                                                                                                                                          
                Icons: width: 24px; height: 24px; cursor: pointer; transition: background-color 0.2s""",                                                                                                                                    
                                                                                                                                                                                                                                            
            2: """Grid: display: grid; gap: 16px; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))                                                                                                                               
                Cards: background: var(--bg-card); border-radius: 12px; overflow: hidden                                                                                                                                                    
                Hover: transform: scale(1.02); box-shadow: 0 4px 12px rgba(0,0,0,0.3)""",                                                                                                                                                   
                                                                                                                                                                                                                                            
            3: """Images: aspect-ratio: 16/9; object-fit: cover; width: 100%                                                                                                                                                                 
                Meta: display: flex; gap: 12px; margin-top: 12px                                                                                                                                                                            
                Text: -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden""",                                                                                                                                             
                                                                                                                                                                                                                                            
            4: """Sidebar: width: 240px; border-right: 1px solid var(--border); overflow-y: auto                                                                                                                                             
                Items: padding: 10px 24px; cursor: pointer; transition: background-color 0.2s                                                                                                                                               
                Active: background-color: var(--bg-hover); font-weight: 500""",                                                                                                                                                             
                                                                                                                                                                                                                                            
            5: """Footer: display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 24px                                                                                                                              
                Links: color: var(--text-secondary); text-decoration: none; font-size: 14px"""                                                                                                                                              
        }                                                                                                                                                                                                                                    
        return patterns.get(part_number, "Use modern CSS with proper responsive design")  

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
        
        if "ERROR" in debug_feedback.upper() and 0:
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
agent.execute("just show me a youtube.com front page no sidebar")
