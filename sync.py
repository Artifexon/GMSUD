import re

def sync_files():
    # Read front and back
    with open('src/front.html', 'r', encoding='utf-8') as f:
        front = f.read()
    with open('src/back.html', 'r', encoding='utf-8') as f:
        back = f.read()

    # Extract sections
    style_match = re.search(r'<style>(.*?)</style>', front, re.DOTALL)
    style = style_match.group(1) if style_match else ''

    front_body_match = re.search(r'<body>(.*?)</body>', front, re.DOTALL)
    front_body = front_body_match.group(1).replace('<div class="spread-label">Outside (Folded Flat)</div>', '')

    back_body_match = re.search(r'<body>(.*?)</body>', back, re.DOTALL)
    back_body = back_body_match.group(1).replace('<div class="spread-label">Inside (Unfolded)</div>', '')

    # Print HTML
    print_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GM Süd GmbH – Flyer Print Ready</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>{style}</style>
</head>
<body>
    <div class="page">
        {front_body}
    </div>
    <div class="page" style="margin-top: 20px;">
        {back_body}
    </div>
</body>
</html>"""

    # Canvas HTML
    canvas_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GM Süd GmbH – Flyer Canvas</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>{style}</style>
</head>
<body>
    <div style="font-size: 14px; font-weight: 700; color: #667085; margin: 0 auto; width: var(--spread-w); text-align: left;">Outside (Folded Flat)</div>
    <div class="page">
        {front_body}
    </div>
    <div style="font-size: 14px; font-weight: 700; color: #667085; margin: 0 auto; width: var(--spread-w); text-align: left; margin-top: 40px;">Inside (Unfolded)</div>
    <div class="page">
        {back_body}
    </div>
    <script>
        document.addEventListener('keydown', (e) => {{
            if ((e.ctrlKey || e.metaKey) && e.key === 'g') {{
                e.preventDefault();
                document.body.classList.toggle('debug-grid');
            }}
        }});
    </script>
</body>
</html>"""

    with open('src/print.html', 'w', encoding='utf-8') as f:
        f.write(print_html)
    with open('src/canvas.html', 'w', encoding='utf-8') as f:
        f.write(canvas_html)

if __name__ == '__main__':
    sync_files()
