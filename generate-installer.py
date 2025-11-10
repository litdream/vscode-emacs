import os
import json

# --- Configuration ---
# Define the files you want to include in the single HTML installer.
# NOTE: The path for 'extension.js' assumes you have compiled your TypeScript
# to JavaScript inside an 'out' directory, which is standard for VS Code extensions.
#
# Gemini + Claude Generated:
# TODO: Test in a separate VSCode
#

EXTENSION_FILES_TO_PACKAGE = [
    {"name": "package.json", "path": "package.json"},
    {"name": "extension.js", "path": "out/extension.js"},
    {"name": "README.md", "path": "README.md"},
]
OUTPUT_FILENAME = "final_extension_installer.html"
# ---------------------

def escape_js_string(content):
    """
    Escapes content for safe embedding within a JavaScript multi-line template literal (backticks `).
    Note: Python triple backticks are handled by wrapping the content in a raw string literal (r'...')
    to prevent unintended escape sequences.
    """
    # 1. Escape the backtick character itself, as it is the delimiter for JS template literals.
    content = content.replace('`', '\\`')
    # 2. Escape backslashes, important for paths and regex in the code.
    content = content.replace('\\', '\\\\')
    # 3. Escape ${ for interpolation within the JS template literal (if needed, though typically harmless)
    content = content.replace('${', '\\${')
    return content.strip()

def generate_extension_installer():
    """Reads extension files, builds the JS array string, and injects it into the HTML template."""
    
    # 1. Read files and build the JavaScript array content string
    js_array_items = []
    
    print("Reading extension files:")
    
    for file_info in EXTENSION_FILES_TO_PACKAGE:
        file_path = file_info["path"]
        file_name = file_info["name"]
        
        if not os.path.exists(file_path):
            print(f"Error: File not found at path: {file_path}")
            print("Please ensure you are running this script from your extension project root.")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Prepare content for embedding inside the JS template literal using raw string quotes (r'...')
            escaped_content = escape_js_string(content)
            
            js_item = f"""
            {{
                name: "{file_name}",
                content: `
{escaped_content}
                `
            }}
            """
            js_array_items.append(js_item)
            print(f"  - Successfully read {file_path}")
            
        except Exception as e:
            print(f"An error occurred while reading {file_path}: {e}")
            return
            
    # Combine all file objects into a single JS array string
    js_array_content = ",\n".join(js_array_items)

    # 2. Define the HTML template structure
    # This template is based on the 'extension_installer.html' you have been using.
    HTML_TEMPLATE = r"""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VS Code Extension Source Installer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7f7f7;
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
        }
        .file-block {
            background-color: #1f2937; /* Dark gray for code background */
            color: #d1d5db; /* Light gray text */
            border-radius: 0.5rem;
            overflow: hidden;
        }
        .file-header {
            background-color: #4b5563; /* Medium gray header */
            color: white;
            padding: 0.75rem 1rem;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .code-area {
            padding: 1rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: monospace;
            font-size: 0.875rem;
            line-height: 1.4;
        }
        .copy-btn {
            padding: 0.5rem 1rem;
            border-radius: 0.375rem;
            transition: background-color 0.15s;
        }
    </style>
</head>
<body class="p-4 sm:p-8 flex justify-center">
    <div class="container w-full">
        <header class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800">VS Code Extension Installer (Text-Only Transfer)</h1>
            <p class="text-gray-600 mt-2">Use this utility in your air-gapped environment to re-create the extension files.</p>
        </header>

        <div id="status" class="mb-6 p-4 rounded-lg bg-blue-100 border border-blue-300 text-blue-800 hidden"></div>

        <!-- Utility Section -->
        <div class="bg-white p-6 rounded-xl shadow-lg mb-8">
            <h2 class="text-2xl font-semibold mb-4 text-gray-700">Rebuilding Instructions</h2>
            <ol class="list-decimal list-inside space-y-3 text-gray-700">
                <li>On the secured machine, open this **HTML file in any browser**.</li>
                <li>For each file block below, click the **"Copy"** button.</li>
                <li>In your air-gapped VS Code environment, create a new folder (e.g., \`my-extension\`).</li>
                <li>Inside that folder, create the corresponding file (e.g., \`package.json\`) and **paste the content**.</li>
                <li>Once all files are created, open the folder in VS Code and use the **Run and Debug** view to launch the extension.</li>
            </ol>
        </div>

        <div id="files-container" class="space-y-6">
            <!-- File blocks will be generated here by JavaScript -->
        </div>
    </div>

    <script>
        // --- Extension Source Code Storage ---
        // This array is dynamically populated by the Python script with your local file content.
        const extensionFiles = [
{js_array_content}
        ];
        // --- End Extension Source Code Storage ---

        const container = document.getElementById('files-container');
        const status = document.getElementById('status');

        function showStatus(message, isError = false) {
            status.textContent = message;
            status.className = `mb-6 p-4 rounded-lg ${isError ? 'bg-red-100 border-red-300 text-red-800' : 'bg-green-100 border-green-300 text-green-800'}`;
            status.style.display = 'block';
            setTimeout(() => {
                status.style.display = 'none';
            }, 3000);
        }

        function copyToClipboard(text) {
            // Use document.execCommand('copy') for better compatibility in iFrames/strict environments
            try {
                const textarea = document.createElement('textarea');
                textarea.value = text.trim();
                textarea.style.position = 'fixed';
                textarea.style.left = '-9999px';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                showStatus(`Successfully copied ${text.substring(0, 15)}... to clipboard!`);
            } catch (err) {
                showStatus('Error copying text. Please select and copy manually.', true);
                console.error('Copy error:', err);
            }
        }

        extensionFiles.forEach(file => {
            // Trim leading/trailing whitespace and remove initial newline from template literal
            const cleanContent = file.content.trim();

            const fileBlock = document.createElement('div');
            fileBlock.className = 'file-block shadow-xl';

            // Encode content to base64 for safe transfer in the data attribute, and decode it before copying.
            fileBlock.innerHTML = `
                <div class="file-header">
                    <span>${file.name}</span>
                    <button
                        class="copy-btn bg-blue-500 hover:bg-blue-600 text-white font-semibold"
                        data-content="${btoa(cleanContent)}"
                    >
                        Copy
                    </button>
                </div>
                <!-- Display content in the pre tag, escaping HTML characters for safety -->
                <pre class="code-area">${cleanContent.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>
            `;

            container.appendChild(fileBlock);
        });

        // Add event listeners for copy buttons
        container.addEventListener('click', (e) => {
            const button = e.target.closest('.copy-btn');
            if (button) {
                // Decode the base64 content for copying
                const base64Content = button.getAttribute('data-content');
                const decodedContent = atob(base64Content);
                copyToClipboard(decodedContent);
            }
        });
    </script>
</body>
</html>
    """
    
    # 3. Write the final HTML file
    try:
        # Replace the placeholder in the raw string template
        final_html = HTML_TEMPLATE.replace('{js_array_content}', js_array_content)

        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        print("-" * 50)
        print(f"Success! Your air-gapped installer is ready:")
        print(f"File: {OUTPUT_FILENAME}")
        print("Transfer this file (as pure text) to your secured network.")
        print("-" * 50)
        
    except Exception as e:
        print(f"An error occurred while writing the output file: {e}")


if __name__ == "__main__":
    generate_extension_installer()
