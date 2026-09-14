---
name: amazon-aplus-strict-model-placeholder-v3-3
description: Strict-model Amazon A+ v3.3 synchronous per-SKU workflow with all-allowed-image semantic analysis, exact SKU-relative tags, hard source exclusions, dynamically derived module reference contracts, model-image-authoritative gender, human Section 3 actions, process-tree timeout cleanup, durable root status, API logging, stitching, and root output collection.
---

# Amazon A+ Creative Director With Strict Model Lock And Placeholders

## Purpose

This skill is the v3.3 strict-model placeholder workflow. It preserves the v3.2 prompt, identity, gender, and synchronous per-SKU generation system while tightening semantic image coverage and dynamically deriving each module's reference-image contract.

Do not overwrite:

- `amazon-aplus-creative-director-api`
- `amazon-aplus-creative-director-influencer-api`
- `amazon-aplus-creative-director-influencer-api-strict-model`
- `amazon-influencer-selfie-generator`

## Mandatory Rules

1. In every A+ module that contains a model, preserve the model identity from the supplied model reference images. Match visible face shape, skin tone, hair color/style, body type, age range, expression mood, pose attitude, and styling character. Do not let the API invent a different model unless the product folder has no usable model reference.
2. Classify every allowed image in the SKU semantically before reference allocation, including images in `素材`, `上身`, and `上身1`. Use visual `contains_person`, `subject_type`, `view`, and `detail_types`; never infer any role from a filename or folder name.
3. Before writing `_aplus_creative_work\aplus_creative_brief.md`, choose and record a `Model Identity Lock`:
   - `model_identity_reference`: clearest front-facing model image, not LOGO and not product-only flat lay.
   - `model_identity_notes`: concise description of the reference model's visible face, hair, skin tone, body type, and attitude.
   - `model_identity_policy`: all A+ model scenes must use this same person; do not change ethnicity, gender presentation, face, hair, or body type.
4. The visible gender presentation of the selected `model_identity_reference` is authoritative for all analysis, creative briefs, A+ prompts, Section directions, influencer plans, and generated people. The attribute-table `target_customer` is advisory only and must not override a usable model image. Record `target_gender_source: model_identity_reference`; use the attribute table only as a documented fallback when no usable model gender can be read.
5. Keep the selected model gender consistent throughout the SKU. Do not pause, swap models, or inject gender-conflict wording merely because `target_customer` disagrees with the model image.
6. Every final A+ module prompt must be English-only for rendered text. Strip local Windows paths, Chinese/CJK characters, template notes, and prompt metadata from image-generation prompts. Visible text in generated modules must not contain Chinese, bilingual labels, file paths, or CJK characters.
7. Each A+ module must receive only the reference images it truly needs. Model/fit modules should receive the model identity references plus a small number of garment accuracy references; detail/fabric modules should receive product flat-lay/detail references; influencer modules should receive generated influencer references. Do not pass all product images to every module unless the user explicitly requests that broad reference strategy.
8. Distinguish influencer background templates from color-block placeholders:
   - If a module instruction says only `不需要生成网红图`, `无需生成网红图`, `并不需要生成网红图`, `用于后续替换为网红图`, `背景图`, or `不需要任何文案`, do not run influencer/selfie generation. Generate a style-matched, text-free empty background module for later influencer replacement. Do not generate color blocks unless the template explicitly asks for them.
   - Generate equal-size color-block placeholders only when the instruction explicitly says `占位符`, `等大色块`, `色块`, `placeholder`, or `color blocks`.
