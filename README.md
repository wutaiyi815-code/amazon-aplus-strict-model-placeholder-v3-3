# Amazon A+ Strict Model Placeholder v3.3

面向服装商品的 Amazon A+ 同步逐 SKU 工作流。它读取根目录模板、每个 SKU 的商品属性表及商品图片，完成全量视觉分类、模特身份锁定、文案与模块规划、参考图分配、可选网红图生成、A+ 模块生成、拼接和根目录汇总。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 名称 | `amazon-aplus-strict-model-placeholder-v3-3` |
| 类型 | Codex Skill 与 Python 工作流脚本 |
| 创建时间 | 2026-08-20（源目录时间） |
| 公开发布整理 | 2026-09-14 |
| 版本 | `2026.09.14` |
| 入口 | [SKILL.md](SKILL.md) |
| 状态 | 可用；生成步骤需要外部模型服务 |

## 目标与适用场景

适用于一个根目录包含多个服装 SKU，需要根据统一 `模板.txt` 生成 Amazon A+ 模块的任务。它强调同一 SKU 的模特身份和性别一致、Excel 文案归属、模块级参考图最小化、逐 SKU 同步执行、错误恢复及输出核验。

不适用于把多个 SKU 合并成一次生成请求、仅凭文件名判断图片角色、跳过人工视觉核对，或没有根模板和商品属性表的自由创作任务。

## 严格输入格式

推荐并受工作流直接支持的目录结构如下：

```text
<ROOT>/
  模板.txt
  LOGO/                         # 可选：按品牌名提供共享 LOGO
    <品牌名>.png
  <SKU-1>/                     # 必须是 ROOT 的直接子文件夹
    1-产品属性表.xlsx
    <商品图片>
    素材/                       # 可选；会纳入视觉分析
    上身/                       # 可选；会纳入视觉分析
    上身1/                      # 可选；会纳入视觉分析
    LOGO.png                    # 可选：SKU 本地 LOGO
  <SKU-2>/
    ...
```

### 根目录与 SKU

- `<ROOT>` 必须存在；每个待处理商品必须是其直接子文件夹，文件夹名就是命令中的精确 SKU 名。
- `--product` 每次只能传一个直接子 SKU 文件夹名。禁止逗号分隔多个 SKU、整个根目录批量提交或在一个隐藏循环中连续生图。
- 根级 `LOGO`、`输出结果*`、备份目录和 `_aplus*` 工作目录不视为 SKU。
- `模板.txt` 位于根目录。模板应写明模块数量、单模块尺寸和各 Section/Module 指令；解析器支持 `Section 1`、`Module 1`、`模块 1` 等编号行。

### Excel 属性表

- 每个 SKU 文件夹必须包含一个属性工作簿。优先使用精确文件名 `1-产品属性表.xlsx`；如果不存在，则按文件名排序使用第一个非 `~$` 临时工作簿。
- 支持 `.xlsx`、`.xlsm`、`.xltx`、`.xltm`，读取活动工作表的全部物理行。
- 推荐使用“字段名在第一列、值在第二列”的键值结构。商品类型、颜色、版型、面料、卖点、品牌、目标顾客及 `occasion_N` 等字段应使用稳定且唯一的名称。
- `Section N Headline`、`Section N Copy` 等模块文案只属于对应的 Section N，不能跨模块复用。空白字段允许工作流按模板和商品事实补写。
- 所有工作开始前会删除键名为 `color_options` 的整行；发生删除时，脚本会先在根目录 `_aplus_color_options_backups` 中备份工作簿。

### 图片格式与筛选

- 核心参考图分配支持 `.jpg`、`.jpeg`、`.png`、`.webp`；部分接触表和简报脚本还可读取 `.bmp`、`.tif`、`.tiff`。为确保全流程一致，推荐统一使用 JPG、PNG 或 WEBP。
- 图片可以位于 SKU 根目录及 `素材`、`上身`、`上身1`。视觉角色必须通过图像内容判断，不能通过文件名或文件夹名猜测。
- `弃用`、`过程文件`、`生成结果`、`输出结果`、`备份`、`备份目录`，以及 `_aplus*`、`_influencer*` 工作目录中的图片不得作为当前参考图。
- 不要求输入图片使用固定编号命名；但路径必须属于当前 SKU，且同名文件应避免造成歧义。
- 图片应清晰呈现服装轮廓、颜色、印花、面料、前后面和模特身份。无法识别的图片会阻断严格参考图规划。

