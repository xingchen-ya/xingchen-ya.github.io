"""Vector project pages matching the approved blue reference compositions."""
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph

BLUE = colors.HexColor("#164BFA")
INK = colors.HexColor("#0A173E")
WHITE = colors.white


def gradient(r, x, top, width, height, radius=10):
    c = r.pdf
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, r.h - top - height, width, height, radius)
    c.clipPath(p, stroke=0, fill=0)
    c.linearGradient(x, 0, x + width, 0,
                     [colors.HexColor("#F2F7FF"), colors.HexColor("#E0EEFF")])
    c.restoreState()


def accents(r):
    c = r.pdf
    for points, fill in [
        ([(r.w-120, r.h), (r.w-65, r.h), (r.w-125, r.h-105), (r.w-180, r.h-105)], "#DCE9FF"),
        ([(r.w-62, r.h), (r.w, r.h), (r.w-70, r.h-110), (r.w-130, r.h-110)], "#8BB3FF"),
    ]:
        p = c.beginPath()
        for i, point in enumerate(points):
            (p.moveTo if i == 0 else p.lineTo)(*point)
        p.close()
        c.saveState()
        c.clipPath(p, stroke=0, fill=0)
        c.linearGradient(0, r.h, 0, r.h-115,
                         [colors.HexColor(fill), colors.HexColor("#FFFFFF")])
        c.restoreState()


def text(r, value, x, top, width, *, size=12, leading=19, bold=False, color=INK):
    style = ParagraphStyle("reference", fontName="CNBold" if bold else "CN",
                           fontSize=size, leading=leading, textColor=color, wordWrap="CJK")
    p = Paragraph(escape(value), style)
    _, height = p.wrap(width, r.h)
    p.drawOn(r.pdf, x, r.h - top - height)
    return height


def label(r, title, top):
    from reportlab.pdfbase import pdfmetrics
    width = pdfmetrics.stringWidth(title, "CNBold", 13.5) + 26
    c = r.pdf
    bottom = r.h - top - 22
    p = c.beginPath()
    for i, point in enumerate([(24, bottom), (24+width-8, bottom),
                                (24+width, bottom+22), (32, bottom+22)]):
        (p.moveTo if i == 0 else p.lineTo)(*point)
    p.close()
    c.setFillColor(BLUE)
    c.drawPath(p, fill=1, stroke=0)
    text(r, title, 36, top+1, width-20, size=13.5, leading=18, bold=True, color=WHITE)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.1)
    c.line(24+width+7, bottom+2, r.w-25, bottom+2)


def card(r, number, title, top, rows, *, keywords=None):
    label(r, f"{number:02d}  {title}", top)
    box_top = top + 27
    box_height = 82 if keywords else 72
    gradient(r, 25, box_top, r.w-50, box_height)
    y = box_top + 6
    for row in rows:
        r.line("•", y+1, size=13, x=38, color=BLUE)
        height = text(r, row, 55, y, r.w-94, size=12, leading=18.5, bold=True)
        if height > 19:
            raise ValueError(f"Reference card requires one line per bullet: {title}: {row}")
        y += 19
    if keywords:
        y = box_top + 62
        from reportlab.pdfbase import pdfmetrics
        width = min(pdfmetrics.stringWidth(keywords, "CNBold", 11.5)+42, r.w-95)
        gradient(r, 43, y, width, 19, radius=9)
        r.line("//", y+1, size=12, x=45, bold=True, color=BLUE)
        text(r, keywords, 67, y+1, width-26, size=11.5, leading=16, bold=True)


def start(r, decorate=True):
    r.pdf.showPage()
    r.margin, r.width, r.y = 26, r.w-52, 30
    if decorate:
        accents(r)


