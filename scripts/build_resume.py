"""Build a searchable, linked two-page A4 resume with ReportLab."""
import argparse
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
BLUE, INK, QUIET, RULE = [colors.HexColor(c) for c in
                         ("#3155D8", "#142342", "#536176", "#CFDAF0")]
SITE = "https://xingchen-ya.github.io/"
CONTEST = "https://www.fwwb.org.cn/topic/show/b027144e-595f-4789-a9d3-057ee8386c53"
ZHIYOU = "https://github.com/xingchen-ya/Digital_Intelligence"
JOBFACE = "https://gitee.com/hao_miao_miao/face-no-worry"


class Resume:
    """Measure every paragraph and fail on page overflow."""
    def __init__(self, output):
        self.w, self.h = A4
        self.margin, self.y = 36, 34
        self.width = self.w - 72
        self.pdf = canvas.Canvas(str(output), pagesize=A4, pageCompression=1, invariant=1)
        self.pdf.setTitle("罗洋 - AI全栈工程师实习简历")
        self.pdf.setAuthor("罗洋")
        self.styles = {
            "body": ParagraphStyle("body", fontName="CN", fontSize=10.5,
                                   leading=15.5, textColor=INK, wordWrap="CJK"),
            "meta": ParagraphStyle("meta", fontName="CN", fontSize=9,
                                   leading=13, textColor=QUIET, wordWrap="CJK"),
        }

    def line(self, text, top, size=10.5, x=None, bold=False, color=INK, right=False):
        self.pdf.setFont("CNBold" if bold else "CN", size)
        self.pdf.setFillColor(color)
        draw = self.pdf.drawRightString if right else self.pdf.drawString
        draw(self.margin if x is None else x, self.h - top - size, text)

    def para(self, text, style="body", indent=0, gap=3):
        p = Paragraph(text, self.styles[style])
        _, height = p.wrap(self.width - indent, self.h)
        if self.y + height > self.h - 46:
            raise ValueError(f"Page overflow near: {text[:70]}")
        p.drawOn(self.pdf, self.margin + indent, self.h - self.y - height)
        self.y += height + gap

    def bullet(self, text):
        self.line("•", self.y, color=BLUE)
        self.para(text, indent=12)

    def section(self, title):
        self.y += 10
        width = pdfmetrics.stringWidth(title, "CNBold", 12) + 26
        bottom = self.h - self.y - 22
        self.pdf.setFillColor(BLUE)
        shape = self.pdf.beginPath()
        for i, point in enumerate([(self.margin, bottom), (self.margin + width - 7, bottom),
                                    (self.margin + width, bottom + 22), (self.margin + 7, bottom + 22)]):
            (shape.moveTo if i == 0 else shape.lineTo)(*point)
        shape.close()
        self.pdf.drawPath(shape, fill=1, stroke=0)
        self.line(title, self.y + 2, 12, x=self.margin + 14, bold=True, color=colors.white)
        self.pdf.setStrokeColor(BLUE)
        self.pdf.setLineWidth(.65)
        self.pdf.line(self.margin + width + 8, bottom + 4, self.w - self.margin, bottom + 4)
        self.y += 29

    def links(self, entries):
        self.para('　 |　 '.join(f'<link href="{escape(url)}" color="#3155D8">{escape(label)}</link>'
                               for label, url in entries), "meta", gap=4)

    def project(self, name, dates, role, description, bullets, links):
        self.line(name, self.y, 12, bold=True)
        self.line(dates, self.y + 2, 9, x=self.w - self.margin, color=QUIET, right=True)
        self.y += 20
        self.para(escape(role), "meta", gap=4)
        self.para(escape(description), gap=4)
        for text in bullets:
            self.bullet(text)
        self.links(links)

    def footer(self, page):
        if self.y > self.h - 45:
            raise ValueError("Content overlaps footer")
        self.pdf.setStrokeColor(RULE)
        self.pdf.setLineWidth(.6)
        self.pdf.line(self.margin, 33, self.w - self.margin, 33)
        self.line("罗洋 · AI 全栈工程师实习", self.h - 27, 8, color=QUIET)
        self.line(f"{page} / 2", self.h - 27, 8, x=self.w - self.margin, color=QUIET, right=True)


