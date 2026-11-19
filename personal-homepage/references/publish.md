# 发布个人主页

先打开最终预览，检查用户要公开的照片、联系方式、链接和区块。确认目标站点、访问范围，再使用当前 Agent 环境支持的授权方式。对外分享前检查站点是否能按约定方式访问。

| 方式 | 适用条件 | 发布方法 |
|---|---|---|
| GitHub Pages | 发布者有 GitHub 账号和仓库权限。免费账号使用公开仓库。公开主页的访客可以直接打开。 | 将 index.html 放到指定发布目录。在仓库 Settings → Pages 选择发布分支和目录。已有 Pages 站点时更新原文件。 |
| Netlify Drop | 需要拖拽上传。匿名部署可先预览，通常要登录认领并检查可见性后才能作为公开站点分享。 | 打开 Drop 入口，把只包含 index.html 的目录上传。更新时进入原站点的生产部署页面上传。 |
| Cloudflare Pages | 发布者有 Cloudflare 账号，可直接上传，无需 GitHub。 | 在 Pages 创建 Direct Upload 项目，上传仅包含 index.html 的目录。更新时给原项目创建新部署。 |
| Vercel | 发布者有 Vercel 账号，可导入仓库或部署本地目录。 | 导入包含 index.html 的静态项目，或使用已登录的 Vercel CLI 发布。分享前检查正式网址的访问保护。 |
| 腾讯云 EdgeOne Pages / Makers | 发布者有腾讯云账号。 | 在控制台选择直接上传，上传网站文件夹或 ZIP。更新时给原项目创建生产部署。 |
| ChatGPT Sites | 账号和当前环境支持 Sites 及所需分享范围，当前 Agent 可以把静态网页导入或部署。 | 通过可用的 Sites 工作流发布并检查分享范围。已有站点则更新对应的项目。 |
| 自有服务器或其他静态托管 | 用户有目标站点上传权限。 | 上传 index.html 到站点发布目录，按照平台设置开启 HTTPS 和所需访问权限。 |

先查阅所选平台的最新官方说明：
[GitHub Pages](https://docs.github.com/en/pages/quickstart) · [Netlify Drop](https://docs.netlify.com/start/quickstarts/netlify-drop-quickstart/) · [Cloudflare Pages](https://developers.cloudflare.com/pages/get-started/direct-upload/) · [Vercel](https://vercel.com/docs/deployments) · [腾讯云](https://cloud.tencent.com/document/product/1552/127371) · [ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites)。

公开发布后，用未登录的浏览器检查首页和新改动。限制访问的站点要检查访问要求和允许的访客范围。当前 Agent 只能生成文件时，将用户带到对应入口，并说明应该上传哪个文件或目录。
