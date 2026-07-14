# 李宏毅《机器学习》2021 / 2022 Spring 课程资料

本仓库按课程年份和 Lecture 顺序整理李宏毅老师 **Machine Learning 2021 Spring** 与 **Machine Learning 2022 Spring** 课程页面公开提供的 PDF / PPTX 讲义，方便个人学习与查阅。

- [2021 Spring 课程主页](https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php)
- [2022 Spring 课程主页](https://speech.ee.ntu.edu.tw/~hylee/ml/2022-spring.php)
- [2022 课程官方 GitHub（作业与代码）](https://github.com/virginiakm1988/ML2022-Spring)

> 本仓库是个人学习归档，并非课程官方仓库。课程安排与资料版本请以课程主页为准。

## 目录结构

```text
.
├── 2021/
│   ├── lectures/          # 13 个 Lecture 分类，45 份 PDF / PPTX
│   └── lecture-files.csv  # 文件名、Lecture 与原始下载地址
└── 2022/
    ├── lectures/          # 原仓库的 2022 课程讲义
    └── homeworks/         # 原仓库已有作业，当前包含 HW01
```

## 2021 Spring

| Lecture | 课程主题 | 主要讲义 |
|---|---|---|
| [Lecture 01](./2021/lectures/Lecture%2001%20-%20Introduction/) | Introduction | 课程介绍（中/英文）、Regression |
| [Lecture 02](./2021/lectures/Lecture%2002%20-%20Deep%20Learning/) | Deep Learning | Overfit、Critical Point、Optimizer、Classification |
| [Lecture 03](./2021/lectures/Lecture%2003%20-%20CNN%20and%20Self-Attention/) | CNN & Self-Attention | ML Pretest、CNN、Self-Attention |
| [Lecture 04](./2021/lectures/Lecture%2004%20-%20Theory%20of%20ML/) | Theory of ML | PAC Learning |
| [Lecture 05](./2021/lectures/Lecture%2005%20-%20Transformer/) | Transformer | Normalization、Seq2Seq |
| [Lecture 06](./2021/lectures/Lecture%2006%20-%20Generative%20Model/) | Generative Model | GAN |
| [Lecture 07](./2021/lectures/Lecture%2007%20-%20Self-Supervised%20Learning/) | Self-Supervised Learning | BERT、Auto-Encoder |
| [Lecture 08](./2021/lectures/Lecture%2008%20-%20Explainable%20AI%20and%20Adversarial%20Attack/) | Explainable AI / Adversarial Attack | XAI、Adversarial Attack |
| [Lecture 09](./2021/lectures/Lecture%2009%20-%20Domain%20Adaptation/) | Domain Adaptation | Domain Adaptation |
| [Lecture 10](./2021/lectures/Lecture%2010%20-%20Reinforcement%20Learning/) | Reinforcement Learning | DRL |
| [Lecture 11](./2021/lectures/Lecture%2011%20-%20Quantum%20ML/) | Quantum ML | 客座讲义 |
| [Lecture 12](./2021/lectures/Lecture%2012%20-%20Life-Long%20Learning%20and%20Compression/) | Life-Long Learning / Compression | Life-long Learning、Network Compression |
| [Lecture 13](./2021/lectures/Lecture%2013%20-%20Meta%20Learning/) | Meta Learning | Meta Learning |

完整文件与来源地址见 [`2021/lecture-files.csv`](./2021/lecture-files.csv)。2021 作业未批量收录；课程页中的公开讲义已完整归档。

## 2022 Spring

**讲义目录：**
[Lecture 01](./2022/lectures/Lecture%2001/) ·
[Lecture 02](./2022/lectures/Lecture%2002/) ·
[Lecture 03](./2022/lectures/Lecture%2003/) ·
Lecture 04（课程页无课件） ·
[Lecture 05](./2022/lectures/Lecture%2005/) ·
[Lecture 06](./2022/lectures/Lecture%2006/) ·
[Special: SSL for NLP](./2022/lectures/Lecture%2006.5%20-%20Special%20SSL%20for%20NLP/) ·
[Lecture 07](./2022/lectures/Lecture%2007/) ·
[Lecture 08](./2022/lectures/Lecture%2008/) ·
[Lecture 09](./2022/lectures/Lecture%2009/) ·
[Lecture 10](./2022/lectures/Lecture%2010/) ·
[Lecture 11](./2022/lectures/Lecture%2011/) ·
[Lecture 12](./2022/lectures/Lecture%2012/) ·
[Lecture 13](./2022/lectures/Lecture%2013/) ·
[Lecture 14](./2022/lectures/Lecture%2014/) ·
[Lecture 15](./2022/lectures/Lecture%2015/)

**作业入口：** [2022 作业目录](./2022/homeworks/) · [HW01：COVID-19 Regression](./2022/homeworks/HW01%20-%20COVID-19%20Regression/)

## Git LFS

仓库中的 PPTX 大文件使用 Git LFS 管理。克隆前请安装 Git LFS：

```bash
git lfs install
git clone https://github.com/lizhuofan-curry/2022SpringLiHongYiML.git
```

如果仓库已经克隆但大文件尚未下载，可在仓库目录执行 `git lfs pull`。

## 版权说明

课程讲义、投影片及其中的内容版权归李宏毅老师、授课讲者与课程团队等原权利人所有，仅供学习与研究参考。仓库中的 MIT License 仅适用于仓库作者自行创作且有权授权的内容，不自动适用于这些第三方课程资料。

## 致谢

感谢李宏毅老师、课程助教与客座讲者公开课程与学习资料。
