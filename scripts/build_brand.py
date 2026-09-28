"""Rebuild the editable brand marks and bilingual README banners (stdlib only)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs' / 'assets'
INK = '#173F35'
PAPER = '#F6F4ED'
SAGE = '#AAB9A3'
BLUE = '#D9E7FB'
CLAY = '#BC7356'


def logo():
    return f'''<path d="M14 0H77L112 35V118Q112 132 98 132H14Q0 132 0 118V14Q0 0 14 0Z" fill="{INK}"/>
<path d="M77 0V28Q77 35 84 35H112" fill="none" stroke="{PAPER}" stroke-width="4"/>
<rect x="18" y="48" width="32" height="30" rx="4" fill="{SAGE}"/>
<rect x="60" y="48" width="32" height="30" rx="4" fill="{BLUE}"/>
<rect x="18" y="88" width="32" height="30" rx="4" fill="{CLAY}"/>
<rect x="60" y="88" width="32" height="30" rx="4" fill="{SAGE}"/>'''


def rules(y, count, width=130, color=SAGE):
    return ''.join(f'<path d="M24 {y+i*16}h{width if i%3 != 2 else width-25}" stroke="{color}" stroke-width="5"/>' for i in range(count))


def sheet(x, y, angle, kind):
    content = f'<path d="M24 30h132" stroke="{INK}" stroke-width="6"/>'
    if kind == 'writing':
        content += rules(59, 5) + rules(173, 5)
        content += f'<path d="M20 101h76M20 106h58M17 165H10v95h7" fill="none" stroke="{CLAY}" stroke-width="3"/>'
        content += f'<ellipse cx="128" cy="145" rx="30" ry="13" fill="none" stroke="{CLAY}" stroke-width="3" transform="rotate(-12 128 145)"/>'
    elif kind == 'figures':
        content += f'<path d="M24 145V64M24 145h132" stroke="{INK}" fill="none" stroke-width="2"/>'
        for pts, color in [('32,128 57,102 82,108 112,78 147,65',INK),('32,135 57,126 82,120 112,114 147,93','#95B4C8')]:
            content += f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3"/>'
            for point in pts.split():
                cx,cy=point.split(',');content += f'<circle cx="{cx}" cy="{cy}" r="4" fill="{color}"/>'
        content += f'<rect x="24" y="178" width="132" height="90" fill="none" stroke="{INK}" stroke-width="1.2"/><rect x="24" y="178" width="132" height="22" fill="{SAGE}"/>'
        content += ''.join(f'<path d="M24 {a}h132" stroke="{SAGE}"/>' for a in (200,223,246))
        content += ''.join(f'<path d="M{a} 178v90" stroke="{SAGE}"/>' for a in (77,118))
    elif kind == 'review':
        content += rules(59, 13)
        content += f'<circle cx="106" cy="151" r="48" fill="{PAPER}" stroke="{INK}" stroke-width="7"/>'
        content += ''.join(f'<path d="M77 {a}h56" stroke="{BLUE}" stroke-width="7"/>' for a in (130,150,170))
        content += f'<path d="M141 190l29 33" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
    else:
        for j in range(4):
            yy=66+j*54
            content += f'<rect x="24" y="{yy}" width="24" height="24" fill="none" stroke="{INK}" stroke-width="2"/><path d="M29 {yy+12}l5 5 10-12" stroke="{INK}" stroke-width="2.5" fill="none"/>'
            content += f'<path d="M60 {yy+5}h58M60 {yy+16}h44" stroke="{SAGE}" stroke-width="4"/>'
            content += f'<rect x="133" y="{yy}" width="24" height="24" rx="2" fill="{[SAGE,BLUE,CLAY,"#DFAE36"][j]}"/>'
    return f'<g transform="translate({x} {y}) rotate({angle} 90 145)"><rect x="5" y="7" width="180" height="294" rx="2" fill="{INK}" opacity=".08"/><rect width="180" height="294" rx="2" fill="#FFFEF9" stroke="{INK}" stroke-width="1.2"/>{content}</g>'


def banner(lang):
    zh=lang=='zh-CN'
    title='学术论文技能集' if zh else 'Academic Paper Skills'
    subtitle='从证据到论文' if zh else 'From evidence to manuscript'
    head=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="480" viewBox="0 0 1440 480" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">Four manuscript pages represent writing, figures and tables, review, and evidence-based requirements. Decorative charts do not represent research results.</desc>
<rect width="1440" height="480" rx="16" fill="{PAPER}"/>
<g transform="translate(68 54) scale(.7)">{logo()}</g>
<text x="168" y="102" fill="{INK}" font-family="Arial, sans-serif" font-size="14" letter-spacing="3">FOUR SKILLS. ONE WORKFLOW.</text>'''
    if zh:
        head += f'<text x="65" y="241" fill="{INK}" font-family="PingFang SC, Noto Serif CJK SC, serif" font-size="51" font-weight="600">学术论文技能集</text>'
        head += f'<text x="68" y="282" fill="{INK}" font-family="Georgia, serif" font-size="25">Academic Paper Skills</text>'
    else:
        head += f'<text x="65" y="230" fill="{INK}" font-family="Georgia, Times New Roman, serif" font-size="61">Academic</text><text x="65" y="296" fill="{INK}" font-family="Georgia, Times New Roman, serif" font-size="61">Paper Skills</text>'
    head += f'<text x="68" y="344" fill="#526A5D" font-family="Arial, PingFang SC, sans-serif" font-size="23">{subtitle}</text>'
    labels='写作 · 图表 · 审阅 · 规范' if zh else 'WRITE  /  VISUALIZE  /  REVIEW  /  VALIDATE'
    head += f'<path d="M68 382h425" stroke="#D5D9CF"/><text x="68" y="413" fill="#526A5D" font-family="Arial, PingFang SC, sans-serif" font-size="13" letter-spacing="1">{labels}</text>'
    head += f'<path d="M595 398h773" stroke="#D5D9CF" stroke-width="2"/>'
    for data in [(596,82,-5,'writing'),(787,75,-2,'figures'),(978,82,2,'review'),(1170,91,5,'policy')]: head+=sheet(*data)
    head += '</svg>\n'
    return head


def main():
    ASSETS.mkdir(parents=True,exist_ok=True)
    (ASSETS/'logo.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="144" height="160" viewBox="-16 -14 144 160" role="img" aria-labelledby="title"><title id="title">Academic Paper Skills logo</title>{logo()}</svg>\n')
    for lang in ('en','zh-CN'):
        (ASSETS/f'hero-{lang}.svg').write_text(banner(lang))
    print('Built logo.svg and two localized, editable SVG banners.')


if __name__=='__main__':
    main()