9. Build prompts in the same content style as a polished template result: first create one full-page creative prompt, then split it into module prompts. Do not put internal execution wording into image prompts, such as `product folder`, `Excel screenshots`, or long hidden workflow rules that the image model cannot see.
10. If a module prompt or template instruction mentions a model/person/on-body look, send suitable model reference images to the generation API for that module. This overrides rigid reference-role defaults. If the module does not mention a model/person, do not send model references just because they exist.
11. Treat the spreadsheet inside each SPU folder as `1-产品属性表.xlsx` even when the filename is different. Prefer an exact `1-产品属性表.xlsx` match when present; otherwise use the first non-temporary Excel workbook in that SPU folder. If that spreadsheet contains `Section {n}` and matching copy fields for a module, use that spreadsheet copy directly in Section n prompts. If Section n copy is missing, write clear English copy from the module function in `模板.txt` and the product attributes in the spreadsheet.
12. Section 1 is the only default LOGO-exposure section, unless the root `模板.txt`, template analysis, or section prompt explicitly says not to use brand LOGO/wordmark/brand mark as a layout design element. When LOGO is allowed, attach the product-local `LOGO` image to Section 1 generation when available and use a generic supplied-LOGO instruction without embedding reference numbers, filenames, paths, or a reference map in the API prompt. Record the exact LOGO file and upload position only in `module_reference_upload_log.json`. When layout LOGO usage is disabled by the template, do not attach standalone LOGO references, remove LOGO-reference wording from the submitted prompt, and add a clear no-layout-logo instruction plus narrow negative prompt terms. Do not ask the model to erase small logos, labels, embroidery, tags, patches, or brand details that naturally exist on the product references.
13. Section 1 model pose must feel like fashion magazine editorial posing, and Section 1 poses must not repeat exactly across SPUs in the same batch. Assign concrete, vivid pose language deterministically by batch order. Do not send internal cross-product instructions like "do not repeat other SPUs" to the image model.
14. Every generated module must log the reference images submitted and API submit/status/download/error information immediately per module, not only after the full product finishes.
15. After all module images for a product are generated or confirmed present, stitch that product's module images into one long vertical A+ image.
16. Prefer distinct supplied model references across sections only when identity consistency is unaffected. If references are insufficient, reuse the clearest Section 1 model reference; identity consistency has higher priority than cross-module reference uniqueness.
17. Section 2 must always carry the exact `model_identity_reference` recorded in `aplus_creative_brief.md`, then add one semantically confirmed front or three-quarter AIGC model image when available. This identity anchor may not be displaced by the no-repeat allocator.
18. Generated section copy must read like shopper-facing Amazon A+ copy, not image-generation instructions. Avoid prompt-like phrases such as "shown with", "captured through", "true front-and-back product clarity", "module", "layout", or "reference". Use short benefit-led copy that can plausibly appear on the final A+ image.
19. Clean every parsed section title before writing prompt files. Strip stray `?`, `？`, replacement characters, mojibake separators, and repeated `Section {n}` prefixes so final prompts use `Section {n} - <clean title>`.
20. Section 3 and Section 4 fallback headlines must be product-specific. Use product type, color, fit, fabric, feature rows, and product-analysis text to produce concrete shopper-facing headlines. Do not fall back to repeated generic phrases such as `STYLE FROM EVERY ANGLE` or `DETAIL THAT HOLDS UP`.
21. Visible prompt language follows spreadsheet values, not spreadsheet field names. If product attribute values are German, generate German visible-copy instructions, German fallback headline/copy, and a German-friendly negative prompt. Preserve German spelling, capitalization, and umlauts. Default to English only when values are English.
22. After stitching each SPU long image, create `<ROOT>\输出结果` when needed and copy the stitched long image there with the filename unchanged.
23. If the spreadsheet contains a plain `Section {n}` row, use that row's value directly as the module `Copy` field. Do not split it into Headline/Copy, do not summarize it, and do not translate it unless the spreadsheet itself provides a translated value.
24. Prompt language follows `marketplace` first. `DE`, `AT`, and `CH` generate German module prompts and German fallback visible copy; `US`, `UK`, `CA`, and `AU` keep English prompts and English fallback visible copy. If `marketplace` is missing, fall back to spreadsheet value-language detection.
25. A back-view model reference is allowed only as `front person + back view`: pair it with a supplied front or three-quarter person reference, preferably the brief identity anchor. Never use a back-view image alone to lock identity. If no front/three-quarter companion exists, omit the back view.
26. Fallback visible copy, especially for Section 3 and Section 4, must read like shopper-facing advertising copy rather than module/layout explanation. Avoid phrases such as `product views`, `views show`, `front and back views`, `on-body and product views`, `in context`, `module`, `layout`, and `reference`. Convert these into benefit-led copy about styling value, comfort, fit, construction, graphic impact, texture, or everyday use.
27. During the explicitly selected model analysis, tag every allowed SKU image before module allocation, including `素材`, `上身`, and `上身1`. Each tag must include `contains_person`, `subject_type`, `gender_presentation`, `view`, `framing`, `usable_for_identity`, `identity_quality`, and `detail_types`. Reference allocation must use only these visual semantic labels.
28. If the final reference list submitted to the image API contains no model/person/on-body reference image, clean the entire submitted prompt before API submission. Remove `Reference note` model-reference claims and any strong model-reference cues from Visual Direction, Product Information, Product Accuracy, or other sections, then add an explicit no-people/no-random-model instruction.
29. Product-category detection for fallback headlines/copy must prioritize explicit spreadsheet fields such as `Product type`, then use word-boundary matching. Never classify by loose substring matches such as `hat` inside `that`; this causes unrelated SPUs to inherit cap/hat copy.
30. If the spreadsheet does not provide Section n copy, generate product-specific `Headline`, `Copy`, and `Visual Direction` from the current root `模板.txt` module function plus `product_type`, `fit`, `fabric`, `feature`, color, marketplace language, and the model-derived `target_gender`. Keep spreadsheet `target_customer` advisory and exclude it from API prompt gender/casting logic whenever a usable model gender exists. Do not use fixed repeated fallback text for a section number or broad product category.
31. Template-level no-logo instructions have higher priority than default Section 1 logo behavior. Treat phrases such as `不要出现品牌LOGO`, `不出现LOGO`, `不露出LOGO`, `无LOGO`, `禁止LOGO`, `no logo`, `without logo`, `do not show logo`, and `no wordmark` as hard constraints against using standalone LOGO assets or logo-like marks as layout design elements. In that mode, generated prompts must not mention attached LOGO references and submitted reference lists must exclude standalone `LOGO.*` files. The image prompt should say: `Do not add, enlarge, redesign, or use any brand LOGO, wordmark, brand mark, brand badge, or logo-like emblem as a separate layout design element. Preserve any small logo, label, embroidery, tag, patch, or brand detail that already exists naturally on the product reference images as part of the actual garment/product.`
32. Final module prompt files must be prompt-ready API text, not intermediate analysis briefs. Do not include `Product Folder`, `Reference Images To Inspect`, `Logo References`, `Visual Observations`, local/UNC paths, draft placeholders, or other workflow-only inspection sections in `module_prompts` or submitted API prompts. Never append `Attached Reference Image Map:` or any filename/path list to the API prompt. Record exact submitted reference filenames only in `module_reference_upload_log.json`. The prompt saved in `api_submitted_prompts` must match the text sent to the API.
33. If the root `模板.txt` or a section instruction says a module should not upload/send/use reference images, treat that as a hard per-section rule. Recognize phrases such as `不要上传参考图`, `不上传参考图`, `无需参考图`, `不要发送参考图`, `不发送参考图`, `不传参考图`, `no reference images`, `without reference images`, `do not upload reference images`, and `do not send reference images`. For that section, `module_reference_images.json` must have no references, API `imageUrls` / `image_urls` must be empty, no LOGO/model/product references should be uploaded, and the final submitted prompt must not mention attached/supplied reference images.
34. Section 1 must never use supplied model back-view images as model references. If the model pool contains front/three-quarter/side/full-body references, Section 1 must select from those only. If only back-view model references exist, omit model identity references for Section 1 rather than using a back-view model reference.
35. If Section 3 shares any final model reference with Section 2, the main agent must inspect that SKU, its Section 3 layout, garment visibility needs, and selected references, then write one bespoke `Section 3 fashion action:` block. Do not select, rotate, or synthesize an action from a safe/category action library. The action must specify concrete body mechanics, gaze or torso direction, and how hands/limbs avoid covering important product features. The reference builder only validates this human-authored block and must stop before generation when it is missing or generic.
36. Every module `Visual Direction` must begin with a concrete composition/layout task derived from the current root `模板.txt` Section n instruction, then add product-specific visual direction from the spreadsheet and image analysis. Preserve dynamic template meaning: hero/banner sections should say hero/banner composition; multi-angle model sections should say multiple model angles in one module; model-plus-flat-lay sections should say model context plus front/back flat-lay product proof; detail/macro sections should say people-free detail/macro collage when the template says no people; influencer-replacement background sections should say text-free, people-free, style-matched background with no social UI or color blocks unless explicitly requested.
37. Headline and Copy generation uses a hybrid copy system. GPT/Gemini analysis should propose shopper-facing A+ copy from the actual `product_type`, `fit`, `fabric`, `color`, `feature_*`, model mood, and current Section task; local prompt-building rules then enforce product-specific fallback copy and same-SKU de-duplication. Do not use fixed category sentences such as one generic zip-hoodie/cardigan line across multiple SPUs. Within one SKU, every Section Headline and Copy must use a distinct selling angle unless the spreadsheet explicitly supplied identical copy; spreadsheet-authored text remains authoritative, while generated text is rewritten when duplicate or near-duplicate content is detected.
38. Determine one normalized product category per SKU for product copy and reference needs. Product category must not drive a Section 3 action library; overlap actions are authored visually by the main agent for the actual Section 3 composition.
39. Orchestrate every multi-SPU generation batch synchronously with `run_sync_product_generation.py`, exactly one `--product "<ONE_PRODUCT_FOLDER_NAME>"` per command. Apply an explicit finite timeout, wait for terminal return, close the execution cell, confirm no child process remains, and only then launch the next SKU. Never generate a whole root, pass comma-separated names, or hide several SKU calls inside one PowerShell loop or wrapper invocation.
40. After every SPU process, verify its expected module count, module dimensions, generation logs, stitched long image, and root `输出结果` copy before marking that SPU complete. Confirm that no generator child process remains before continuing. If a command times out or the task is interrupted, inspect the saved artifacts and logs, then resume only the incomplete SPU and missing modules. If all artifacts are complete but a yielded execution cell remains open, terminate that stale cell explicitly instead of leaving the Codex task running.
41. At task start, before any preparation or analysis, remove every `color_options` row from every direct SKU attribute workbook. Back up each changed workbook and write the root audit JSON. Stop if any workbook removal or verification fails.
42. Creative-brief preparation and module construction must use the same shared, normal-mode Excel reader. Always load with `read_only=False` and iterate the physical worksheet rows. Never use a read-only streaming worksheet for either stage, because stale worksheet dimension metadata can truncate valid cells to `A1`.
43. Excel `Section N Headline` and `Section N Copy` belong only to Section N. Override only the matching field in the matching section, and leave Gemini-generated Headline or Copy unchanged when the corresponding Excel cell is empty. After resolution, validate section ownership and cross-section duplicates. If any authoritative Section N Headline/Copy appears in another section, stop before reference planning or image generation.
44. Do not address missing rendered copy by adding fixed text-area percentages, mandatory split layouts, rigid text-safe blocks, or extra design restrictions. Keep the original design freedom. Treat a missing rendered title/copy as image-output QA and regenerate that module when necessary.
45. `Suggested Visual Baseline` is a main-agent visual-analysis deliverable, not a scripted or Gemini-composed field. For every SKU, inspect its model images and product/flat-lay/detail images yourself, then write four genuinely product-specific dynamic lines. Do not create baselines by rules, palettes, category templates, string combinations, scripts, or copied sibling wording. Keep the `Style balance` line exactly fixed. If visual inspection cannot be completed, stop instead of fabricating a baseline.
46. Do not create or send a `Text / Callouts:` block for any Section, even when a brief or spreadsheet supplies callout content. Use only `Headline` and `Copy` for shopper-facing text. The module builder must omit the field, and API submission must defensively remove it from legacy module prompts while preserving any following `Negative Prompt:` block.
47. Analyze all allowed images through one labeled contact sheet and one request to the explicitly selected model for each exact SKU. Require exact manifest-ID coverage and valid fields, write results atomically, and reject every heuristic tag. Never silently downgrade an API failure to filename or folder inference.
48. Hard-exclude every image beneath `弃用`, `过程文件`, `生成结果`, `输出结果`, any directory whose name contains `备份` or `backup`, and workflow directories beginning `_aplus` or `_influencer`. These paths may not enter contact sheets, tags, role maps, module maps, or API uploads.
49. Store and resolve semantic tags only by the image's complete SKU-relative path. Basename matching and filename fallback are forbidden, including when two folders contain the same filename.
50. Every business reference must resolve to an existing allowed image inside the current SKU. Reject outside paths, stale paths from another SKU, and paths beneath hard-excluded directories before upload.
51. Rebuild `module_reference_images.json` from an empty mapping every time. Every current prompt filename must receive a fresh entry, including an empty list for a verified no-reference module. Never preserve historical entries when new selection fails.
52. Derive each module's image-role contract dynamically from the current template instruction and module prompt, not from its section number. Then select only from semantically analyzed images and hard-validate sources and roles before generation.
53. A model multi-angle/front-side-back contract requires a front model and a back model; a semantically confirmed side or three-quarter model is optional when unavailable. A model-plus-flat-lay-front/back contract requires a front identity model, a flat-lay product front, and a flat-lay product back.
54. A fabric/craft/detail close-up contract requires at least one visually confirmed fabric, neckline, cuff, zipper, print, stitching, hem, pocket, hardware, closure, or other genuine detail image. Prefer eligible images from `素材`, then `上身`/`上身1`, without using the folder name as semantic evidence.
55. A pure-background/no-reference contract must contain an empty reference list and upload no business reference image. Provider-required blank technical seeds are not business references and must be logged separately.
48. Write analysis and generation terminal states to `<ROOT>\_aplus_sync_run_status.json`. A SKU may advance only when the current stage is completed or intentionally resumed from an explicit failed, interrupted, or timed-out state.
49. On timeout or interruption, terminate the complete generator child process tree. Set the outer shell/tool timeout at least 60 seconds longer than the wrapper's `--timeout-seconds` so cleanup can finish. A shell/tool timeout without process-tree verification is not cleanup, and no yielded execution cell may remain open after a command finishes.
50. Keep API keys only in process environment variables. Never store them in status JSON, provider state, prompts, command files, logs, or generated artifacts.

