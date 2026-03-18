import re

def sync_html():
    with open('src/front.html', 'r', encoding='utf-8') as f:
        front = f.read()
    with open('src/back.html', 'r', encoding='utf-8') as f:
        back = f.read()
    with open('src/canvas.html', 'r', encoding='utf-8') as f:
        canvas = f.read()
    with open('src/print.html', 'r', encoding='utf-8') as f:
        print_html = f.read()

    outer_match = re.search(r'(<section class="spread[^>]*id="outer-spread">.*?</section>)', front, re.DOTALL)
    if outer_match:
        outer_content = outer_match.group(1)
        canvas = re.sub(r'<section class="spread[^>]*id="outer-spread">.*?</section>', outer_content, canvas, flags=re.DOTALL)
        print_html = re.sub(r'<section class="spread[^>]*id="outer-spread">.*?</section>', outer_content, print_html, flags=re.DOTALL)

    inner_match = re.search(r'(<section class="spread[^>]*id="inner-spread">.*?</section>)', back, re.DOTALL)
    if inner_match:
        inner_content = inner_match.group(1)
        canvas = re.sub(r'<section class="spread[^>]*id="inner-spread">.*?</section>', inner_content, canvas, flags=re.DOTALL)
        print_html = re.sub(r'<section class="spread[^>]*id="inner-spread">.*?</section>', inner_content, print_html, flags=re.DOTALL)

    with open('src/canvas.html', 'w', encoding='utf-8') as f:
        f.write(canvas)
    with open('src/print.html', 'w', encoding='utf-8') as f:
        f.write(print_html)
    
    print("Successfully synced front.html and back.html into canvas.html and print.html!")

if __name__ == '__main__':
    sync_html()
