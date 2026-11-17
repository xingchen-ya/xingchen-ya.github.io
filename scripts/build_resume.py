"""Build a searchable three-page A4 resume and reference-matched project pages."""
import argparse
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from resume_project_pages import draw_project_pages
from resume_header import draw_header

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
        if self.y > self.h - 41:
            raise ValueError("Content overlaps footer")
        self.pdf.setStrokeColor(RULE)
        self.pdf.setLineWidth(.6)
        self.pdf.line(self.margin, 33, self.w - self.margin, 33)
        self.line("罗洋 · AI 全栈工程师实习", self.h - 27, 8, color=QUIET)
        self.line(f"{page} / 3", self.h - 27, 8, x=self.w - self.margin, color=QUIET, right=True)


def personal_header(r):
    draw_header(r.pdf, r.h, ROOT / 'assets/resume-header')
    r.y = 131


def build(font_path, output, bold_path=None):
    pdfmetrics.registerFont(TTFont("CN", str(font_path)))
    pdfmetrics.registerFont(TTFont("CNBold", str(bold_path or font_path)))
    pdfmetrics.registerFontFamily("CN", normal="CN", bold="CNBold")
    output.parent.mkdir(parents=True, exist_ok=True)
    r = Resume(output)
    personal_header(r)
    r.section("教育背景")
    r.line("浙江树人学院 · 物联网工程 · 本科在读", r.y, 11, bold=True)
    r.line("2024.09 - 2028.06", r.y + 1, 9, x=r.w-r.margin, color=QUIET, right=True)
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
    r.project("知友（KnowMate）", "2026.08 - 2026.10",
              "项目经理 / 移动端开发　 |　 React Native / Expo · TypeScript · FastAPI",
              "面向 K12 学生的 AI 通识教育 App，结合课程、训练、小队共学与学习助手“小满”。",
              ["<b>页面与整合：</b>参与登录、新手引导、个人页与成长报告开发，整合页面、路由与交互。",
               "<b>交互与联调：</b>参与故事引导与学习画像流程，处理进度恢复、账号隔离、加载和失败重试。",
               "<b>协作与交付：</b>负责模块分工、成果验收、项目整合，以及演示流程和答辩材料准备。"],
              [("项目代码", ZHIYOU), ("项目资料", SITE + "#knowmate")])
    r.y += 6
    r.project("职面AI（JobFace AI）", "2026.03 - 2026.09",
              "项目经理 / 应用开发　 |　 React Native · TypeScript · LLM / RAG",
              "面向计算机专业学生的模拟面试与能力提升平台，覆盖后端、前端和运维岗位，兼顾求职辅助。",
              ["<b>应用开发：</b>参与简历管理、分析与润色页面及接口接入，组织生成请求、查询和结果展示。",
               "<b>接口与状态：</b>参与登录注册和社区功能，处理鉴权、异步请求、超时反馈与失败重试。",
               "<b>项目推进：</b>负责任务分配、成果验收、应用整合与答辩准备；面试技术机制见第 3 页。"],
              [("项目代码", JOBFACE), ("官方赛题", CONTEST)])
    r.y += 4
    r.para("<b>其他项目实践</b>", gap=3)
    for title, description, anchor in [
        ("法智引擎", "AI 法律服务，法律咨询与合同文档处理。", "fazhi"),
        ("乳腺癌影像分析", "国家级创新创业项目，影像分析与分割流程。", "breast-imaging"),
        ("灵犀学伴", "移动学习体验与学习交互。", "lingxi"),
        ("智翎智能学习平台", "Web 学习中心与教学管理。", "zhiling"),
    ]:
        r.para(f'<link href="{SITE}#{anchor}" color="#3155D8"><b>{title}</b></link>：{description}',
               "meta", gap=2)
    r.section("代表荣誉")
    for text in [
        "2026.07　中国大学生服务外包创新创业大赛 · 全国赛三等奖（人工智能专项赛道）",
        "2026.06　同届大赛 · 东部区域赛二等奖（人工智能专项赛道）",
        "2025.11　浙江省第十二届大学生服务外包创新应用大赛 · 一等奖",
        "2025.05　第三届“外研U词杯”全国大学生英语词汇智慧学习大赛 · 全国一等奖",
    ]:
        r.para(escape(text), "meta", gap=2)
    r.footer(1)
    draw_project_pages(r, ROOT, SITE, CONTEST)
    r.pdf.save()
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=Path("C:/Windows/Fonts/msyh.ttc"))
    parser.add_argument("--bold-font", type=Path, default=Path("C:/Windows/Fonts/msyhbd.ttc"))
    parser.add_argument("--output", type=Path, default=ROOT / "assets/luo-yang-resume.pdf")
    args = parser.parse_args()
    build(args.font, args.output, args.bold_font if args.bold_font.exists() else None)
