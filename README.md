# 李宏毅《机器学习》2022 Spring 课程资料

本仓库按照课程 Lecture 顺序，整理李宏毅老师 **Machine Learning 2022 Spring** 课程页面公开提供的 PDF / PPTX 讲义，方便个人学习与查阅。

- [课程主页](https://speech.ee.ntu.edu.tw/~hylee/ml/2022-spring.php)
- [课程官方 GitHub（作业与代码）](https://github.com/virginiakm1988/ML2022-Spring)

> 本仓库是个人学习归档，并非课程官方仓库。课程安排与资料版本请以课程主页为准。

## 快速跳转

**页面导航：** [课程资料](#课程资料) · [资料说明](#资料说明) · [Git LFS](#git-lfs) · [版权说明](#版权说明) · [致谢](#致谢)

**讲义目录：**
[Lecture 01](./lectures/Lecture%2001/) ·
[Lecture 02](./lectures/Lecture%2002/) ·
[Lecture 03](./lectures/Lecture%2003/) ·
Lecture 04（无课件） ·
[Lecture 05](./lectures/Lecture%2005/) ·
[Lecture 06](./lectures/Lecture%2006/) ·
[Special: SSL for NLP](./lectures/Lecture%2006.5%20-%20Special%20SSL%20for%20NLP/) ·
[Lecture 07](./lectures/Lecture%2007/) ·
[Lecture 08](./lectures/Lecture%2008/) ·
[Lecture 09](./lectures/Lecture%2009/) ·
[Lecture 10](./lectures/Lecture%2010/) ·
[Lecture 11](./lectures/Lecture%2011/) ·
[Lecture 12](./lectures/Lecture%2012/) ·
[Lecture 13](./lectures/Lecture%2013/) ·
[Lecture 14](./lectures/Lecture%2014/) ·
[Lecture 15](./lectures/Lecture%2015/)

## 课程资料

| Lecture | 日期 | 课程主题 | 本仓库讲义 |
|---|---:|---|---|
| [Lecture 01](./lectures/Lecture%2001/) | 02/18 | Introduction of Deep Learning | 2022：课程介绍、规则、PyTorch、Colab、环境设置；另含原目录已有的 Regression 补充讲义 |
| [Lecture 02](./lectures/Lecture%2002/) | 02/25 | What to do if my network fails to train | 2022：Basic Theory |
| [Lecture 03](./lectures/Lecture%2003/) | 03/04 | Image as Input | 2022：Validation、Why Deep |
| Lecture 04 | 03/11 | Sequence as Input | 课程页未提供 PDF / PPTX |
| [Lecture 05](./lectures/Lecture%2005/) | 03/18 | Sequence to Sequence | 2022：Self-attention / Transformer (`xformer`) |
| [Lecture 06](./lectures/Lecture%2006/) | 03/25 | Generation | 2021 GAN 补充材料；2022 当周课程为 Privacy for ML |
| [Special: SSL for NLP](./lectures/Lecture%2006.5%20-%20Special%20SSL%20for%20NLP/) | 04/01 | Recent Advance of Self-supervised Learning for NLP | 2022：PLM；2021 补充：BERT |
| [Lecture 07](./lectures/Lecture%2007/) | 04/15 | Self-supervised Learning for Speech and Image | 2022：SSL for Speech and Image |
| [Lecture 08](./lectures/Lecture%2008/) | 04/22 | Auto-encoder / Anomaly Detection | 2021 Auto-Encoder 补充材料；2022 当周为客座演讲 |
| [Lecture 09](./lectures/Lecture%2009/) | 04/29 | Explainable AI | 2022：Adversarial Attack for NLP Part 1；2021 补充：Explainable AI |
| [Lecture 10](./lectures/Lecture%2010/) | 05/06 | Attack | 2022：Adversarial Attack for NLP Part 2；2021 补充：Adversarial Attack |
| [Lecture 11](./lectures/Lecture%2011/) | 05/13 | Adaptation | 2022：More about Self-supervised Learning；2021 补充：Adaptation |
| [Lecture 12](./lectures/Lecture%2012/) | 05/20 | Reinforcement Learning | 2021 DRL 补充材料；2022 当周课程为 Quantum Machine Learning |
| [Lecture 13](./lectures/Lecture%2013/) | 05/27 | Network Compression | 2021：Network Compression |
| [Lecture 14](./lectures/Lecture%2014/) | 06/03 | Life-long Learning | 2021：Life-long Learning；2022 当周为期末考周、不上课 |
| [Lecture 15](./lectures/Lecture%2015/) | 06/10 | Meta Learning | 2022：More about Meta Learning |

## 资料说明

- `lectures/` 目前包含 43 个 PDF / PPTX 文件，总计约 322 MiB。
- 课程主页同时列有 **2022 当期材料**和部分 **2021 补充材料**，上表已注明来源年份。
- Lecture 09 与 Lecture 10 的 2022 NLP 对抗攻击课程共用同一份 `Attacks-in-NLP-Draft.pdf`。为避免重复，本仓库只在 `Lecture 09` 中保留一份。
- Lecture 04 的课程页没有提供 PDF / PPTX，因此没有对应课件目录。
- 文件保留课程页上的原始名称与格式；目录编号补零，以便在 GitHub 中按照 Lecture 顺序显示。

## Git LFS

所有 PPTX 文件均由 [Git LFS](https://git-lfs.com/) 管理，其中 `Lecture 12/drl_v5.pptx` 超过普通 GitHub 文件的单文件大小限制。

克隆仓库前请先安装 Git LFS：

```bash
git lfs install
git clone https://github.com/lizhuofan-curry/2022SpringLiHongYiML.git
```

如果仓库已经克隆，但大文件尚未下载，可在仓库目录执行：

```bash
git lfs pull
```

## 版权说明

课程讲义、投影片及其中的内容版权归李宏毅老师、授课讲者与课程团队等原权利人所有，仅供学习与研究参考。仓库中的 MIT License 仅适用于仓库作者自行创作且有权授权的内容，不自动适用于这些第三方课程资料。

## 致谢

感谢李宏毅老师、课程助教与客座讲者公开课程与学习资料。