def draw_jobface_header(r, root, parts=None):
    """Draw the approved project header; parts also support isolated PNG exports."""
    c = r.pdf
    boxes = {}

    def enabled(key):
        return parts is None or key in parts

    def words(key, value, x, top, width, size, leading):
        if enabled(key):
            text(r, value, x, top, width, size=size, leading=leading, bold=True)
        boxes[key] = (x-2, top-2, x+width+2, top+leading+3)

    if enabled('corner-ribbons'):
        c.drawImage(ImageReader(str(root / 'assets/resume-jobface-ribbons.png')),
                    r.w-180, r.h-110, width=180, height=110, mask='auto')
    boxes['corner-ribbons'] = (r.w-180, 0, r.w, 112)
    if enabled('accent-vertical'):
        c.setFillColor(BLUE)
        c.rect(25, r.h-133, 5, 105, fill=1, stroke=0)
    boxes['accent-vertical'] = (23, 26, 32, 135)
    words('project-title', '职面AI（JobFace AI）', 40, 22, 390, 31, 41)
    words('project-subtitle', 'AI 模拟面试与能力提升平台', 40, 70, 405, 23, 32)
    if enabled('tagline-bg'):
        gradient(r, 40, 111, 331, 25, radius=12)
    boxes['tagline-bg'] = (38, 109, 373, 138)
    words('tagline-text', '模拟面试 · 求职辅助 · 能力提升', 52, 114, 315, 12, 18)
    boxes['tagline-complete'] = boxes['tagline-bg']
    if enabled('mascot'):
        c.drawImage(ImageReader(str(root / 'assets/resume-jobface.png')),
                    r.w-170, r.h-128, width=132, height=124,
                    preserveAspectRatio=True, mask='auto')
    if enabled('mascot-label-bg'):
        gradient(r, r.w-170, 127, 145, 23, radius=11)
    boxes['mascot-label-bg'] = (r.w-172, 125, r.w-23, 152)
    words('mascot-label-text', 'AI 面试官 · 乔比', r.w-157, 130, 133, 12, 17)
    boxes['mascot-label-complete'] = boxes['mascot-label-bg']
    if enabled('divider-horizontal'):
        c.setStrokeColor(BLUE)
        c.setLineWidth(.6)
        c.line(26, r.h-157, r.w-26, r.h-157)
    boxes['divider-horizontal'] = (24, 155, r.w-24, 159)
    return boxes


