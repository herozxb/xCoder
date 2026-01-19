import webbrowser
import os
import ollama
import re

class RecursiveHTMLAgent:
    def __init__(self, model_name):
        self.model_name = model_name
        self.parts = {}

    def plan_tool(self, task_description):
        print(f"  [Agent Planning: {task_description}]")
        prompt = f"Create a 5-step structural plan for: {task_description}. No code yet, just logic."
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']

    def generate_part_tool(self, part_number, plan):
        print(f"  [Agent Generating Part {part_number}]")
        prompt = f"Based on this plan: {plan}\n\nWrite only the HTML/CSS for step {part_number}. No talk, no markdown."
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']

    # --- NEW LLM-BASED DEBUG TOOL ---
    def debug_tool(self, code):
        """Uses the LLM to scan for syntax and structural errors."""
        print("  [LLM is inspecting the code for bugs...]")
        
        prompt = f"""
        Act as a Senior Web Developer. Review the following HTML code for errors. No talk, no markdown.
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
        print("=================full_plan===================")
        print(full_plan)
        
        # 2. Generate Parts
        for i in range(1, 6):
            self.parts[i] = self.generate_part_tool(i, full_plan)
            print("=================[{i}]===================")
            print(self.parts[i])
        
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
agent = RecursiveHTMLAgent("deepseek-coder-v2")
agent.execute("just show me a robot dancing page")