## Workflow

1. Confirm the root directory. Treat every direct child SKU directory as one product. Remove `color_options` rows before any other task step:

```powershell
python "<SKILL_DIR>\scripts\remove_color_options_rows.py" --root "<ROOT>"
```

Confirm `_aplus_color_options_removal.json` reports no errors. Each changed workbook must have a timestamped copy under `_aplus_color_options_backups`.

2. Analyze the root template:

```powershell
python "<SKILL_DIR>\scripts\analyze_template.py" `
  --template "<ROOT>\模板.txt" `
  --out "<ROOT>\_aplus_creative_template_analysis.json"
```

3. Check `modules[*].instruction` in `_aplus_creative_template_analysis.json`.
   - If an instruction contains `占位符`, `等大色块`, `色块`, `placeholder`, or `color blocks`, mark that module as `placeholder_blocks`. Do not generate influencer selfies for it.
   - If an instruction contains `不需要生成网红图`, `无需生成网红图`, `并不需要生成网红图`, `用于后续替换为网红图`, `背景图`, or `不需要任何文案` without explicit color-block wording, mark it as an influencer replacement background. Do not generate influencer selfies, people, social screenshots, color blocks, or visible copy for it.
   - If an instruction contains `网红图`, `网红`, `UGC`, or `influencer` and does not contain placeholder/no-generation wording, generate influencer selfie images before A+ modules.

