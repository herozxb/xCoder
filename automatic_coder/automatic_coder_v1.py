import webbrowser
import os

class SimpleAgent:
    def __init__(self, model_name):
        self.model_name = model_name

    # Define a method for code generation in parts
    def plan_html_code(self):
        return """
        1. Part 1: HTML structure - Define the basic HTML skeleton.
        2. Part 2: Head section - Add meta tags, title, and link to stylesheets.
        3. Part 3: Body section - Create content like headings, paragraphs, and buttons.
        4. Part 4: Add styles - Implement simple CSS for layout and color.
        5. Part 5: Debugging - Run and check for errors.
        """

    def generate_html_part(self, part):
        # Based on the part requested, return the generated HTML code
        if part == 1:
            return "<!DOCTYPE html><html lang='en'>\n<head>\n</head>\n<body>\n</body>\n</html>"
        elif part == 2:
            return "<head>\n<meta charset='UTF-8'>\n<title>My Simple Page</title>\n</head>"
        elif part == 3:
            return "<body>\n<h1>Welcome to My Simple HTML Page</h1>\n<p>This is a paragraph.</p>\n</body>"
        elif part == 4:
            return "<style>\nbody { font-family: Arial, sans-serif; background-color: lightblue; }\nh1 { color: darkblue; }\n</style>"
        elif part == 5:
            return "Running the HTML... Debugging..."

    def combine_html_parts(self, parts):
        # Combine all parts into a complete HTML document
        full_html = "<!DOCTYPE html>\n<html lang='en'>\n"
        for part in parts:
            full_html += part + "\n"
        full_html += "</html>"
        return full_html

    def debug_html(self, html_code):
        # Check if HTML code has any obvious issues, e.g., missing closing tags
        if "<head>" not in html_code or "<body>" not in html_code:
            return "Error: Missing head or body section."
        return "HTML code looks good!"

    def run(self):
        # Plan the HTML code and generate each part
        print("Planning the HTML code...\n")
        plan = self.plan_html_code()
        print(plan)

        print("\nGenerating each part...\n")
        parts = []
        for i in range(1, 5):
            part_code = self.generate_html_part(i)
            print(f"Generated part {i}:\n{part_code}\n")
            parts.append(part_code)

        # Combine all parts
        full_html = self.combine_html_parts(parts)
        print(f"Full HTML generated:\n{full_html}\n")

        # Debug the HTML code
        print("Running the HTML and debugging...\n")
        debug_result = self.debug_html(full_html)
        print(debug_result)

        # Repeat until successful
        while "Error" in debug_result:
            print("\nFixing the issue...\n")
            # Here, we can simply simulate fixing an issue by generating a correct part and re-running
            parts[1] = self.generate_html_part(2)  # Let's assume a fix was made in part 2 for simplicity
            full_html = self.combine_html_parts(parts)
            debug_result = self.debug_html(full_html)
            print(f"Fixed HTML: {full_html}")
            print(debug_result)

        print("\nHTML successfully generated and running!")

        # Save the HTML to a file
        file_path = "generated_page.html"
        with open(file_path, "w") as file:
            file.write(full_html)

        # Open the HTML file in the default browser
        webbrowser.open(f"file://{os.path.realpath(file_path)}")

        return full_html


# Initialize the agent with the model (for simplicity, we're not using the model here directly)
agent = SimpleAgent("deepseek-coder-v2")

# Run the agent to generate and debug the HTML page
agent.run()
