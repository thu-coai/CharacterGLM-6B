# CharacterGLM-6B

<div align="center">
<img src=resources/CharacterGLM-logo.png width="40%"/>
</div>

<br>

<p align="center">
🤗 <a href="https://huggingface.co/thu-coai/CharacterGLM-6B" target="_blank">HF Repo</a> • 📃 <a href="https://arxiv.org/abs/2311.16832" target="_blank">CharacterGLM Paper</a><br>
</p>
<p align="center">
    👋 加入我们的 <a href="resources/wechat.md" target="_blank">微信</a>
</p>
<p align="center">
📍在 <a href="https://open.bigmodel.cn/dev/api#super-humanoid">开放平台</a> 体验更大规模的 CharacterGLM 模型。
</p>

[Read this in English.](./README_en.md)

### 体验更强的能力

如果你想使用更大参数量的 CharacterGLM 模型，可以在 [开放平台](https://open.bigmodel.cn/dev/api#super-humanoid) 体验更大规模的 CharacterGLM 模型。
API版本 具有更多角色，更强的情景带入能力，更加完善的法律，道德规范，具备产品能力，方便开发者进行更深度的情景模拟和产品开发。

**开源模型不具备商用能力，仅供学术研究使用，不可用于任何商业和传播用途**

📔
更为详细的使用信息，可以参考：[CharacterGLM-6B 技术文档](https://zhipu-ai.feishu.cn/wiki/MlRiwU8NXi3A3zkpHNdcvcUmnCg)

## 介绍

CharacterGLM-6B 是 聆心智能和清华大学 CoAI 实验室联合发布的新一代对话预训练模型。CharacterGLM-6B 是 基于 ChatGLM2
系列中的开源模型，在保留了前两代模型对话流畅、部署门槛低等众多优秀特性的基础上，CharacterGLM-6B 的设计遵循以下原则：

#### AI角色变“活”的强心针

一个对话式的AI角色要想表现的像一个栩栩如生的人，必定需要具备“人的特质”，特别是人在语言表达中的文本形式的特征。我们将人的语言表达特征的重点落实在属性和行为上：属性主要影响语言表达的内容，行为则影响语言表达的风格和口吻。

**属性：** CharacterGLM的设计主要考虑了七种属性，包括身份、兴趣、观点、经历、成就、社交关系和其他。

**行为：** 行为主要由一些动态的元素组成：语言特征、情感表达和互动模式。例如，老年人更倾向于使用一些更正式的语言，而青少年则更喜欢用网络流行语。CharacterGLM则主要考虑了语言学特征和性格作为行为方面的设计。

#### AI角色是否“活”的照妖镜

一个对话式的AI角色要想证明自己是一个栩栩如生的角色，需要具备真实的人所具备的表达特质。我们主要关注三个方面的表达特质：一致性、拟人化和吸引力。

**一致性：** 角色一致性是角色在交互期间展现稳定的属性和行为的能力。维持一个会话式AI角色在对话中属性和行为的一致对于赢得用户的满足和信任是至关重要的。

**拟人化：** 角色拟人化要求角色在与用户的交互中表现自然，类似人与人之间的自然交互。类人的会话式AI角色对于提高用户的接受度以及促进更自然和有吸引力的对话是不可或缺的。

**吸引力：** 吸引力是会话式AI角色引起用户兴趣以及促进用户参与的衡量依据。聊天过程中，让对话有趣，让人想聊下去会直接影响用户的体验，这也是对话模型整体性能的一个体现。

## 对话示例

<div align="center">
<img src=resources/intro-case.png width="80%"/>
</div>

## 方法

依据上面的设计原则，我们收集了包含属性和行为的角色描述，并众包构建了一个大规模高质量的对话数据集，并将角色描述转化为了自然语言提示，进而使用从6B到66B参数的ChatGLM模型进行微调来打造CharacterGLM。此外，还收集了一部分线上交互数据来增强
CharacterGLM 的训练，以实现CharacterGLM的自我完善式迭代。

<div align="center">
<img src=resources/framework.png width="80%"/>
</div>

-----

CharacterGLM-6B 开源模型旨在与开源社区一起推动大模型技术发展，恳请开发者和大家遵守 [开源协议](MODEL_LICENSE)，
勿将开源模型和代码及基于开源项目产生的衍生物用于任何可能给国家和社会带来危害的用途以及用于任何未经过安全评估和备案的服务。
目前，本项目我们未基于 **CharacterGLM-6B 开源模型** 开发任何应用，包括网页端、安卓、苹果 iOS 及 Windows App 等应用。
由于 CharacterGLM-6B 模型规模较小，且模型受概率随机性因素影响，无法保证输出内容的准确。同时模型的输出容易被用户的输入误导。
**本项目不承担开源模型和代码导致的数据安全、舆情风险或发生任何模型被误导、滥用、传播、不当利用而产生的风险和责任。**

## 实验

### 评估标准

除了一致性（Consistency）、拟人化（Human-likeness）和吸引力（Engagement），我们使用：（1）质量（Quality）来评估回复的流畅度和上下文连贯性，（2）安全性（Safety）衡量回复是否符合道德标准，（3）正确性（Correctness）确定回复是否存在幻觉。此外，使用“整体（Overall）”指标来衡量模型回复的整体质量。

### 评估设置

我们将 CharacterGLM 与10个中文友好的主流 LLM
进行对比，雇佣了10个标注人员，每个标注人员在11个模型上各创建两个角色，并进行不少于20轮的对话交互。交互完成后，标注人员依据上述6个子维度和整体维度进行1-5分的打分，分值越高表示模型性能越好，最后计算每个模型在各个维度上的平均分。

<div align="center">
<img src=resources/characterglm-baseline.png width="80%"/>
</div>

### 评估结果

<div align="center">
<img src=resources/characterglm-experiments-1.png width="80%"/>
</div>

### 错误分析

我们对11个模型每个轮次的回复进一步标注了六个方面：角色不一致（OOC）、矛盾（Contradiction）、重复（Repetition）、低质量（Less-quality）、低信息量（Less-information）和主动性（Proactivity，主动引导话题并推动对话发展的能力）。此外，“整体（Overall）”分数的计算方式为前五个维度的总和减去第六个维度，“整体”得分越低表示性能越好。

<div align="center">
<img src=resources/characterglm-experiments-2.png width="80%"/>
</div>

结果如上表所示，CharacterGLM的整体回答质量明显优于基准模型。虽然 CharacterGLM-66B
在大多数维度上并未达到最佳性能，但整体得分最佳。此外，尽管CharacterGLM在主动性方面的表现不够出色，但从下表示例中可以看到模型具备推动情节发展的能力，这在吸引用户并保持他们对话的兴趣中发挥了关键作用。

<div align="center">
<img src=resources/case.png width="80%"/>
</div>

### 对比式评估

我们将 CharacterGLM 与专门用于角色扮演的 MiniMax 模型以及 GPT-3.5 和
GPT-4进行了对比式的评估。该评估仍采用交互式人工评估，共涉及24个角色，涵盖名人类、日常生活类、游戏影音类以及虚拟恋爱类角色，对话主题限制在闲聊、访谈和恋爱三种场景。同样地，这里雇佣了10个标注人员与模型进行交互，并标记两个模型在相同上下文下的两个输出为胜（win）/平（tie）/负（lose），最终计算每个模型在不同角色类别和对话主题下的胜/平/负比率。

按角色类别评估的结果如下表所示，CharacterGLM-66B 在大多数角色类别中始终优于 GPT-3.5 和 MiniMax。

<div align="center">
<img src=resources/characterglm-experiments-3.png width="80%"/>
</div>

按对话主题评估的结果如下表所示，CharacterGLM-66B 在闲聊和恋爱场景中与 MiniMax 表现相当，但在访谈场景中 CharacterGLM-66B
以显著的7%优势胜过 MiniMax。CharacterGLM-66B 稍逊 GPT-4，但与 GPT-3.5 相比，CharacterGLM-66B 在所有对话主题中都具有优势。

<div align="center">
<img src=resources/characterglm-experiments-4.png width="80%"/>
</div>

## 使用方式

### 环境安装

首先需要下载本仓库：

```shell
git clone https://github.com/thu-coai/CharacterGLM-6B
cd CharacterGLM-6b
```

然后使用 pip 安装依赖：

```
pip install -r requirements.txt
```

+ `transformers` 库版本应该 `4.36.2` 以及以上的版本 ，`torch` 库版本应为 2.1.0 及以上的版本，以获得最佳的推理性能。
+ 为了保证 `torch` 的版本正确，请严格按照 [官方文档](https://pytorch.org/get-started/locally/) 的说明安装。

#### 从本地加载模型

自动下载模型实现和参数。完整的模型实现在 [Hugging Face Hub](https://huggingface.co/thu-coai/CharacterGLM-6B)
。如果你的网络环境较差，下载模型参数可能会花费较长时间甚至失败。此时可以先将模型下载到本地，然后从本地加载。

从 Hugging Face Hub
下载模型需要先[安装Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)
，然后运行

```Shell
git clone https://huggingface.co/thu-coai/CharacterGLM-6B
```

### 网页版对话 Demo

可以通过以下命令启动基于 Streamlit 的[网页版 demo](basic_demo/web_demo_streamlit.py)：

```shell

streamlit run basic_demo/web_demo_streamlit.py
```

网页版 demo 会运行一个 Web Server，并输出地址。在浏览器中打开输出的地址即可使用。 经测试，基于 Streamlit 的网页版 Demo 会更流畅。

### 命令行对话 Demo

运行仓库中 [cli_demo.py](basic_demo/cli_demo.py)：

```shell
python basic_demo/cli_demo.py
```

程序会在命令行中进行交互式的对话，在命令行中输入指示并回车即可生成回复，输入 `clear` 可以清空对话历史，输入 `stop` 终止程序。

### 模型微调

我们暂时还没有提供模型微调的脚本，我们将尽快推出，敬请期待。

## 引用

如果你觉得我们的工作有帮助的话，请考虑引用下列论文。

```
@article{zhou2023characterglm,
  title={CharacterGLM: Customizing Chinese Conversational AI Characters with Large Language Models},
  author={Zhou, Jinfeng and Chen, Zhuang and Wan, Dazhen and Wen, Bosi and Song, Yi and Yu, Jifan and Huang, Yongkang and Peng, Libiao and Yang, Jiaming and Xiao, Xiyao and others},
  journal={arXiv preprint arXiv:2311.16832},
  year={2023}
}
```