4. Prepare influencer selfie plans:

```powershell
python "<SKILL_DIR>\influencer_scripts\prepare_selfie_batch.py" `
  --root "<ROOT>" `
  --background-root "<BACKGROUND_ROOT>"
```

Use the user-supplied `--background-root` directory as the background library. If it is not supplied, ask the user for the background image folder; never assume a machine-specific path.

After preparation, inspect product and background contact sheets. Fill or correct each product's `_influencer_selfie_work\selfie_plan.json`:

- `front_model_reference`: best model/product image for Image 1, never LOGO.
- `target_gender`: women, men, or unisex, derived from the selected model image when usable.
- `target_gender_source`: `model_identity_reference` when the model tag is usable; `attribute_table_fallback` only when model gender is unavailable.
- `target_customer_reference`: preserved as advisory spreadsheet metadata only.
- `model_identity_reference`: clearest supplied model image when one exists.
- `model_identity_notes`: visible model identity details for A+ modules.
- `product_subject`: top, T-shirt, pants, sweatpants, skirt, dress, hoodie, etc.
- `product_accuracy_notes`: exact garment details to preserve.
- `background_reference` and `background_reason` for each occasion.
- Avoid reusing the same background mapping mechanically across products unless the user requests a controlled repeat.

5. Build final influencer prompts:

```powershell
python "<SKILL_DIR>\influencer_scripts\build_selfie_prompts.py" `
  --root "<ROOT>" `
  --template "<SKILL_DIR>\assets\selfie_prompt_template.txt"
```

The prompt builder enforces model-derived `target_gender`. A conflicting spreadsheet `target_customer` must not change the selected model's gender in influencer or A+ prompts.

6. Ask the user for generation method and API supplier:

```text
请选择生图方式：
1. Codex 内置 image_gen 工具
2. API 方式：GPT-ToAPI（原 ToAPIs gpt-image-2）
3. API 方式：GPT-RH（RunningHub rhart-image-g-2-official）
```

If the user chooses API, ask which supplier to use before running generation. Use API keys from `--api-key`, supplier-specific environment variables, or an interactive prompt. Do not write secrets into files.

- GPT-ToAPI uses `TOAPIS_API_KEY` or `OPENAI_API_KEY`.
- GPT-RH uses `RUNNINGHUB_API_KEY`.
- GPT-RH default `quality` is `medium`; allowed values are `low`, `medium`, and `high`.

Also ask for the text/image analysis model before building or revising product briefs:

```text
Provide the exact ToAPIs text/image analysis model ID, for example `gpt-5.6-sol` or a supported Gemini model.
```

Use `TOAPIS_API_KEY` or `OPENAI_API_KEY` and pass the exact selected model to the helper script below for reference-image/product analysis:

```powershell
python "<SKILL_DIR>\scripts\analyze_reference_with_toapi_gpt55.py" `
  --model "<USER_SELECTED_ANALYSIS_MODEL>" `
  --prompt "Analyze these product and model reference images for Amazon A+ planning..." `
  --image "<PRODUCT_OR_MODEL_IMAGE>" `
  --out "<PRODUCT>\_aplus_creative_work\gpt55_reference_analysis.json"
```

Use the selected-model analysis result as product truth and visual-baseline input, but do not copy raw analysis metadata into image-generation prompts.

After the user chooses the analysis model, process one exact SKU at a time. Create one labeled contact sheet for every allowed image in the SKU, including `素材`, `上身`, and `上身1` while applying all hard exclusions; send one request to that model and validate complete JSON coverage before building module reference maps:

```powershell
python "<SKILL_DIR>\scripts\tag_contact_sheet_with_toapi.py" `
  --root "<ROOT>" `
  --product "<ONE_PRODUCT_FOLDER_NAME>" `
  --model "<USER_SELECTED_ANALYSIS_MODEL>" `
  --request-timeout 300 `
  --overwrite
```

Set `TOAPIS_API_KEY` or `OPENAI_API_KEY` in the process environment. Do not pass or save the key when the environment is available. Issue one separate shell/tool invocation per SKU and wait for it to return; do not hide multiple SKU analyses inside a loop.

The script writes `analysis_contact_sheet.jpg`, `analysis_contact_sheet_manifest.json`, `contact_sheet_analysis_raw.json`, validated `aigc_model_view_tags.json`, and root `_aplus_sync_run_status.json`. It fails without replacing tags when the request times out, JSON is invalid, any manifest ID is missing/extra, or a field is invalid. Do not use the legacy per-image helper; it cannot satisfy v3.3's all-image, single-contact-sheet, no-heuristic contract.

Each `aigc_model_view_tags.json` entry must include at least:

- `contains_person`: boolean based on visible image content.
- `subject_type`: `model_person`, `product_flatlay`, `product_detail`, or `unknown`.
- `gender_presentation`: `woman`, `man`, `ambiguous`, or `unknown`.
- `view`: `front`, `three_quarter`, `side`, `back`, `detail`, or `unknown`.
- `framing`: `full_body`, `half_body`, `upper_body`, `closeup`, or `unknown`.
- `usable_for_identity`: boolean.
- `identity_quality`: `high`, `medium`, `low`, or `unknown`.

Every tag must record `source` equal to the explicitly selected analysis model. No tag with `source: heuristic` may proceed to reference planning or generation. Only validated visual analysis may promote an 上身 image to `model_person`.

For API influencer generation:

```powershell
python "<SKILL_DIR>\influencer_scripts\generate_selfies_toapi.py" `
  --root "<ROOT>" `
  --size "4:5" `
  --resolution "2K"
```

7. Run normal A+ preparation:

```powershell
python "<SKILL_DIR>\scripts\prepare_aplus_batch.py" --root "<ROOT>"
```

8. Inspect product references and create each product's `_aplus_creative_work\aplus_creative_brief.md`.

The brief must include:

