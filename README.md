# 王冬科研主页

网站使用 GitHub Pages 支持的 Jekyll 生成静态页面。共用导航在 `_data/navigation.yml`，双语首页文案在 `_data/home.yml`，公开联系方式和代表成果在 `_data/profile.yml`。页面模板在 `_layouts/`，站点样式在 `style.css`。

## 本地预览

使用 Ruby 3.3 和 Bundler。在仓库目录执行：

```sh
bundle install
bundle exec jekyll serve
```

打开终端所示的本地地址。只生成静态文件时，运行 `bundle exec jekyll build`，输出到 `_site/`。

## 更新内容

| 栏目 | 从哪里更新 | 详情地址 |
| --- | --- | --- |
| 科研首页 | `_data/home.yml`、`_data/profile.yml` | `/`、`/en/` |
| 个人简历 | `_data/cv.yml` | `/cv/`、`/en/cv/` |
| 课题组动态 | `_group_updates/<slug>.md` | `/group/updates/<slug>/` |
| 文献日报 | `_literature/YYYY-MM-DD.md` | `/literature/YYYY-MM-DD/` |
| CCF 会议追踪 | `_conference_editions/<series>/<year>.md` | `/conferences/<series>/<year>/` |
| 知识库 | `_knowledge_notes/<topic>/<slug>.md` | `/knowledge/<topic>/<slug>/` |

日报试刊可用作 Markdown 元数据样例。标题、摘要和栏目专用字段由栏目页和详情页一起读取。日报使用 `date`、`coverage` 和可选 `topics`。课题组条目使用 `date` 和 `kind`，会议届次使用 `status`、`next_milestone` 和 `last_verified`，知识笔记使用 `topic` 和可选 `updated`。首页自动读取最新一期日报与最近三条课题组动态。

只将可公开的条目放进本仓库。`sample: true` 会标注预览样例并为详情页添加 `noindex`。预览样例的内容仍会生成可访问的页面。

中文版沿用现有路径，英文版位于 `/en/` 下。写英文条目时设置 `lang: en` 和以 `/en/` 开头的 `permalink`。有对应译文时，两条记录的 `alternate_url` 互指。语言设置与日间／夜间模式保存在访问者的浏览器中。

旧首页的八个履历锚点由 `_data/legacy_sections.yml` 映射到中文版简历。保留两个简历页面中的对应 ID 和历史报告路径。
