import os

# Your official Google Analytics tracking snippet
GA_SNIPPET = """
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-R0WMWNF4NZ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-R0WMWNF4NZ');
  </script>
"""

def inject_analytics():
    root_dir = "."
    count = 0
    for subdir, dirs, files in os.walk(root_dir):
        # Skip hidden directories like .git and .github
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(subdir, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check if GA ID is already present to avoid duplicate injection
                if "G-R0WMWNF4NZ" not in content:
                    if "</head>" in content:
                        # Insert right before </head>
                        content = content.replace("</head>", f"{GA_SNIPPET}\n</head>")
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(content)
                        print(f"Injected GA into: {filepath}")
                        count += 1
                    else:
                        print(f"Skipped (no </head> found): {filepath}")
                else:
                    print(f"Already tracked: {filepath}")
                    
    print(f"\nDone! Google Analytics successfully added to {count} files.")

if __name__ == "__main__":
    inject_analytics()
