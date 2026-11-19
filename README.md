# 个人主页生成与更新

把你想放到个人主页上的资料发给 Agent，就能生成一版网页预览。简历、几段文字、照片和链接都可以直接发。默认可展示个人介绍、个人经历、作品与项目、联系方式。每个区块都支持图文混排和链接。没有作品集也可以先做个人介绍。

- [打开在线示例](https://rainbowwa999.github.io/personal-homepage-template/)
- [下载模板和 Skill](https://rainbowwa999.github.io/personal-homepage-template/personal-homepage-skill.zip)

## 怎么用

1. 下载并解压，打开 `demo.html` 看效果。示例里的人物和资料都是虚构的。
2. 支持 Skill 的 Agent 可以导入 `personal-homepage/`。其他能读取项目文件的 Agent 可以打开解压后的目录，从 `personal-homepage/SKILL.md` 开始。
3. 把资料发给 Agent，然后说：

   > 用这个模板做一版我的个人主页。把资料放进合适的区块，先给我预览。我看完再决定怎么改、要不要上线。

4. 以后打开同一个主页项目，说「换掉首页照片」「加一页摄影」或「更新到原来的链接」即可继续。

资料保存在主页项目的 `content.json`，最终网页是 `index.html`。生成器使用 Python 3.9 或更新版本，无需安装额外依赖。发布时可用 GitHub Pages、Netlify、Cloudflare Pages、Vercel、腾讯云 EdgeOne、ChatGPT Sites 或其他支持静态网页的托管。具体路线看你的账号和当前 Agent 的能力。

如果想手动生成，可参照 [资料格式](personal-homepage/references/content.md) 创建 `content.json`，再执行：

```sh
python3 personal-homepage/scripts/build.py /你的主页项目路径
```