### 模块尺寸与数量

- 模块数量和尺寸以当前根目录的 `模板.txt` 为准，生成结果必须逐模块核验。
- 随附的 [assets/module_prompt_template.txt](assets/module_prompt_template.txt) 是 7 个模块的示例：单模块 `1464 × 600 px`，拼接后为 `1464 × 4200 px`。只有采用该模板时这些尺寸才是硬要求。
- 网红自拍默认示例输出为 `4:5`、`2K`；实际生成命令可按服务支持范围调整。

### 参考图顺序合同

- 所有可用图片先被汇总为一个带标签的 SKU 接触表，再由用户选择的分析模型一次性分类；`aigc_model_view_tags.json` 必须完整覆盖允许图片。
- 模特模块必须携带已确认的身份参考图和少量商品准确性参考图；面料、工艺、细节模块应使用平铺或细节图。
- Section 2 必须首先携带简报中记录的 `model_identity_reference`，再在可用时加入一张视觉确认的正面或三分之四 AIGC 模特图。
- 背面人物图必须同时有已确认的正面或三分之四身份参考；否则不得提交该背面人物图。
- LOGO 默认仅在允许品牌露出的 Section 1 使用。共享 LOGO 文件名主体必须与 Excel 品牌值一致，随后复制为 SKU 本地 `LOGO.<ext>`。
- 明确禁止参考图的模块必须提交空参考列表；RunningHub 图生图端点若拒绝空列表，只能使用脚本生成的空白技术种子，并在日志中标记。
- GPT-RH 每次最多 10 张参考图；超出时按模块专用参考和 LOGO 规划后的顺序保留前 10 张。

## 环境与依赖

- Python 3.12 已用于发布验证；建议使用 Python 3.10 或更新版本。
- 安装 [requirements.txt](requirements.txt) 中的 Pillow、openpyxl 和 requests。
- 可选生成服务：ToAPIs 或 RunningHub。凭据通过 `TOAPIS_API_KEY`、`OPENAI_API_KEY`、`RUNNINGHUB_API_KEY` 或 `--api-key` 提供。
- 网红背景库必须通过 `--background-root "<BACKGROUND_ROOT>"` 明确传入。
- 远程生成不要求本地 GPU，但需要网络、有效模型账号及相应额度。

```powershell
python -m pip install -r requirements.txt
```

不要把真实 API 密钥、带签名下载地址、生成日志或业务图片提交到仓库。

## 主要执行顺序

```powershell
python "<SKILL_DIR>\scripts\remove_color_options_rows.py" --root "<ROOT>"
python "<SKILL_DIR>\scripts\analyze_template.py" --template "<ROOT>\模板.txt" --out "<ROOT>\_aplus_creative_template_analysis.json"
python "<SKILL_DIR>\influencer_scripts\prepare_selfie_batch.py" --root "<ROOT>" --background-root "<BACKGROUND_ROOT>"
python "<SKILL_DIR>\scripts\tag_contact_sheet_with_toapi.py" --root "<ROOT>" --product "<ONE_SKU>" --model "<ANALYSIS_MODEL>" --overwrite
python "<SKILL_DIR>\scripts\prepare_aplus_batch.py" --root "<ROOT>"
python "<SKILL_DIR>\scripts\run_sync_product_generation.py" --root "<ROOT>" --product "<ONE_SKU>" --timeout-seconds 3600
```

完整的人工检查点、提示词合同、服务商选择和恢复规则以 [SKILL.md](SKILL.md) 为准。

## 主要交付物

- `<SKU>\_aplus_creative_work\generated_split`：A+ 模块及拼接长图。
- `<ROOT>\输出结果`：每个 SKU 的最终长图副本。
- `<SKU>\_influencer_selfie_work\generated`：可选网红自拍图。
- `aigc_model_view_tags.json`、`module_reference_images.json`：视觉分类与模块参考图合同。
- `module_reference_upload_log.json`、`module_generation_api_log.jsonl`：实际上传参考图及 API 执行日志。
- `_aplus_sync_run_status.json`：根级逐 SKU 状态与恢复依据。

## 发布验证范围

发布前执行 Skill 格式校验、全部 Python 文件语法检查及仓库自带回归测试。真实视觉分析和图片生成需要有效凭据且可能产生费用，不在无凭据发布验证中执行。