def draw_project_pages(r, root, site, contest):
    start(r)
    c = r.pdf
    c.setFillColor(BLUE)
    c.rect(25, r.h-133, 5, 105, fill=1, stroke=0)
    text(r, "知友（KnowMate）", 40, 22, 390, size=31, leading=41, bold=True)
    text(r, "K12 人工智能通识教育 App", 40, 70, 405, size=24, leading=32, bold=True)
    gradient(r, 40, 111, 331, 25, radius=12)
    text(r, "课程学习 · 实践探索 · 小队共学 · 成长反馈", 52, 114, 315,
         size=12, leading=18, bold=True)
    c.drawImage(ImageReader(str(root / "assets/resume-xiaoman.webp")),
                r.w-170, r.h-128, width=132, height=124,
                preserveAspectRatio=True, mask="auto")
    gradient(r, r.w-170, 127, 145, 23, radius=11)
    text(r, "AI 学习助手 · 小满", r.w-157, 130, 133, size=12, leading=17, bold=True)
    c.setStrokeColor(BLUE)
    c.line(26, r.h-157, r.w-26, r.h-157)
    groups = [
        ("实时协同与课程实践", [
            "学生端 React Native / Expo，管理端 React，后端 FastAPI。",
            "WebRTC 支持屏幕共享与语音交流，WebSocket 同步消息及协作状态。",
            "围绕五大 AI 知识模块，将课程、单人探究与小队协作衔接起来。"]),
        ("知识追踪与个性化路径", [
            "UKT：以概率分布表示知识状态，用 Wasserstein 自注意力追踪不确定性。",
            "KnowLP：结合先修、相似关系与学习目标推荐路径，遇阻补前置知识。",
            "结合六维画像和复测结果调整学习建议，证据不足时补充诊断。"]),
        ("可追溯答疑与学习记忆", [
            "LLM Wiki / RAG：关联知识来源、版本和权限，链接课程与习题。",
            "LightMem：按主题压缩交互信息，并在离线阶段整理巩固。",
            "MemoryOS：分层组织上下文与长期线索，支持跨次交流和记忆更正。"]),
        ("自适应学习支持", [
            "CTS（情境汤普森采样）：选择复习、鼓励、共学邀请或暂不提示。",
            "依据任务完成、回访和打扰反馈更新策略；限制时段与频次，允许关闭。",
            "KnowLP 负责学习内容与路径，CTS 调整支持时机与方式。"]),
        ("成长反馈与公平参与", [
            "六维反馈：知识建构、思辨推理、实践迁移、自我调控、协作表达、安全意识。",
            "积分与徽章用于鼓励参与，不代替学习质量评价；答错或暂离不扣分。",
            "任务可补做，异常奖励先提醒核验，并保留申诉与纠正入口。"]),
    ]
    for i, (title, rows) in enumerate(groups):
        card(r, i+1, title, 173+i*106, rows)
    gradient(r, 25, 710, r.w-50, 58)
    for title, value, top in [
        ("学生端：", "首页 / 组队 / 学习助手 / 训练 / 我的", 716),
        ("管理端：", "任务配置 / 账号权限 / 积分榜单 / 学习反馈", 742),
    ]:
        c.setFillColor(BLUE)
        c.roundRect(33, r.h-top-19, 65, 19, 8, fill=1, stroke=0)
        text(r, title, 39, top+1, 57, size=11.5, leading=17, bold=True, color=WHITE)
        text(r, value, 109, top+1, r.w-137, size=11.5, leading=17, bold=True)
    r.y = 799
    r.footer(2)

    start(r, decorate=False)
    draw_jobface_header(r, root)
    groups = [
        ("岗位知识库与 RAG", [
            "后端、前端、运维三类岗位均已完成题库与知识库建设。",
            "知识库包含技术栈、考点、参考答案与评分标准。",
            "RAG 支撑出题、解析和追问，追问限定在审核题库范围内。"],
         "LLM · RAG · 岗位配置 · 题库约束"),
        ("多轮面试与节奏控制", [
            "覆盖技术问答、项目深挖、场景题与行为题。",
            "根据作答生成约束式追问，围绕岗位要求深入考察。",
            "结合岗位需求与时间预算把控面试节奏。"],
         "多轮对话 · 上下文管理 · 时间预算"),
        ("语音交互与可选视频", [
            "支持语音与文本作答，视频分析作为可选辅助。",
            "分析语速、停顿和清晰度等表达指标。",
            "摄像头不可用时，语音或文本面试流程仍可完整进行。"],
         "语音识别 / ASR · 文本交互 · 视频辅助"),
        ("证据驱动的五维评估", [
            "从作答中提取有效证据，结合评分标准完成量化评估。",
            "五个维度：技术深度、逻辑表达、沟通协作、应变能力、岗位适配。",
            "情绪倾向仅作为应变能力的组成信号之一。"],
         "作答证据 · 岗位标准 · 结构化评估"),
        ("报告反馈与成长闭环", [
            "输出结构化报告，展示得分、作答证据、优缺点与改进建议。",
            "根据评估结果生成个性化练习及提升方案。",
            "留存面试记录，通过历史报告和成长曲线展示能力变化。"],
         "结构化报告 · 个性化练习 · 历史成长曲线"),
    ]
    for i, (title, rows, keywords) in enumerate(groups):
        card(r, i+1, title, 173+i*117, rows, keywords=keywords)
    r.y = 772
    r.links([("官方赛题：AI 模拟面试与能力提升软件（锐捷网络）", contest)])
    r.y = 799
    r.footer(3)
