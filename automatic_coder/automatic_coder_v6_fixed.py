import webbrowser
import os
import ollama
import re
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RecursiveHTMLAgent:
    def __init__(self, model_name):
        self.model_name = model_name
        self.parts = {}

    def _safe_ollama_call(self, prompt: str, operation_name: str, timeout: int = 180, max_retries: int = 5) -> str:
        """
        Safe wrapper for ollama calls with retry logic and timeout handling.
        
        Args:
            prompt: The prompt to send to the model
            operation_name: Name of the operation for logging
            timeout: Timeout in seconds for each attempt (default 180s / 3 minutes)
            max_retries: Maximum number of retry attempts (default 5)
        
        Returns:
            The response content from ollama
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries} for {operation_name}")
                
                # Add timeout to the ollama call
                response = ollama.chat(
                    model=self.model_name, 
                    messages=[{"role": "user", "content": prompt}],
                    timeout=timeout
                )
                logger.info(f"Successfully completed {operation_name}")
                return response['message']['content']
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {operation_name}: {str(e)}")
                
                if attempt == max_retries - 1:
                    logger.error(f"All {max_retries} attempts failed for {operation_name}")
                    raise Exception(f"Failed to complete {operation_name} after {max_retries} attempts: {str(e)}")
                
                # Wait before retrying (exponential backoff)
                wait_time = (2 ** attempt) + (attempt * 0.5)
                logger.info(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        # This should never be reached, but just in case
        raise Exception(f"Unexpected error in {operation_name}")

    def plan_tool(self, task_description):
        """
        Enhanced planning tool that creates a structured 5-part plan for web page development.
        Each part corresponds to a specific component of the web page architecture.
        Includes timeout handling and retry logic.
        """
        print(f"  [Agent Planning: {task_description}]")
        
        prompt = f"""
        You are a senior web architect planning the structure of a web page.
        
        TASK: Create a detailed 5-part structural plan for: {task_description}
        
        WEB PAGE ARCHITECTURE REQUIREMENTS:
        The plan must be divided into exactly 5 parts, each representing a specific component:
        
        PART 1: HEADER & NAVIGATION
        - Main header with branding/logo
        - Navigation menu structure
        - Search functionality (if applicable)
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
        - Social media integration
        
        PLANNING REQUIREMENTS:
        1. Each part must be clearly numbered and described
        2. Focus on structure and layout, not specific code
        3. Consider responsive design principles
        4. Include accessibility considerations
        5. Ensure logical flow between parts
        6. Account for user experience and navigation
        7. Plan for scalability and maintainability
        
        OUTPUT FORMAT:
        Return a structured plan with exactly 5 parts, clearly labeled.
        Use bullet points for each component within each part.
        Do not include any HTML or CSS code.
        
        Create the 5-part plan for: {task_description}
        """
        
        return self._safe_ollama_call(prompt, "plan_tool")

    def generate_part_tool(self, part_number, plan):
        """
        Enhanced prompt generation for creating specific parts of a web page.
        Uses structured prompting to ensure high-quality, consistent output.
        Includes timeout handling and retry logic.
        """
        print(f"  [Agent Generating Part {part_number}]")
        
        # Enhanced prompt with clear structure and requirements
        prompt = f"""
        You are a senior front-end developer creating a specific part of a web page.
        
        PLAN OVERVIEW: {plan}
        
        TASK: Generate Part {part_number} of the web page.
        
        REQUIREMENTS:
        1. Focus ONLY on the specific component for this part number
        2. Use semantic HTML5 elements where appropriate
        3. Include modern CSS with flexbox/grid for layout
        4. Ensure responsive design (mobile-first approach)
        5. Add appropriate ARIA labels for accessibility
        6. Use meaningful class names (BEM methodology preferred)
        7. Include hover effects and smooth transitions
        8. No JavaScript - HTML and CSS only
        9. No markdown formatting in output
        10. No explanations or comments in the code
        
        OUTPUT FORMAT:
        - Return ONLY the HTML and CSS code
        - Wrap CSS in <style> tags
        - Use <section> or <div> as appropriate for the component
        - Ensure the code is production-ready and follows best practices
        
        Generate the code for Part {part_number}:
        """
        
        return self._safe_ollama_call(prompt, f"generate_part_{part_number}")

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
        
        return self._safe_ollama_call(prompt, "debug_tool")

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
            fix_response = self._safe_ollama_call(prompt, "debug_fix")
            full_html = fix_response
        else:
            print("  [Code Verified by LLM]")

        return full_html

    def execute(self, user_goal):
        try:
            final_code = self.run_recursive_logic(user_goal)
            
            file_path = "llm_debugged_page.html"
            with open(file_path, "w") as f:
                # Clean up potential markdown formatting from LLM response
                clean_code = final_code.replace("```html", "").replace("```", "")
                f.write(clean_code)
            
            webbrowser.open(f"file://{os.path.realpath(file_path)}")
            print("Successfully generated and opened the web page!")
            
        except Exception as e:
            logger.error(f"Error during execution: {str(e)}")
            print(f"An error occurred: {str(e)}")
            print("Please check your ollama server connection and try again.")

# Start
if __name__ == "__main__":
    # Create agent with longer timeout and retry logic
    agent = RecursiveHTMLAgent(model_name="qwen3-coder")
    agent.execute("just show me a youtube.com front page")