import re

def process_file(filename, is_front=False):
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Strip out borders radius
    content = content.replace('border-radius: 8px;', '')
    
    # 2. Consistent Header Component.
    # We will manually target the headers and replace them.
    
    # Front panel 1: Das Unternehmen
    content = re.sub(
        r'<div class="frame-col gap-8">\s*<div class="text-label">Das Unternehmen</div>\s*<h2 class="text-h1">Ihr Partner für<br>professionelles FM</h2>\s*<div class="divider navy"></div>\s*</div>',
        '<div class="frame-col gap-8">\n                    <div class="text-label">Das Unternehmen</div>\n                    <h2 class="text-h1">Ihr Partner für<br>professionelles FM</h2>\n                    <div class="divider navy"></div>\n                    <p class="text-body" style="font-size: 0.875rem; line-height: 1.4; color: var(--text-primary); margin-top: 8px;">GM Süd steht für zuverlässiges, lösungsorientiertes und erfahrenes Facility Management im Großraum München.</p>\n                    <p class="text-body" style="font-size: 0.875rem; line-height: 1.4; color: var(--text-primary); margin-top: 4px;">Wir verstehen, dass jedes Gebäude einzigartig ist... durch unser geschultes Personal.</p>\n                </div>',
        content, flags=re.DOTALL
    )
    # wait I shouldn\'t regex everything. I\'ll just string replace the chunks I know.
