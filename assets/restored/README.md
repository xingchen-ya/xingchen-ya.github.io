# 网站还原素材

此目录为新版纸感作品集实际使用的独立素材，共 27 项：19 张透明 PNG、8 个 SVG。另有 `previews/` 下 18 张小尺寸透明 PNG，供网页按屏幕大小选用，避免默认下载全部大图。

## 手机素材

`knowmate-practice.png`、`knowmate-growth.png`、`facenoworry-home.png`、`facenoworry-analysis.png`、`facenoworry-polish.png` 均为 **宽 1080 × 高 1920 像素**。

以原站项目截图为内容，在透明画布上使用网页设备边框渲染，再导出 PNG。画面按截图原始长宽比放入，没有将界面强行拉伸成 9:16，也没有裁切页面。1080×1920 是交付画布尺寸；源截图本身的细节分辨率没有被夸大为原生全高清。页面使用小图预览，点击后可查看原始截图。

## 背景处理与来源

- `mountains-sun.png`：使用内置 imagegen，从用户选定的第三版展示图中辅助提取。去掉原纸张与界面背景，保留水墨线条和橙色太阳；可能有局部重绘。
- 项目界面与获奖预览：使用现有真实图片，通过网页渲染透明外围、圆角和设备边框，未用 AI 改写截图或证书内容。界面底色、证书纸张属于内容本身，予以保留；原始 JPG、WebP、PDF 证明文件未改写。
- `ridge-ornament.svg`、`browser-dots.svg`：用矢量路径重建装饰；其余图标、笔画与纸纹复用既有矢量素材。均无实色矩形底图。纸纹用于叠加到网页背景色上。
- GitHub 图标来自 Bootstrap Icons，MIT 许可见 `LICENSE-icons.txt`。

## 清晰度与体积

PNG 保留真实透明通道，采用调色板与无损 DEFLATE 压缩；反锯齿边缘包含半透明像素。SVG 不嵌入栅格背景。网页通过 `srcset` 和懒加载按需选择预览图；高清交付图完整保留。

`manifest.json` 列出素材尺寸、字节数、透明像素和实色像素统计。可在网站 `assets-preview.html` 用透明棋盘、纸色、深色背景检查边缘。
