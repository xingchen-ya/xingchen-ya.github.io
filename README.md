# 罗洋 · 个人作品集

静态站点，采用浅色纸张、橙色与山水插画。可直接打开 `index.html`，也可在本目录运行 `python -m http.server 8000`，再访问 `http://localhost:8000/`。

## 发布到 GitHub Pages

1. 在 `xingchen-ya` 账号下创建名为 `xingchen-ya.github.io` 的仓库。GitHub Free 需要使用公开仓库。
2. 上传**本目录的内容**到仓库 `main` 分支，保留 `.nojekyll`。确认 `index.html` 位于仓库根目录，且 `assets/` 也在根目录。
3. 打开仓库 **Settings → Pages → Build and deployment**，选择 **Deploy from a branch**，分支选 **main**，目录选 **/(root)**，点击 **Save**。
4. 在仓库的 **Actions** 页面确认 Pages 部署成功。再打开 [预期站点地址](https://xingchen-ya.github.io/)，检查项目展开、GitHub/Gitee 链接和简历下载。

[GitHub 官方建站步骤](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) · [官方发布源配置](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 把 GitHub 个人资料页连到作品集

站点上线后，在 GitHub 个人资料的 Website 栏填入站点地址。也可以在另一个同名公开仓库 `xingchen-ya/xingchen-ya` 的根目录添加 `README.md`，用简短介绍和项目直达链接引导访客。简历里可直接引用同样的项目地址。

```markdown
# 罗洋 · AI 全栈开发者 / 项目经理

参与 AI 学习和求职应用开发，负责团队分工、页面开发、成果验收和答辩准备。

- [独立作品集](https://xingchen-ya.github.io/)
- [KnowMate · AI 学习应用](https://xingchen-ya.github.io/#knowmate)
- [FaceNoWorry · AI 求职应用](https://xingchen-ya.github.io/#facenoworry)
```

[Peter-JXL 的个人资料示例](https://github.com/Peter-JXL) · [Peter-JXL 的主页制作教程](https://www.cnblogs.com/PeterJXL/p/18437094) · [GitHub 官方 Profile README 指南](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)

## 更新内容

- `index.html` 保存自我介绍和项目经历。团队仓库仅列链接，具体个人职责确认后再补充。
- `assets/` 保存公开展示的图片及求职简历 PDF。网站与简历已补充联系方式、教育、实习意向、技术能力和项目阶段记录；学校留空，意向城市待定。
- Pages 只提供静态托管。数据库、登录后台和私有上传可接独立服务。首版通过 GitHub 仓库维护文件。

## 透明素材

原图拆分素材位于 assets/extracted/，共 3 张 PNG 和 9 个 SVG，合计约 290 KiB。assets-preview.html 提供棋盘、纸色和深色背景预览。

山水与笔记本使用内置 imagegen 辅助提取，可能存在细节重绘；笔记本仅为示意素材。主页面接入透明山水与 SVG 按钮，项目区继续使用项目截图。通用图标与笔画为 SVG 重建，GitHub 图标来自 Bootstrap Icons，MIT 许可见 assets/extracted/LICENSE-icons.txt。

## 项目媒体与证明

首页各项目列出重点功能与技术标签；`videos.html` 提供灵犀学伴、智翎智能学习平台和法智引擎的视频节选。媒体位于 `assets/media/`，默认点击后加载；获奖证书及预览图位于 `assets/awards/`，获奖区链接至完整图片或原 PDF。2026 年全国赛证书暂不关联具体项目。

获奖区目前整理 8 项去重后的荣誉，每项附参赛实践、赛事介绍与证明入口。全国、区域、省级与校级按证明分别标注；机器人名单与申报界面作为同一校赛一等奖的佐证，含他人联系方式的申报表不公开。个人职责只使用已有依据的参赛经历。

## 更新简历

`scripts/build_resume.py` 使用 ReportLab 生成一页简历，默认中文字体为 Windows 宋体，可通过 `--font` 指定其他中文 TTF 字体。安装 `reportlab` 后在项目目录运行 `python scripts/build_resume.py`。生成后检查页数、文字提取和页面渲染，再发布更新。内容来源与待补项见 `docs/resume-content-evidence.md`。
