import webbrowser
import os
import ollama
import re

class RecursiveHTMLAgent:
    def __init__(self, model_name):
        self.model_name = model_name
        self.parts = {}

    # --- STRUCTURAL TOOLS (Replacing Math Tools) ---

    def plan_tool(self, task_description):
        """Asks the LLM to provide a step-by-step plan."""
        print(f"  [Agent Planning: {task_description}]")
        prompt = f"Create a 5-part plan to build this website: {task_description}. Output only the plan."
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']

    def generate_part_tool(self, part_number, description):
        """Generates specific HTML/CSS code for a single part."""
        print(f"  [Agent Generating Part {part_number}: {description}]")
        prompt = f"Write only the code for Part {part_number} of a website based on this: {description}. No markdown."
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']

    def debug_tool(self, code):
        """Checks for missing structural tags."""
        print("  [Agent Debugging...]")
        if "<head>" not in code or "<body>" not in code:
            return "Error: Missing head or body section."
        return "Success: Code looks valid."

    # --- RECURSIVE REASONING ENGINE ---

    def run_recursive_logic(self, goal):
        # 1. Plan
        full_plan = self.plan_tool(goal)
        print(f"\nPLAN GENERATED:\n{full_plan}\n")

        # 2. Recursive Generation (Looping through the 5 parts)
        for i in range(1, 6):
            # We "pass" the plan context to the generator
            self.parts[i] = self.generate_part_tool(i, full_plan)
        
        # 3. Combine
        full_html = "<!DOCTYPE html>\n<html>\n" + "\n".join(self.parts.values()) + "\n</html>"
        
        # 4. Debug & Fix Loop
        debug_status = self.debug_tool(full_html)
        if "Error" in debug_status:
            print(f"ALERT: {debug_status} Re-generating structure...")
            self.parts[1] = "<head><title>Fixed Page</title></head>"
            self.parts[2] = "<body>"
            self.parts[5] = "</body>"
            full_html = "<!DOCTYPE html>\n<html>\n" + "\n".join(self.parts.values()) + "\n</html>"

        return full_html

    def execute(self, user_goal):
        # Generate the file
        final_code = self.run_recursive_logic(user_goal)
        
        file_path = "recursive_generated_page.html"
        with open(file_path, "w") as f:
            f.write(final_code)
        
        print(f"\nFinal HTML saved to {file_path}")
        webbrowser.open(f"file://{os.path.realpath(file_path)}")

# --- START ---
agent = RecursiveHTMLAgent("deepseek-coder-v2")
agent.execute("A futuristic robotics portfolio page with a dark theme")