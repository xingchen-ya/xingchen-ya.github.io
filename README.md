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
- `assets/` 保存公开展示的图片及简历 PDF。当前 PDF 是依据已提供经历制作的项目版，可用正式公开版替换同名文件。
- Pages 只提供静态托管。数据库、登录后台和私有上传可接独立服务。首版通过 GitHub 仓库维护文件。
