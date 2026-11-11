"""Build the one-page public resume. Requires reportlab and a Chinese TTF font."""

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
INK = colors.HexColor("#241b15")
ACCENT = colors.HexColor("#ad471b")
QUIET = colors.HexColor("#675748")


def build(font_path: Path, output: Path) -> None:
    pdfmetrics.registerFont(TTFont("ResumeCN", str(font_path)))
    pdfmetrics.registerFontFamily("ResumeCN", normal="ResumeCN", bold="ResumeCN")
    base = dict(fontName="ResumeCN", textColor=INK, wordWrap="CJK", alignment=TA_LEFT)
    styles = {
        "name": ParagraphStyle("name", fontSize=29, leading=36, **base),
        "role": ParagraphStyle("role", fontSize=12, leading=20, **{**base, "textColor": ACCENT}),
        "contact": ParagraphStyle("contact", fontSize=9, leading=15, **base),
        "body": ParagraphStyle("body", fontSize=9.4, leading=15, spaceAfter=3, **base),
        "heading": ParagraphStyle("heading", fontSize=13, leading=20, spaceBefore=10, spaceAfter=3, **base),
        "project": ParagraphStyle("project", fontSize=11, leading=17, spaceBefore=4, spaceAfter=3, **base),
        "meta": ParagraphStyle("meta", fontSize=8.6, leading=14, spaceAfter=3, **{**base, "textColor": QUIET}),
    }
    story = []

    def para(text: str, style: str = "body") -> Paragraph:
        return Paragraph(text, styles[style])

    def section(title: str) -> None:
        story.append(para(title, "heading"))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#c5b49d"), spaceAfter=5))

    story.extend([
        para("罗洋", "name"),
        para("求职意向：AI 全栈工程师 / 实习", "role"),
        para('邮箱：<link href="mailto:3583418031@qq.com">3583418031@qq.com</link>　电话：18989542495', "contact"),
        para("到岗时间：2027.07　意向城市：待定", "contact"),
        para('<link href="https://xingchen-ya.github.io/">作品集：xingchen-ya.github.io</link>　<link href="https://github.com/xingchen-ya">GitHub：xingchen-ya</link>', "contact"),
    ])
    section("教育背景")
    story.append(para("物联网工程 / 本科在读　　2024.09 - 2028.06（预计毕业）"))
    story.append(para("学校：________", "meta"))
    section("技术能力")
    skills = [
        "前端与移动端：JavaScript、TypeScript、React、React Native、Expo Router；页面组件、路由导航、表单与状态管理；HTML / CSS 响应式网页。",
        "后端与接口：参与 Python / FastAPI 项目开发与整合；REST API、Axios / Fetch、JSON 数据映射、鉴权状态、异步请求、超时与错误处理。",
        "AI 应用：参与大模型服务接入、提示词与结构化结果展示，组织分析 / 润色的加载、结果、重试和降级流程。",
        "工程与协作：Git 分支协作、代码整合、Android / ADB 调试、APK 打包、本地环境联调与测试检查；任务拆分、成果验收和答辩材料整理。",
        "项目技术接触：Redux Toolkit、AsyncStorage、安全存储；MySQL、PostgreSQL / pgvector、Redis、SQLAlchemy、LangChain、Docker Compose。",
    ]
    story.extend(para(escape(text)) for text in skills)
    section("项目经历")
    projects = [
        (
            "KnowMate / AI 学习应用",
            "2026.08 - 2026.10　团队项目 / 项目经理、移动端开发",
            [
                "参与登录与新手引导、个人页、成长报告的页面开发及整合，使用 React Native、TypeScript 与 Expo Router 组织页面和交互。",
                "参与 AI 故事引导与学习画像流程，处理进度恢复、账号隔离、加载反馈和失败重试；协调前后端接口联调。",
                "负责模块分工、页面与交互验收、成员成果整合，以及演示流程和答辩材料准备。",
            ],
            "https://github.com/xingchen-ya/Digital_Intelligence",
        ),
        (
            "FaceNoWorry / AI 求职应用",
            "2026.03 - 2026.09　团队项目 / 项目经理、应用开发",
            [
                "参与简历管理、分析与润色页面及接口接入，围绕简历 ID 组织生成请求、结果查询、加载展示、超时处理和失败重试。",
                "参与登录注册、新老用户判断、社区帖子 / 评论 / 关注功能开发与接口对接，处理请求封装和鉴权状态。",
                "负责任务分配、成果验收、项目整合与答辩准备；已有部分登录验证记录，简历服务完整在线端到端结果尚未确认。",
            ],
            "https://gitee.com/hao_miao_miao/face-no-worry",
        ),
    ]
    for title, meta, bullets, url in projects:
        block = [para(title, "project"), para(meta, "meta")]
        block.extend(para("· " + escape(text)) for text in bullets)
        block.append(para(f'<link href="{url}">{url.removeprefix("https://")}</link>', "meta"))
        story.append(KeepTogether(block))
    story.append(Spacer(1, 4))
    story.append(para("项目时间依据原始提交与阶段联调记录；展示截图和演示数据不代表真实业务指标。", "meta"))

    def footer(canvas, document):
        canvas.setTitle("罗洋 - AI全栈工程师实习简历")
        canvas.setAuthor("罗洋")
        canvas.setFont("ResumeCN", 8)
        canvas.setFillColor(QUIET)
        canvas.drawString(42, 23, "罗洋 / AI 全栈工程师实习")
        canvas.drawRightString(A4[0] - 42, 23, str(document.page))

    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=42, leftMargin=42,
                                 topMargin=29, bottomMargin=36)
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=Path("C:/Windows/Fonts/simsun.ttc"))
    parser.add_argument("--output", type=Path, default=ROOT / "assets/luo-yang-resume.pdf")
    args = parser.parse_args()
    build(args.font, args.output)
