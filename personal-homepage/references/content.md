# 主页资料格式

每个主页单独使用一个目录。将下方 JSON 保存为该目录里的 `content.json`，图片可放在同目录的 `media/` 内。最终的 `index.html` 由脚本生成。

```json
{
  "name": "示例姓名",
  "subtitle": "内容策划与社区运营",
  "portrait": {"src": "media/photo.jpg", "alt": "个人照片"},
  "sections": [
    {
      "id": "about",
      "title": "个人介绍",
      "blocks": [
        {"type": "text", "text": "我在做内容策划，也记录周末的城市散步。"},
        {"type": "link", "label": "看我的文章", "url": "https://example.com/"}
      ]
    },
    {
      "id": "photography",
      "title": "我的摄影",
      "blocks": [
        {"type": "text", "text": "这是我最近拍的城市照片。"},
        {"type": "image", "src": "media/street.jpg", "alt": "傍晚的街道", "caption": "周末散步"},
        {"type": "link", "label": "查看更多", "url": "https://example.com/"}
      ]
    }
  ]
}
```

- `name`、`subtitle`、`portrait` 可省略。无姓名时网页标题用「个人主页」，无头像时使用渐变版式。
- `sections` 决定页面和导航的顺序。默认可用 `about`、`experience`、`projects`、`contact`，标题可改。可用任意小写英文 ID 增加区块，有内容才会显示。
- `blocks` 按顺序支持 `text`、`image`、`link`。`heading` 可用字段 `text` 加小标题。也可用 `card`，字段为 `title`、可选 `summary` 和用于展开的 `blocks`。卡片详情使用文字、图片、链接和小标题。适用于作品、经历及自定义区块。
- 图片可用主页项目内的相对路径，或用户提供的 HTTPS 图片地址。写清替代文字。链接支持 HTTP、HTTPS、mailto 和页内锚点。
- 联系区块写成 `link`，例如 `{"type":"link","label":"hi@example.com","url":"mailto:hi@example.com"}`。
- 示例网页用虚构内容。生成个人版时使用用户资料。没有资料时可以直接打开示例，或用 `--demo` 模式生成一份单独的示例网页。