- Product truth from Excel and image inspection.
- `Model Identity Lock` with selected reference path and visible identity notes.
- Product accuracy notes for exact garment construction, color, print, fabric, and fit.
- Section plans matching the template module count.
- For model sections: require the same supplied model identity.
- For influencer sections: say generated influencer images should be the module's main UGC/photo-tile content.
- For explicit color-block placeholder sections: say no influencer photos, selfies, people, UGC screenshots, or social posts should be generated. The module should use the same global style and show exactly the requested equal-size color-block placeholders.
- For influencer replacement background sections: say no influencer photos, selfies, people, UGC screenshots, social posts, color blocks, or visible copy should be generated. The module should be a clean style-matched background/layout image, ready for later influencer replacement.
- Do not write internal correction language into image-generation prompts. Avoid phrases like "replace the template's original men's Liquid Metal tee" or any mention of irrelevant template products, wrong genders, or obsolete graphics. Final prompts should describe only the actual product and the current module.
- Keep each module prompt focused on that module. Use shared product truth, model identity lock, and visual system notes for consistency; do not append the full creative brief or other modules' directions into every module prompt.
- Preserve template-level design execution requirements from `模板.txt`, especially typography, font family, exact supplied LOGO usage, and brand-asset consistency. Convert them into direct image-generation instructions in both the full-page prompt and every split module prompt.
- If `模板.txt` says no brand LOGO/wordmark/brand mark should appear, this overrides any default Section 1 standalone LOGO behavior. Keep typography and layout requirements, remove standalone LOGO-reference wording, add an explicit no-layout-logo rule, and preserve product-reference logos, labels, embroidery, tags, patches, and brand details that are physically part of the garment/product.
- If `模板.txt` says a section should not upload or use reference images, preserve that section-level instruction in the prompt as a direct no-reference rule and remove wording such as `attached product reference images`, `supplied references`, model-reference notes, LOGO-reference notes, and attached-reference map expectations for that section.
- Write final prompt-ready copy in English. Do not carry Chinese template wording, Chinese file paths, or Chinese labels into renderable copy.
- Create a contact sheet that includes the SKU's usable model images plus product flat lays/details, inspect it yourself at readable resolution, and write this exact block in the brief:

```text
## Suggested Visual Baseline
Main color: <manually observed product-specific direction>
Supporting colors: <manually observed product-specific direction>
Background: <manually chosen product-specific scene direction>
Texture: <manually observed material and mood direction>
Style balance: 70% Amazon information clarity + 30% light streetwear editorial atmosphere
```

- The first four lines must be independently written for this SKU from the inspected images. Do not ask Gemini or a script to invent them, and do not reuse a rule-combined baseline. The prompt builder rejects missing/incomplete baselines, a changed Style balance line, and near-duplicate sibling baselines.

Save the twelve (or current batch count) human-written baseline objects in `<ROOT>\_aplus_manual_visual_baselines.json`, keyed by exact SKU folder name, using the five exact field names above. Then let the same user-selected analysis model perform the remaining image analysis and creative-copy work while pinning those human values verbatim:

```powershell
python "<SKILL_DIR>\scripts\generate_creative_briefs_gemini.py" `
  --root "<ROOT>" `
  --model "<USER_SELECTED_ANALYSIS_MODEL>" `
  --baseline-file "<ROOT>\_aplus_manual_visual_baselines.json" `
  --overwrite
```

The script may send the contact sheet plus selected model/product references to the selected model, but it must exclude prior output images and may not rewrite the human baseline. It must record the exact selected model and must not add fixed text-safe percentages, rigid split layouts, or other copy-missing workarounds to the creative brief.

9. Build A+ module prompts:

```powershell
python "<SKILL_DIR>\scripts\build_creative_module_prompts.py" `
  --creative-brief "<PRODUCT>\_aplus_creative_work\aplus_creative_brief.md" `
  --template-analysis "<ROOT>\_aplus_creative_template_analysis.json"
```

This script writes:

- `<product>\_aplus_creative_work\aplus_full_prompt.txt`: one full-page prompt in the same structure as the analyzed template result.
- `<product>\_aplus_creative_work\module_prompts\section-XX-*.txt`: per-module prompts split from the full-page direction.

The module prompts should stay close to the template-result format: one complete overall prompt first, then split section prompts with canvas specification, `Suggested Visual Baseline`, template design requirements, product information, section headline/copy, visual direction, product accuracy, optional reference note, and negative prompt. Avoid verbose internal-only constraints. `module_prompts` must be clean API-ready prompt bodies, not creative-brief drafts.

Prompt cleanliness rules:

- Do not include `Copy Source`, `文案来源`, `Generated from template function and product attributes`, spreadsheet/file names, local paths, or workflow metadata in prompts sent to image generation.
- Do not include draft-only sections such as `Product Folder`, `Reference Images To Inspect`, `Logo References`, `Visual Observations`, image path lists, or inspection placeholders. Product Information should be a concise product-fact summary only.
- Do not include internal product-truth wording such as `Use only verified product details from the spreadsheet`, `source references`, or `Module purpose from template` in prompts sent to image generation. Convert those into concrete visible product facts, such as exact color, fit, fabric, print, logo placement, silhouette, and construction details.
- Do not send cross-product operational rules to the image model. Section 1 may retain its v3 editorial pose handling; when Section 3 overlaps Section 2 references, use only the bespoke main-agent-authored `Section 3 fashion action:` block for that SKU.
- Parse spreadsheet copy such as `Headline: ... / Subheading: ...` into separate `Headline` and `Copy` fields. Never duplicate the same long line in both fields.
- Generate product-specific headlines, copy, and visual direction when Section n copy or product-ready direction is absent. Use product type, color, fit, fabric, print/detail, model mood, and the current template module purpose.
- Use the hybrid copy system for generated text: GPT/Gemini may polish the language, but local rules must first choose a product/section-specific selling angle and then de-duplicate Headline and Copy within the same SKU. If two generated sections produce the same or near-same text, rewrite the later generated section using a different product attribute or section function. Do not alter spreadsheet-authored Section copy for de-duplication.
- Section titles must be cleaned before output. Use `Section n - Title`, never mojibake separators or a stray question mark after `Section n`.
- Section 3 and Section 4 fallback headlines must be concrete to the product/category/detail, not generic repeated titles.
- Shopper-facing copy must be concise and benefit-led. It should sound like final A+ page text, not a camera/layout instruction.
- If non-spreadsheet copy sounds like a module explanation, such as describing product views, references, layout, or what the image shows, replace it with a cleaner advertising line. Keep spreadsheet-authored Section copy unchanged.
- If spreadsheet values are German, prompts must instruct the image model to render German copy and avoid English visible labels. German fallback copy is used when Section n copy is missing.
- If the spreadsheet has a plain `Section n` row, write that row value directly under `Copy:` in the final module prompt.
- Use `marketplace` as the primary language switch: DE/AT/CH -> German prompt output; US/UK/CA/AU -> English prompt output.
- Do not output `Text / Callouts:` in full-page, module, or API-submitted prompts. Ignore any legacy brief/spreadsheet callout field; shopper-facing text belongs in `Headline` and `Copy` only.
- Do not output `Attached Reference Image Map:` or raw reference filenames/paths in API prompts. Keep exact file mapping only in `module_reference_upload_log.json`.
- Insert the manually written `Suggested Visual Baseline` from the creative brief verbatim. Do not derive or rewrite it during module construction.

