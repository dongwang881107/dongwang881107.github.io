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
| 文献热点 | `_literature/YYYY-MM-DD.md`、`_literature/en/YYYY-MM-DD.md` | `/literature/YYYY-MM-DD/`、`/en/literature/YYYY-MM-DD/` |
| CCF 会议追踪 | `_data/conference_schedule.json`、`_data/conference_archive.json`、`_data/conference_review.yml` | `/conferences/`、`/en/conferences/` |
| 知识库 | `_knowledge_notes/<topic>/<slug>.md` | `/knowledge/<topic>/<slug>/` |

标题、摘要和栏目专用字段由栏目页和详情页一起读取。课题组条目使用 `date` 和 `kind`，会议届次使用 `status`、`next_milestone` 和 `last_verified`，知识笔记使用 `topic` 和可选 `updated`。首页自动读取最新一篇文献热点与最近三条课题组动态。

只将可公开的条目放进本仓库。`sample: true` 会标注预览样例并为详情页添加 `noindex`。预览样例的内容仍会生成可访问的页面。

中文版沿用现有路径，英文版位于 `/en/` 下。写英文条目时设置 `lang: en` 和以 `/en/` 开头的 `permalink`。有对应译文时，两条记录的 `alternate_url` 互指。语言设置与日间／夜间模式保存在访问者的浏览器中。

旧首页的八个履历锚点由 `_data/legacy_sections.yml` 映射到中文版简历。保留两个简历页面中的对应 ID 和历史报告路径。

## 更新文献热点

每期从「每日文献日报」任务生成的精选日报中选一篇，优先关注与医学成像、电阻抗成像或逆问题相关的 CCF A 类会议论文和中科院一区期刊论文。正文写清研究问题、方法、实验依据及与本领域的关联。论文原文和出版记录用于核对内容与出处。

中英文条目使用同一天的文件名和发布日期。设置 `title`、`summary`、`date`、`lang`、`permalink` 及互指的 `alternate_url`。`paper` 下写入原论文 `title`、发表 `venue` 和原文 `url`，可附 `doi` 与经核实的 `tier`。`topics` 可记录相关研究方向。列表按日期倒序排列，早期试刊可从原地址访问。

## 刷新 CCF 会议日程

网站的会议日程从会议追踪项目的 `配置/watchlist.json` 导出。源项目更新后，在网站仓库执行以下命令，并重新运行 Jekyll 构建或预览。

```sh
python3 tools/export_conference_schedule.py "/path/to/meeting-tracker/配置/watchlist.json"
```

生成的 `_data/conference_schedule.json` 由中英文会议页共用。默认从源快照的核对日期起显示未来 180 天，也可用 `--as-of YYYY-MM-DD` 和 `--days N` 指定窗口。精确时刻换算为北京时间并保留原时区。官网只给日期时，页面保留原日期。暂定和尚待公布的会议单独列出。

## 刷新 CCF 往期回顾

在网站仓库运行下列命令，传入会议追踪项目的根目录。

```sh
python3 tools/export_conference_archive.py "/path/to/meeting-tracker"
```

脚本从会议注册表及各届的核验报告生成 `_data/conference_archive.json`。导出字段包含届次、题录和摘要计数及公开来源。默认使用追踪名单的核对日期作为截止日。当年会议在会期结束后进入档案，日期未确认的当年会议待补日期后再收录。

双语研究趋势摘要单独维护在 `_data/conference_review.yml`。更新时同步核对中文与英文中的统计时间、会议范围、分母和代表论文链接。

### 同步逐篇论文

刷新往期回顾后，运行下列命令从相同的核验版本同步题名、作者、论文来源和已知的撤稿或非研究类型标记。每届各有一份 JSON，网站在选中届次时加载对应文件。

```sh
python3 -B tools/export_conference_papers.py "/path/to/meeting-tracker"
```

GitHub Pages 构建使用 `assets/conference-papers/` 下的题录。需要在本机阅读与检索已收录的摘要时，将摘要版本导出到仓库外的预览目录。

```sh
python3 -B tools/export_conference_papers.py "/path/to/meeting-tracker" \
  --include-abstracts --output-dir /tmp/research-site-preview/conference-papers-preview
```

在仓库外另存 `/tmp/research-site-preview.yml`，为本地构建指定摘要数据路径。

```yaml
conference_papers_path: /conference-papers-preview/
conference_papers_has_abstracts: true
keep_files:
  - .git
  - .svn
  - conference-papers-preview
```

```sh
bundle exec jekyll serve --config _config.yml,/tmp/research-site-preview.yml \
  --destination /tmp/research-site-preview
```
