# CharacterGLM-6B

<div align="center">
<img src=resources/CharacterGLM-logo.png width="40%"/>
</div>

<br>

<p align="center">
🤗 <a href="https://huggingface.co/thu-coai/CharacterGLM-6B" target="_blank">HF Repo</a> • 📃 <a href="https://arxiv.org/abs/2311.16832 " target="_blank">CharacterGLM Paper</a><br>
</p>
<p align="center">
     👋 Join our <a href="resources/wechat.md" target="_blank">WeChat</a>
</p>
<p align="center">
📍Experience the larger-scale CharacterGLM model on the <a href="https://open.bigmodel.cn/dev/api#super-humanoid">Open Platform</a>.
</p>

[Read this in Chinese.](./README.md)

### Experience stronger abilities

If you want to use the CharacterGLM model with a larger number of parameters, you can experience the larger-scale
CharacterGLM model on [Open Platform](https://open.bigmodel.cn/dev/api#super-humanoid).
The API version has more roles, stronger scene introduction capabilities, more complete laws and ethics, and product
capabilities, making it easier for developers to conduct more in-depth scene simulations and product development.

**The open source model does not have development capabilities and is for academic research only and cannot be used for
any commercial and communication purposes**

📔
For more detailed usage information, please refer
to: [CharacterGLM-6B Technical Documentation](https://huggingface.co/thu-coai/CharacterGLM-6B)

## introduce

CharacterGLM-6B is a new generation dialogue pre-training model jointly released by Lingxin Intelligence and Tsinghua
University CoAI Laboratory. CharacterGLM-6B is based on ChatGLM2
The open source models in the series retain many excellent features of the previous two generations of models, such as
smooth dialogue and low deployment threshold. The design of CharacterGLM-6B follows the following principles:

#### A shot in the arm to make AI characters “alive”

If a conversational AI character wants to behave like a lifelike person, it must have "human characteristics",
especially the characteristics of human text form in language expression. We focus on the characteristics of human
language expression in attributes and behaviors: attributes mainly affect the content of language expression, while
behaviors affect the style and tone of language expression.

**Attributes:** The design of CharacterGLM mainly considers seven attributes, including identity, interests, opinions,
experiences, achievements, social relationships and others.

**Behavior:** Behavior is mainly composed of some dynamic elements: language characteristics, emotional expressions and
interaction patterns. For example, older people tend to use more formal language, while teenagers prefer Internet
buzzwords. CharacterGLM mainly considers linguistic features and personality as behavioral aspects of design.

#### Whether the AI character is "alive" in the demon mirror

For a conversational AI character to prove itself as a lifelike character, it needs to possess the expressive qualities
of a real person. We focused on three aspects of expressive qualities: consistency, personification, and attractiveness.

**Consistency:** Character consistency is the ability of a character to exhibit stable attributes and behaviors across
interactions. Maintaining consistency in a conversational AI character's attributes and behaviors across conversations
is critical to earning user satisfaction and trust.

**Anthropomorphism:** Character anthropomorphism requires the character to behave naturally in its interaction with the
user, similar to the natural interaction between people. Human-like conversational AI characters are integral to
increasing user acceptance and promoting more natural and engaging conversations.

**Engagement:** Engagement is a measure of how conversational AI characters generate user interest and drive engagement.
During the chat process, making the conversation interesting and making people want to continue chatting will directly
affect the user experience. This is also a reflection of the overall performance of the dialogue model.

## Dialogue example

<div align="center">
<img src=resources/intro-case.png width="80%"/>
</div>

## method

Based on the above design principles, we collected role descriptions containing attributes and behaviors, crowdsourced
to build a large-scale high-quality dialogue data set, and converted the role descriptions into natural language
prompts, and then used parameters from 6B to 66B The ChatGLM model is fine-tuned to create CharacterGLM. In addition, a
portion of online interaction data was also collected to enhance the training of CharacterGLM to achieve
self-improvement iteration of CharacterGLM.

<div align="center">
<img src=resources/framework.png width="80%"/>
</div>

-----

The CharacterGLM-6B open source model aims to promote the development of large model technology together with the open
source community. Developers and everyone are kindly requested to abide by the [Open Source Agreement] (MODEL_LICENSE).
Do not use open source models and codes and derivatives based on open source projects for any purpose that may cause
harm to the country and society or for any services that have not undergone security assessment and filing.
Currently, we have not developed any applications based on the **CharacterGLM-6B open source model** in this project,
including web, Android, Apple iOS and Windows App applications.
Due to the small scale of the CharacterGLM-6B model and the fact that the model is affected by probabilistic and random
factors, the accuracy of the output content cannot be guaranteed. At the same time, the output of the model is easily
misled by the user's input.
**This project does not assume any risks and responsibilities arising from data security and public opinion risks caused
by open source models and codes, or any model being misled, abused, disseminated, or improperly exploited. **

## Experiment

### Evaluation Criteria

In addition to Consistency, Human-likeness, and Engagement, we use: (1) Quality to evaluate the fluency and contextual
coherence of responses, (2) Safety Measure whether the reply complies with ethical standards, and (3) Correctness
determines whether the reply contains hallucinations. Additionally, use the Overall metric to measure the overall
quality of model responses.

### Assessment settings

We compared CharacterGLM with 10 Chinese-friendly mainstream LLMs and hired 10 annotators. Each annotator created two
characters on 11 models and conducted no less than 20 rounds of dialogue interaction. After the interaction is
completed, the annotator will give a score of 1-5 based on the above six sub-dimensions and the overall dimension. The
higher the score, the better the model performance. Finally, the average score of each model in each dimension is
calculated.

<div align="center">
<img src=resources/characterglm-baseline.png width="80%"/>
</div>

### evaluation result

<div align="center">
<img src=resources/characterglm-experiments-1.png width="80%"/>
</div>

### Error analysis

We further marked six aspects of the responses to each round of the 11 models: role inconsistency (OOC), contradiction (
Contradiction), repetition (Repetition), low quality (Less-quality), and low information content (Less-information) and
Proactivity (the ability to actively guide topics and promote the development of conversations). Additionally, the
“Overall” score is calculated as the sum of the first five dimensions minus the sixth dimension, with lower “Overall”
scores indicating better performance.

<div align="center">
<img src=resources/characterglm-experiments-2.png width="80%"/>
</div>

The results are shown in the table above. The overall answer quality of CharacterGLM is significantly better than the
baseline model. Although CharacterGLM-66B does not achieve the best performance in most dimensions, it scores best
overall. In addition, although CharacterGLM does not perform well in terms of initiative, as you can see from the
example in the table below, the model has the ability to advance the plot, which plays a key role in attracting users
and keeping their interest in the conversation.

<div align="center">
<img src=resources/case.png width="80%"/>
</div>

### Comparative evaluation

We evaluated CharacterGLM against the MiniMax model specifically designed for role-playing, as well as GPT-3.5 and
GPT-4. The evaluation still uses interactive manual evaluation, involving a total of 24 characters, covering
celebrities, daily life, game audio and video, and virtual love characters. The conversation topics are limited to three
scenarios: chatting, interviews, and love. Similarly, 10 annotators are hired here to interact with the model and label
the two outputs of the two models in the same context as win/tie/lose, and finally calculate the value of each model in
Win/draw/loss ratios for different character classes and dialogue topics.

The results evaluated by character category are shown in the table below, CharacterGLM-66B consistently outperforms
GPT-3.5 and MiniMax in most character categories.

<div align="center">
<img src=resources/characterglm-experiments-3.png width="80%"/>
</div>

The results of the evaluation by conversation topic are shown in the table below. CharacterGLM-66B performs equally well
with MiniMax in casual chat and love scenes, but in interview scenes CharacterGLM-66B outperforms MiniMax by a
significant 7% advantage. CharacterGLM-66B is slightly inferior to GPT-4, but compared to GPT-3.5, CharacterGLM-66B has
advantages in all conversation topics.

<div align="center">
<img src=resources/characterglm-experiments-4.png width="80%"/>
</div>

## Usage

### Environment installation

First you need to download this repository:

```shell
git clone https://github.com/thu-coai/CharacterGLM-6B
cd CharacterGLM-6b
```

Then use pip to install dependencies:

```
pip install -r requirements.txt
```

+ The `transformers` library version should be `4.36.2` and above, and the `torch` library version should be `2.1.0` and
  above to obtain the best inference performance.
+ In order to ensure that the version of `torch` is correct, please strictly follow the instructions
  of [official documentation](https://pytorch.org/get-started/locally/) for installation.
+ The `streamlit` library version should be the `1.30.0` version and above.

#### Load model from local

Automatically download model implementation and parameters. The complete model is implemented
in [Hugging Face](https://huggingface.co/thu-coai/CharacterGLM-6B)
. If your network environment is poor, downloading model parameters may take a long time or even fail. At this time, you
can first download the model to the local and then load it from the local.

From Hugging Face Hub
To download the model, you need
to [install Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)
, then run

```Shell
git clone https://huggingface.co/thu-coai/CharacterGLM-6B
```

### Web version dialogue Demo

You can start the web version demo based on Streamlit with the following command [web_demo_streamlit.py](basic_demo/web_demo_streamlit.py):

```shell
cd basic_demo
streamlit run web_demo_streamlit.py
```

The web version demo will run a Web Server and output the address. Open the output address in a browser to use it. After
testing, the web version Demo based on Streamlit will be smoother.

### Command line dialogue Demo

Run [cli_demo.py](basic_demo/cli_demo.py) in the warehouse:

```shell
cd basic_demo
python cli_demo.py
```

The program will conduct an interactive conversation in the command line. Enter instructions in the command line and
press Enter to generate a reply. Enter `clear` to clear the conversation history, and enter `stop` to terminate the
program.

### Model fine-tuning

We do not yet provide model fine-tuning scripts, we will launch them as soon as possible, so stay tuned.

## Quote

If you find our work helpful, please consider citing the following papers.

```
@article{zhou2023characterglm,
  title={CharacterGLM: Customizing Chinese Conversational AI Characters with Large Language Models},
  author={Zhou, Jinfeng and Chen, Zhuang and Wan, Dazhen and Wen, Bosi and Song, Yi and Yu, Jifan and Huang, Yongkang and Peng, Libiao and Yang, Jiaming and Xiao, Xiyao and others},
  journal={arXiv preprint arXiv:2311.16832},
  year={2023}
}
```