def build(font_path, output, bold_path=None):
    pdfmetrics.registerFont(TTFont("CN", str(font_path)))
    pdfmetrics.registerFont(TTFont("CNBold", str(bold_path or font_path)))
    pdfmetrics.registerFontFamily("CN", normal="CN", bold="CNBold")
    output.parent.mkdir(parents=True, exist_ok=True)
    r = Resume(output)
    r.line("罗洋", 28, 32, bold=True)
    r.line("AI 全栈工程师 · 实习", 36, 14, x=150, bold=True, color=BLUE)
    r.line("2027.07 起可到岗 · 意向城市待定", 60, 10, x=150, color=QUIET)
    r.y = 91
    r.links([("3583418031@qq.com", "mailto:3583418031@qq.com"),
             ("18989542495", "tel:18989542495"), ("个人网站", SITE),
             ("GitHub", "https://github.com/xingchen-ya")])
    r.section("教育背景")
    r.line("浙江树人学院 · 物联网工程 · 本科在读", r.y, 11, bold=True)
    r.line("2024.09 - 2028.06（预计）", r.y + 1, 9, x=r.w-r.margin, color=QUIET, right=True)
    r.y += 21
    r.section("核心技能")
    for title, text in [
        ("前端与移动端", "TypeScript / JavaScript、React、React Native、Expo Router。"),
        ("后端与接口", "Python / FastAPI、REST API、Axios / Fetch、鉴权及异步状态处理。"),
        ("AI 应用接入", "大模型 API、提示词、结构化结果展示、加载反馈与失败重试。"),
        ("工程与协作", "Git、Android / ADB、APK 打包、接口联调、任务拆分与成果验收。"),
    ]:
        r.para(f"<b>{title}：</b>{escape(text)}", gap=2)
    r.section("项目经历")
    r.project("知友（KnowMate）", "2026.08 - 2026.10 · 阶段记录",
              "项目经理 / 移动端开发　 |　 React Native / Expo · TypeScript · FastAPI",
              "面向 K12 学生的 AI 通识教育 App，结合课程、训练、小队共学与学习助手“小满”。",
              ["<b>页面与整合：</b>参与登录、新手引导、个人页与成长报告开发，整合页面、路由与交互。",
               "<b>交互与联调：</b>参与故事引导与学习画像流程，处理进度恢复、账号隔离、加载和失败重试。",
               "<b>协作与交付：</b>负责模块分工、成果验收、项目整合，以及演示流程和答辩材料准备。"],
              [("项目代码", ZHIYOU), ("项目资料", SITE + "#knowmate")])
    r.y += 6
    r.project("职面AI（JobFace AI）", "2026.03 - 2026.09 · 阶段记录",
              "项目经理 / 应用开发　 |　 React Native · TypeScript · LLM / RAG",
              "面向计算机专业学生的模拟面试与能力提升平台，覆盖后端、前端和运维岗位，兼顾求职辅助。",
              ["<b>应用开发：</b>参与简历管理、分析与润色页面及接口接入，组织生成请求、查询和结果展示。",
               "<b>接口与状态：</b>参与登录注册和社区功能，处理鉴权、异步请求、超时反馈与失败重试。",
               "<b>项目推进：</b>负责任务分配、成果验收、应用整合与答辩准备；面试技术机制见第 2 页。"],
              [("项目代码", JOBFACE), ("官方赛题", CONTEST)])
    r.section("代表荣誉")
    for text in [
        "2026.07　中国大学生服务外包创新创业大赛 · 全国赛三等奖（人工智能专项赛道）",
        "2026.06　同届大赛 · 东部区域赛二等奖（人工智能专项赛道）",
        "2025.11　浙江省第十二届大学生服务外包创新应用大赛 · 一等奖",
        "2025.05　第三届“外研U词杯”全国大学生英语词汇智慧学习大赛 · 全国一等奖",
    ]:
        r.para(escape(text), "meta", gap=2)
    r.footer(1)
    r.pdf.showPage()
    r.y = 32
    r.line("精选项目 · 技术补充", r.y, 21, bold=True)
    mascot = ROOT / "assets/resume-xiaoman.webp"
    if mascot.exists():
        r.pdf.drawImage(ImageReader(str(mascot)), r.w - 90, r.h - 79,
                        width=48, height=48, preserveAspectRatio=True, mask="auto")
    r.y += 34
    r.para("以下为项目功能与技术机制；个人分工见第 1 页。", "meta")
    r.section("知友  /  共学与学习支持")
    r.para("<b>定位：</b>面向 K12 的 AI 通识教育；课程、实践、小队协作与学习反馈衔接。")
    for text in [
        "<b>实时共学：</b>React Native / Expo 学生端、React 管理端与 FastAPI 后端；WebRTC 承载屏幕共享和语音，WebSocket 同步消息与协作状态。",
        "<b>诊断与路径：</b>UKT 以概率知识状态与 Wasserstein 自注意力追踪掌握趋势及不确定性；KnowLP 结合先修、相似关系和学习目标推荐路径。",
        "<b>知识与记忆：</b>LLM Wiki / RAG 关联知识来源、版本与权限；LightMem 按主题压缩交互并离线巩固。<br/>MemoryOS 分层组织上下文与长期线索（扩展方案）。",
        "<b>支持时机：</b>CTS 选择复习、鼓励、共学邀请或暂不提示，限制时段与频次，允许关闭。<br/>KnowLP 负责内容与路径，CTS 仅调整支持时机与方式。",
    ]:
        r.bullet(text)
    r.para("学习助手“小满”提供答疑与引导；积分用于协作激励，六维反馈用于学习改进，两者分开呈现。", "meta", gap=6)
    r.links([("知友代码", ZHIYOU), ("项目资料", SITE + "#knowmate")])
    r.section("职面AI  /  模拟面试与能力提升")
    r.para("<b>定位：</b>面向后端、前端、运维三类岗位，形成“面试 - 评估 - 练习 - 成长”的提升流程。")
    for text in [
        "<b>知识库与 RAG：</b>三岗题库覆盖技术问答、项目深挖、场景题与行为题。<br/>知识库关联考点、参考答案与评分标准，支撑出题、解析和追问。",
        "<b>受限追问与编排：</b>AI 面试官在审核题库范围内追问，结合岗位需求、作答上下文和时间预算控制面试节奏。",
        "<b>多模态交互：</b>支持语音与文本作答，可选视频辅助；摄像头不可用时不阻断面试。语音反馈关注语速、停顿与清晰度。",
        "<b>证据评估与成长：</b>从作答提取证据，按技术深度、逻辑表达、沟通协作、应变能力、岗位适配五维输出报告；情绪倾向仅作为组成信号。报告连接练习计划、历史记录与成长曲线。",
    ]:
        r.bullet(text)
    r.links([("职面AI代码", JOBFACE), ("官方赛题：AI 模拟面试与能力提升软件", CONTEST)])
    r.section("更多项目与证明")
    r.para("法智引擎、乳腺癌影像分析、灵犀学伴、智翎智能学习平台的功能、演示及获奖证明见个人网站。", gap=7)
    r.links([("项目展示", SITE + "#projects"), ("获奖证明", SITE + "#awards"),
             ("联系我", "mailto:3583418031@qq.com")])
    r.para("说明：阶段日期依据原始提交与联调记录。技术补充按设计方案及最新项目说明整理，不将团队整体功能归为个人独立完成，不使用演示数据作为业务指标。", "meta", gap=0)
    r.footer(2)
    r.pdf.save()
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=Path("C:/Windows/Fonts/msyh.ttc"))
    parser.add_argument("--bold-font", type=Path, default=Path("C:/Windows/Fonts/msyhbd.ttc"))
    parser.add_argument("--output", type=Path, default=ROOT / "assets/luo-yang-resume.pdf")
    args = parser.parse_args()
    build(args.font, args.output, args.bold_font if args.bold_font.exists() else None)