Excel section-copy behavior:

- The SPU folder's Excel workbook is the product attribute table even if the filename is not `1-产品属性表.xlsx`. If the spreadsheet contains a row or key like `Section 1`, `Section 2`, etc. and neighboring copy/title/callout cells, that copy is authoritative for the matching module.
- Both creative-brief preparation and module construction must call the shared normal-mode reader in `scripts\excel_reader.py`; do not add a second workbook-reading path and do not use `read_only=True`.
- If the spreadsheet contains `Section n Headline`, `Section n Title`, `Section n 主标题`, or equivalent title rows, use that value directly as the module `Headline`. If it contains plain `Section n` or copy/body/subheading rows, use that value as the module `Copy` according to the parsing rules above.
- Apply each non-empty Excel field only to its own Section n and its own field. An empty Excel Headline or Copy does not erase or replace Gemini-generated text. Before writing module prompts, hard-fail if authoritative Section n text appears in any other section; after generated-text resolution, hard-fail unresolved cross-section duplicate Headline/Copy.
- After an ownership hard failure, do not continue to reference planning or image generation. If the misplaced destination field is not itself Excel-authored, regenerate only that destination field with `repair_cross_section_copy_gemini.py --model "<USER_SELECTED_ANALYSIS_MODEL>"`, then rerun the complete module builder and validators. Never rewrite the authoritative Excel-owned source field.
- If the spreadsheet does not provide Section n copy, infer concise renderable copy from the current `模板.txt` Section n function and product attributes. Do not assume Section 2/3/4 always means the same thing across templates, and do not reuse one category-level fallback sentence across multiple SPUs with different product details.
- Section fallback copy and visual direction must be based on the template's actual Section n function for this run: banner/hero, fit/silhouette, model plus flat-lay front/back, detail/macro/fabric, lifestyle/gift, or text-free replacement background. For example, a fit section should discuss cap adjustability, hoodie layering volume, or pants waistband/leg movement depending on the product.
- `Visual Direction` must include the section composition task inferred from the current `模板.txt`, not only a generic product/style statement. Write the layout task as direct API-ready wording, such as a hero banner, multi-angle model board, model-plus-flat-lay composition, people-free macro collage, or text-free replacement background.
- Track copy provenance internally for validation, but never render source labels or spreadsheet filenames in API prompt files.

Section 1 banner behavior:

- Treat Section 1 as the brand/logo hero banner unless the template explicitly disables LOGO exposure.
- Attach product-local `LOGO.*` to Section 1 even if the prompt does not contain the word `logo`, but only when the template does not disable LOGO exposure.
- Record the LOGO filename and upload position in `module_reference_upload_log.json`; do not append a numbered LOGO map or filename to the API prompt.
- Use fashion-magazine editorial pose direction. Across products in the same root batch, rotate concrete pose descriptions so two SPUs do not receive the same default pose. The prompt should describe only the chosen pose, not the batch comparison rule.

10. Inject generated influencer images into A+ prompts only for true influencer sections:

```powershell
python "<SKILL_DIR>\scripts\inject_influencer_sections.py" `
  --root "<ROOT>" `
  --template-analysis "<ROOT>\_aplus_creative_template_analysis.json"
```

This creates `<product>\_aplus_creative_work\module_reference_images.json` and appends influencer UGC layout instructions to affected section prompts.

Explicit placeholder/color-block sections are skipped by this script and handled by the normal module prompt plus `build_module_reference_images.py` as `placeholder_blocks`. No-influencer background sections are also skipped by influencer generation, but are handled as `influencer_background`, not as color blocks.

11. Build per-module reference image maps:

```powershell
python "<SKILL_DIR>\scripts\build_module_reference_images.py" `
  --root "<ROOT>" `
  --template-analysis "<ROOT>\_aplus_creative_template_analysis.json"
```

This reads the original template analysis plus each module prompt, detects Chinese and English module semantics, and writes:

- `<product>\_aplus_creative_work\reference_image_roles.json`: explicit role for each source image.
- `<product>\_aplus_creative_work\module_reference_requirements.json`: explicit module role and required reference roles.
- `<product>\_aplus_creative_work\module_reference_images.json`: final image list to upload for each module.

It detects module intent from terms such as `首图`, `模特`, `版型`, `廓形`, `正反面`, `印花`, `面料`, `细节`, `工艺`, `网红图`, `用于后续替换为网红图`, `背景图`, `占位符`, `色块`, plus English equivalents such as `hero`, `model`, `fit`, `silhouette`, `front-back`, `graphic`, `fabric`, `construction`, `UGC`, `influencer`, `background only`, `placeholder`, and `color blocks`.

The final mapping ensures each module sends only the references it needs:

- Hero/model/fit sections: selected model identity references plus a few garment accuracy refs.
- Any section whose prompt or template instruction mentions model/person/on-body styling: model identity references plus needed product refs.
- Graphic/detail/fabric sections: product flat-lay, back-view, and macro/detail refs.
- Influencer sections: generated influencer selfie refs preserved from injection.
- Placeholder sections: product color/detail and brand references only; no influencer images.
- Model reference selection must use `_aplus_creative_work\aigc_model_view_tags.json`. Prefer front/three-quarter and full-body model images for identity-sensitive modules. Treat back-view tags as back-view references even if the filename is unclear.
- Section 2 must include the brief's exact `model_identity_reference` plus a second confirmed front/three-quarter AIGC person image when available.
- If the model pool is short, reuse Section 1 references. Same-person identity consistency outranks cross-section reference de-duplication.
- A back-view reference must be paired with a confirmed front/three-quarter person reference; otherwise remove the back view.

Run the reference builder once. When it reports a Section 2/Section 3 overlap and exits with code 2, inspect that SKU and write a bespoke block into the affected Section 3 prompt:

```text
Section 3 fashion action:
<main-agent-authored action describing body mechanics, gaze/torso direction, and garment-clearance logic for this exact composition>
```

Do not use a safe action library or a category preset. Rerun `build_module_reference_images.py`; generation may continue only after the validator accepts the block.

