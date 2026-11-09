<!-- translation-of: STD.md -->
# 软件测试说明 — 修仙包

简体中文 · [English](STD.md)

状态：草稿。
批次：B10
日期：2026-11-09

`STP.md` 里每个测试一节。每节说怎么准备、做什么、看到什么。命令都在仓库根目录跑；
引擎的网页版在已发布站点上，通过「所有包 → 安装插件包」装本地 `.zip`。

## TC-ID-001 — 一个目录一个 id

1. 跑 `python infra/tool/release/pack.py build packs/cultivation --out dist`，派遣包同样跑一遍。
2. 用 `python -c "import zipfile,json;print(json.loads(zipfile.ZipFile('dist/cultivation.zip').read('manifest.json'))['id'])"`
   读两个压缩包根上的 manifest。
3. 把打印出的 id 与目录名比对。

预期：两个压缩包，根的 manifest 分别写 `cultivation` 与 `cultivation-rogue`，
与目录名一致，且两个 id 不同。

## TC-ENV-001 — 压缩包不越出信封

1. 跑 `python infra/checks/check_pack.py dist/cultivation.zip`，派遣包同样。
2. 复制一份，在根上加第二个文件：
   `python -c "import zipfile,shutil;shutil.copy('dist/cultivation.zip','dist/bad.zip');z=zipfile.ZipFile('dist/bad.zip','a');z.writestr('README.md','x');z.close()"`。
3. 跑 `check_pack.py dist/bad.zip`。
4. 用符号链接条目（`ZipInfo` 的 `external_attr` 设 `0xA1FF0000`）和一个 9 MiB 条目重做第 2 步。

预期：第 1 步两次打印 `the envelope holds`；第 3、4 步失败，
并分别点出第二个根条目、符号链接与 8 MiB 上限。

## TC-IDN-001 — 玩家看到名字，不是 id

1. 开新游戏，进「所有包」。
2. 记下世界条目下的两个包。
3. 把界面语言切到英文，再进「所有包」。

预期：条目读作「修仙·派遣」与 Cultivation: Dispatch；两屏都不出现
`cultivation` 或 `cultivation-rogue`。

## TC-LOC-001 — 每个节点、每个标签都有译文

1. 对两个包做标签镜像：`nodes.json` 里每个节点 id，在 `data/i18n/en.json`
   里都要有条目，含 `text`，且 `choices` 数组长度相同。
2. 对派遣包每个状态资源、动作、位阶与失败，检查 `strings` 里有引擎会打印的键。
3. 从 `en.json` 删掉一个键，重建、安装。

预期：第 1、2 步找不到缺口；第 3 步在安装时以缺译文报错被拒，
把键补回去又能装上。

## TC-LIN-001 — 五个节点，一个结尾

1. 装 `dist/cultivation.zip`，开新游戏。
2. 五屏各选第一个选项。

预期：第五屏没有选项，出现结束屏；结束时步数读作 5/5。

## TC-PRG-001 — 读数是引擎算的

1. 开线性包，记下第一、二、三屏正文下方那行小字。
2. 打开 `packs/cultivation/data/mechanics.json`。

预期：小字依次读作「第 1/5 步」「第 2/5 步」「第 3/5 步」；文件里是
`{"rules": []}`。

## TC-BLF-001 — 两局，两个结局

1. 装 `dist/cultivation-rogue.zip`，开新游戏，剑相关的问题都按「信」回答。
2. 存到槽 1，走完第一幕，记下结局与结局点出的信念数。
3. 重开一局，每个问题都按「不信」回答，走完比对。

预期：两个结局不同；结束时的信念数不同；导航在第二、三场就分开了，
不只是最后一场。

## TC-VOI-001 — 四场只有听者能开的戏

1. 走一遍第一幕，在剑那一场选听者的那句。
2. 再走一遍，选把话留在心里的那句。
3. 比对节点图：
   `python -c "import json;n=json.load(open('packs/cultivation-rogue/data/nodes.json'));print([x['id'] for x in n['nodes'] if 'voice' in x['id']])"`。

预期：第一遍经过四场 `a1-voice-*` 之一，第二遍一场都不经过；
四场都存在，且每场只由它对应的听者选项通向。

## TC-DSP-001 — 一次派遣会写进一个弟子

1. 打开派遣包，走完序章到中枢，把阿磐派去废墟。
2. 读前后的账本：中枢显示灵石，弟子那一行显示伤、信或贪。
3. 再派阿磐去废墟一次，再试第三次。

预期：每次派遣都改 `stone`，并至少改 `injury.apan`/`trust.apan`/`greed.apan`
之一；第二次之后伤为 2，第三个按钮按不下去，理由里点出 `injury.apan`。

## TC-DSP-002 — 歇息让弟子重新可派

1. 阿磐伤为 2 时，歇息一次。
2. 再试废墟派遣。

预期：伤降到 1，按钮可用，派遣成功。

## TC-PHS-001 — 十二天，三条失败

1. 歇息十二次，数着天数。
2. 新开一局，把一名弟子往废墟派到伤为 3。

预期：第十三个动作被拒，本局报告天数用完（第 1、5、9 天各出现一个位阶名）；
伤到 3 时本局以该弟子自己的失败语结束，不是通用话术。

## TC-PHS-002 — 中枢继续活着

1. 打开派遣包，走完序章到山门。
2. 看中枢屏：它没有选项，却仍然给出动作列表。

预期：能给动作，天数读作 12，显示第一个位阶名。

## TC-SAV-001 — 存档属于它的包

1. 在派遣包的中枢存到槽 1，退回包列表。
2. 打开线性包的存档页。
3. 回派遣包，读槽 1。

预期：线性包列不出这个档；派遣包槽 1 显示中枢的文本，读回后回到中枢，
灵石与伤的数一致。

## TC-COL-001 — 一个世界，两个包

1. 两个包都装好后，打开「所有包」。
2. 复制派遣包，从 manifest 里删掉 `collection` 块，重建后换个测试名安装。

预期：第 1 步一个世界标题下有两个包；第 2 步被改过的包落在这个标题之外。

## TC-REL-001 — 描述文件与压缩包一致

1. 在 GitHub 上取最新的 `pack/cultivation-rogue/v*` 发布。
2. 下载两个资产。
3. 对下载到的压缩包跑 `python infra/tool/release/pack.py hash cultivation-rogue.zip`，
   与描述文件里的 `sha256` 比对。

预期：两个值相同，且描述文件里的版本与标签一致。

## TC-CI-001 — 坏包落不了地

1. 在临时分支上，从 `packs/cultivation/data/nodes.json` 删一个节点，不动 `en.json`。
2. 推送，打开工作流运行。

预期：`check_pack` 一步失败，运行变红并点出缺哪条译文；`main` 最新一次运行
在两个包上都是绿的。
