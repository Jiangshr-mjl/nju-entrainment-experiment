# 数据与文件对应关系

## 本地输入

逐工况子视频按项目所有者要求不上传 GitHub。处理代码需要以下八个文件位于 `--data-dir` 指定的同一目录中：

| 文件名 | 条件 | 图件中的 v 标记 |
| --- | --- | --- |
| `pure_v_1_5.mp4` | 无盐度、无浮力 | 1.5 mm/s |
| `pure_v_2_0.mp4` | 无盐度、无浮力 | 2.0 mm/s |
| `pure_v_2_5.mp4` | 无盐度、无浮力 | 2.5 mm/s |
| `pure_v_3_0.mp4` | 无盐度、无浮力 | 3.0 mm/s |
| `salt_v_1_5.mp4` | 有盐度、有浮力 | 1.5 mm/s |
| `salt_v_2_0.mp4` | 有盐度、有浮力 | 2.0 mm/s |
| `salt_v_2_5.mp4` | 有盐度、有浮力 | 2.5 mm/s |
| `salt_v_3_0.mp4` | 有盐度、有浮力 | 3.0 mm/s |

条件含义由项目所有者确认。盐度数值、密度差、`v` 对应的装置参数、重复试验编号和拍摄时间标定记录尚未提供。

原项目另有 `video/raw/`，其中包含不同命名及额外的片段。没有将其重命名或与上述输入互换，也没有推断这些片段之间的实验对应关系。

## 展示材料

| 公开候选文件 | 原始文件 | 处理 |
| --- | --- | --- |
| `docs/figures/time_height_panels.png` | `code_260712_experiment_nju/p.png` | 仅复制、重命名，图像内容不变 |
| `docs/figures/arrival_at_top.png` | `video/result/ariving_at_top.png` | 仅复制、重命名，图像内容不变 |
| `video/result/entire_process_silent.mp4` | `video/result/entire_process.mp4` | 保留视频流，移除全部音轨、原容器元数据及章节 |

单工况视频、PPT、IDE 配置、Python 缓存及探索性的归一化练习脚本 `test.py` 均不在发布候选中。