12. Generate A+ modules one SPU at a time.

First enumerate valid direct-child SPU folders. Exclude operational folders such as `LOGO`, `输出结果*`, root analysis/output folders, backups, and folders whose names begin with `_aplus`. Keep this ordered SPU list as the batch resume checklist.

For a multi-SPU root, issue each command below as a separate shell/tool invocation containing exactly one `--product` value. The synchronous wrapper applies the timeout and owns full process-tree cleanup. Do not run the entire root, a comma-separated subset, or a PowerShell loop in one long-lived execution session.

For GPT-ToAPI, run this once for one SPU:

```powershell
python "<SKILL_DIR>\scripts\run_sync_product_generation.py" `
  --root "<ROOT>" `
  --template-analysis "<ROOT>\_aplus_creative_template_analysis.json" `
  --provider "gpt-toapi" `
  --product "<ONE_PRODUCT_FOLDER_NAME>" `
  --size "21:9" `
  --resolution "2K" `
  --timeout-seconds 1800
```

For GPT-RH / RunningHub, run this once for one SPU:

```powershell
python "<SKILL_DIR>\scripts\run_sync_product_generation.py" `
  --root "<ROOT>" `
  --template-analysis "<ROOT>\_aplus_creative_template_analysis.json" `
  --provider "gpt-rh" `
  --product "<ONE_PRODUCT_FOLDER_NAME>" `
  --size "21:9" `
  --resolution "2K" `
  --quality "<low|medium|high>" `
  --timeout-seconds 1800
```

After each independent SPU command returns:

1. Read the final events in that SPU's `module_generation_api_log.jsonl` and confirm that every expected Section has either a completed image or an explicit error record.
2. Verify the generated module count and dimensions, the stitched long image, and the unchanged-name copy in `<ROOT>\输出结果`.
3. Inspect the complete process command line and confirm that neither `run_sync_product_generation.py` nor its `generate_modules_toapi.py` child remains alive.
4. Close or terminate the completed shell/tool execution session before starting the next SPU. A completed filesystem result is not a reason to leave a yielded execution cell open.
5. On timeout or interruption, confirm `_aplus_sync_run_status.json` records the terminal state, verify that the complete process tree was terminated, audit existing images/logs, and rerun only that incomplete SPU. Preserve completed SPUs. Use `--overwrite` only when the user explicitly requests regeneration.
6. Visually inspect the stitched image. If a non-empty authoritative/generated Headline or Copy is missing from the rendered image, do not change the prompt layout or add text-area constraints. Regenerate only the affected prompt(s) with `--module "section-XX-name" --overwrite`, then restitch and inspect again.

The script may technically accept broader `--product` input, but this skill must always pass one exact SPU folder name per generation command.

Important reference rule for module-specific references:

- Require a freshly rebuilt entry for every current module prompt in `module_reference_images.json`. Pass only those mapped current-SKU references plus a product-local `LOGO` when the module prompt explicitly needs a logo or brand mark. Shared recursive fallback is forbidden.
- Section 1 is an exception: always pass the product `LOGO` image when available and use a generic supplied-LOGO fidelity instruction, unless the template or prompt disables LOGO exposure. Do not expose its number or filename in the prompt.
- Section 1 upload logs must retain the exact LOGO filename and upload position; the API prompt must not contain an `Attached Reference Image Map:` block.
- No-logo template instructions override the two Section 1 LOGO rules above. In no-logo mode, do not upload product `LOGO` images, do not add a Section 1 LOGO reference map, and strip any prompt line that says a LOGO reference is attached.
- If the final reference list submitted to the image API contains no model/on-body reference image, strip model-reference notes such as `Reference note: Use the attached model reference images...` before API submission. Never imply that model references are attached when the request only sends product, detail, background, or LOGO images.
- If the prompt disables reference images for a module, do not upload shared references, module-specific references, or LOGO references for that module. Save `mode: no_reference` and an empty `reference_images` list in `module_reference_upload_log.json`, and save the actual submitted prompt in `api_submitted_prompts`. For RunningHub only, because its image-to-image endpoint rejects empty `imageUrls`, upload one blank technical seed image and explicitly tell the model it is not a product/model/style/LOGO reference; log `runninghub_blank_technical_seed: true`.
- This no-model cleanup must scan the whole submitted prompt, not only one exact `Reference note` phrase. Remove lines that imply attached model references, same-person matching, model identity, face/hair/body matching, model styling, on-body fit, model poses, or other model-reference cues in `Reference note`, `Visual Direction`, `Product Information`, `Product Accuracy`, and similar blocks. Then add a clear instruction that no model/person reference images are attached and the module should not generate random people unless attached references explicitly include a person.
- When a module prompt needs a logo or brand mark, read the brand from the SPU folder's Excel workbook, treating it as `1-产品属性表.xlsx` even if the filename differs. Then look for matching image files in the root-level sibling folder `<ROOT>\LOGO` where the file stem equals the brand name. If a sibling brand logo is found, copy the selected logo into the SPU/product folder as `LOGO.<original extension>` and upload that product-local `LOGO` file to the image API. If no sibling brand logo is found, fall back to existing product-local LOGO images.
- Print the final reference image list for every generated module before submitting it to the API, and write the same per-module list to `<product>\_aplus_creative_work\module_reference_upload_log.json`.
- Write `module_reference_upload_log.json` immediately after planning each module so interrupted runs still keep the reference-image record.
- Use distinct model references where possible, but reuse Section 1 references whenever needed to preserve the same person. Identity consistency outranks de-duplication.
- Section 2 always includes the exact brief `model_identity_reference` and then a confirmed front/three-quarter AIGC companion when available.
- Never submit a back-view model reference without a confirmed front/three-quarter person companion. If no such companion exists, remove the back view.
- Section 1 is stricter than other model sections: remove all back-view model references from Section 1, even when a companion model image exists.
- If Section 3's final model references overlap with Section 2, require and validate a main-agent-authored `Section 3 fashion action:` block. Record `section3_human_fashion_action_required`, `section3_human_fashion_action_validated`, and the shared references in `module_reference_requirements.json`. Never auto-insert an action.
- If a module is marked as influencer / `网红图` and has generated influencer images, pass only generated influencer images plus product `LOGO` if the prompt explicitly needs a logo or brand mark.
- If a module is marked as `placeholder_blocks`, pass only product color/detail and brand references; never pass generated influencer images.
- If a module is marked as `influencer_background`, pass product color/detail and brand references only; never pass generated influencer images, model references, social UI, or color-block instructions.
- Non-influencer modules must use their module-specific references and obey `Model Identity Lock`; do not send all references to all modules.
- GPT-RH uploads local references through `https://www.runninghub.ai/openapi/v2/media/upload/binary`, submits module generation to `https://www.runninghub.ai/openapi/v2/rhart-image-g-2-official/image-to-image`, sends `imageUrls`, `aspectRatio`, `resolution`, and `quality`, and polls task status through `https://www.runninghub.ai/openapi/v2/query` with the returned `taskId`.
- GPT-RH supports at most 10 reference images per request. If a module maps more than 10 references, keep the first 10 after module-specific and LOGO planning.

