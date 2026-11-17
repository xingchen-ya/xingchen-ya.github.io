"""Draw a compact personal header; return named boxes for transparent PNG exports."""
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics

INK = colors.HexColor('#10204A')
BLUE = colors.HexColor('#164BFA')


def draw_header(c, height, assets, parts=None):
    boxes = {}
    enabled = lambda key: parts is None or key in parts

    def text(key, value, x, top, size, bold=False, color=INK, url=None, tracking=0):
        font = 'CNBold' if bold else 'CN'
        if enabled(key):
            c.setFont(font, size)
            c.setFillColor(color)
            if key == 'job-intent-text':
                prefix, rest = value.split('  ', 1)
                c.setFillColor(BLUE)
                c.drawString(x, height-top-size, prefix)
                c.setFillColor(color)
                c.drawString(x+pdfmetrics.stringWidth(prefix+'  ', font, size), height-top-size, rest)
            elif tracking:
                run = c.beginText(x, height-top-size)
                run.setFont(font, size)
                run.setCharSpace(tracking)
                run.textOut(value)
                run.setCharSpace(0)
                c.drawText(run)
            else:
                c.drawString(x, height-top-size, value)
        width = pdfmetrics.stringWidth(value, font, size) + tracking * max(0, len(value)-1)
        boxes[key] = (x-2, top-2, x+width+2, top+size+5)
        if url and enabled(key):
            c.linkURL(url, (x, height-top-size-3, x+width, height-top+2), relative=0)
        return width

    text('name', '罗洋', 36, 24, 44, True, tracking=6)
    c.setStrokeColor(colors.HexColor('#8C9AB1'))
    c.setLineWidth(.8)
    if enabled('divider-name'):
        c.line(160, height-32, 160, height-76)
    boxes['divider-name'] = (156, 29, 164, 79)
    intent = '求职意向  AI 全栈工程师 · 实习'
    badge_width = pdfmetrics.stringWidth(intent, 'CNBold', 12) + 18
    c.setFillColor(colors.HexColor('#D6E7FF'))
    if enabled('job-intent-bg'):
        c.roundRect(179, height-49, badge_width, 24, 12, fill=1, stroke=0)
    text('job-intent-text', intent, 188, 27, 12, True)
    boxes['job-intent-badge'] = (177, 23, 181+badge_width, 51)
    boxes['job-intent-bg'] = boxes['job-intent-badge']
    text('availability', '2027.07 起可到岗', 185, 55, 12)
    rows = [
        (88, [('mail', '3583418031@qq.com', 'mailto:3583418031@qq.com'),
              ('phone', '18989542495', 'tel:18989542495')]),
        (110, [('link', '个人网站  xingchen-ya.github.io', 'https://xingchen-ya.github.io/'),
               ('github', 'GitHub  github.com/xingchen-ya', 'https://github.com/xingchen-ya')]),
    ]
    for index, (top, entries) in enumerate(rows):
        x = 36
        for col, (icon, value, url) in enumerate(entries):
            if col:
                c.setStrokeColor(INK)
                c.setLineWidth(.6)
                if enabled(f'divider-row-{index+1}'):
                    c.line(x-10, height-top-2, x-10, height-top-12)
                boxes[f'divider-row-{index+1}'] = (x-13, top-1, x-7, top+14)
            if enabled(f'icon-{icon}'):
                c.drawImage(ImageReader(str(assets / f'icon-{icon}.png')),
                            x, height-top-13, width=13, height=13, mask='auto')
            width = text(f'text-{icon}', value, x+21, top, 10.8, url=url)
            x += 21+width+27
        if x-27 > 563:
            raise ValueError('Header contact row exceeds printable width')
        boxes[f'contact-row-{index+1}'] = (33, top-2, x-25, top+17)
    return boxes
