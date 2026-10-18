import os
import re

def remove_google_analytics(directory):
    # Regex to match the full Google Analytics script block (gtag.js)
    # Matches from <script async src="https://www.googletagmanager.com/...> up to the closing </script>
    # and handles inline initialization configs as well.
    ga_script_pattern = re.compile(
        r'<script[^>]*src=["\']https://www\.googletagmanager\.com/gtag/js\?id=[^"\']+["\'][^>]*>.*?</script>',
        re.DOTALL | re.IGNORECASE
    )
    
    # Regex to match the inline gtag config block (e.g., gtag('config', 'G-XXXXXXXXXX');)
    ga_config_pattern = re.compile(
        r'<script[^>]*>\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];\s*function\s*gtag\([^)]*\)\s*\{[^}]*\}\s*gtag\([^)]+\);\s*</script>',
        re.DOTALL | re.IGNORECASE
    )
    
    # Alternative simpler pattern for generic gtag config snippets
    gtag_inline_pattern = re.compile(
        r'<script[^>]*>.*?(?:gtag\(\s*[\'"]config[\'"]\s*,\s*[\'"][GU]A-[^\'"]+[\'"]\s*\)).*?</script>',
        re.DOTALL | re.IGNORECASE
    )

    modified_files = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.html', '.htm', '.php')):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original_content = content

                # Apply regex replacements
                content = ga_script_pattern.sub('', content)
                content = ga_config_pattern.sub('', content)
                content = gtag_inline_pattern.sub('', content)

                # If changes were made, write the cleaned content back
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"[Removed GA] Cleaned: {file_path}")
                    modified_files += 1

    print(f"\nCleanup complete. Modified {modified_files} file(s).")

if __name__ == "__main__":
    # Specify the root directory of your website project
    target_directory = input("Enter the path to your website directory: ").strip()
    
    if os.path.isdir(target_directory):
        remove_google_analytics(target_directory)
    else:
        print("Invalid directory path. Please try again.")