## Output Locations

Influencer selfie images:

```text
<product>\_influencer_selfie_work\generated
```

A+ module images:

```text
<product>\_aplus_creative_work\generated_split
```

Injection summary:

```text
<ROOT>\_aplus_influencer_section_injection.json
```

Per-module API reference upload log:

```text
<product>\_aplus_creative_work\module_reference_upload_log.json
```

Final API-submitted prompt text, written immediately before each generation request:

```text
<product>\_aplus_creative_work\api_submitted_prompts\section-XX-*.txt
```

Per-module API submit/status/download/error log:

```text
<product>\_aplus_creative_work\module_generation_api_log.jsonl
```

AIGC/model view tags:

```text
<product>\_aplus_creative_work\aigc_model_view_tags.json
```

Root synchronous analysis/generation status:

```text
<ROOT>\_aplus_sync_run_status.json
```

Stitched long A+ image:

```text
<product>\_aplus_creative_work\<product>_Aplus_Long_<width>x<height>.png
<product>\_aplus_creative_work\generated_split\<product>_Aplus_Long_<width>x<height>.png
<ROOT>\输出结果\<product>_Aplus_Long_<width>x<height>.png
```

## Quality Gate

Before finishing, confirm:

- `_aplus_color_options_removal.json` reports zero errors, no `color_options` row remains, and every changed workbook has a backup.
- Preparation and module construction both used `scripts\excel_reader.py` in normal mode and read the complete physical worksheet rows despite stale worksheet dimension metadata.
- Every Excel Section N Headline/Copy appears only in Section N; empty Excel fields preserve Gemini-generated copy; ownership and cross-section duplicate validators passed before image generation.
- Every creative brief contains the exact five-line `Suggested Visual Baseline` block, the first four lines were written after direct visual inspection for that SKU, the fixed Style balance line is unchanged, and sibling baselines are not near-duplicates.
- No fixed text-area percentage, rigid text-safe block, or mandatory split layout was added as a workaround for missing rendered copy.
- No module prompt or API-submitted prompt contains any `Text / Callouts:` block.
- No API-submitted prompt contains `Attached Reference Image Map:` or raw reference filenames/paths; `module_reference_upload_log.json` contains the exact submitted files instead.
- Template module count and module size.
- Which sections were detected as influencer sections.
- Which sections were detected as placeholder/color-block sections, and which were detected as no-influencer replacement backgrounds.
- `target_gender`, `target_gender_source`, and whether every A+ and influencer person matches the selected model image's gender. Treat `target_customer_reference` as advisory only.
- `model_identity_reference` and whether A+ model modules resemble that reference.
- `aigc_model_view_tags.json` exactly covers all and only allowed SKU images, including `素材`, `上身`, and `上身1`, keyed by complete SKU-relative path and recording semantic person/product/detail classification, gender presentation, view, framing, and identity usability.
- Every tag was produced by the explicitly selected analysis model from one SKU contact-sheet request, every manifest ID is covered exactly once, and no tag has `source: heuristic`.
- Influencer images generated per product and occasion.
- Affected A+ module prompts have influencer instructions and `module_reference_images.json`.
- Each module's freshly rebuilt `module_reference_images.json` entry contains only role-appropriate, visually analyzed, current-SKU references; no excluded, external, stale, basename-fallback, or historical references remain.
- Each generated module prints and logs the exact reference images submitted to the API.
- The selected API supplier is recorded in `module_generation_api_log.jsonl`; GPT-RH logs include `quality`, defaulting to `medium`.
- Section 1 upload logs identify the LOGO filename and upload position when LOGO is allowed, API prompts contain no numbered filename map, and Section 1 pose directions are not exact duplicates across SPUs in the same batch.
- If the template disables LOGO exposure, Section 1 logs should show `logo_disabled_by_prompt: true`, `logo_requested_by_prompt: false`, no LOGO reference number, and no `LOGO.*` reference image.
- No module submits a back-view person without a confirmed front/three-quarter identity companion; otherwise the back-view reference is omitted.
- Section 2 contains the brief identity anchor plus a confirmed front/three-quarter AIGC companion when available.
- Every Section 2/Section 3 model-reference overlap has a validated main-agent-authored `Section 3 fashion action:` block and no legacy safe-library action block.
- When a module submits no model/person/on-body reference images, its final API prompt contains no model-reference note, no same-person/model-identity language, and no Visual Direction/Product Information cues that would cause random model generation.
- Logo modules use the Excel brand name to resolve `<ROOT>\LOGO\<brand>.*`, copy the selected file into the SPU/product folder as `LOGO.<ext>`, and upload that product-local LOGO before falling back to existing product-local LOGO images.
- `module_generation_api_log.jsonl` exists for generated products and records submit, status, completion, download, and error events.
- Each completed product has a stitched long A+ image.
- Each completed product's stitched long A+ image is also copied into `<ROOT>\输出结果` with the filename unchanged.
- Final prompts and injected instructions are English-only for visible text and explicitly forbid Chinese/CJK rendered text.
- Final influencer A+ section uses generated influencer images as reference/layout material.
- Final explicit placeholder sections contain style-matched equal-size color blocks and no influencer people, selfies, UGC screenshots, or social UI.
- Final influencer replacement background sections contain a style-matched empty background/layout, with no people, no influencer selfies, no UGC screenshots, no social UI, no color blocks unless explicitly requested, and no visible copy when the template says no copy.
- Any failed influencer or A+ modules are recorded and skipped without stopping the batch.
- Multi-SPU generation used `run_sync_product_generation.py` as one independent synchronous command per SPU, with exactly one `--product` value, an explicit timeout, and no comma-separated, whole-root, loop-hidden, detached, or background generation command.
- `_aplus_sync_run_status.json` records a terminal analysis and generation state for every attempted SKU; each command session was closed before the next began, and no wrapper, generator child process, or yielded execution cell remains after final artifact checks.
