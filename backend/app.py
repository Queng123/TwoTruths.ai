from dotenv import load_dotenv

from flask import Flask, jsonify, request
from flask_cors import CORS

from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from goose3 import Goose

import openai
import logging
import os


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

@app.route('/rewrite', methods=['POST'])
def rewrite():
    url = request.json['url']
    g = Goose()

    article = g.extract(url=url).cleaned_text

    preprompt = """
    rewrite this article without any bias:
    * DO NOT ADD ANY OTHER DATA
    * THE NEW ARTICLE SHOULD BE NONE ORIENTED
    * Ensure neutrality in tone by removing any language that implies judgment, preference, or criticism.
    *Maintain factual accuracy, keeping all original details and figures without interpretation or exaggeration.
    *Exclude language or phrasing that could indicate support, opposition, or affiliation with any viewpoint.
    *Remove adjectives or adverbs that add emotional or persuasive weight to the content.
    * Do not change the quotes or any citations
    """

    template = """
    {preprompt}

    Article:
    {article}
    """

    prompt_template = PromptTemplate(input_variables=["preprompt", "article"], template=template)




    prompt = prompt_template.format(preprompt=preprompt, article=article)
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = LLMChain(llm=llm, prompt=prompt_template)
    output = chain.run({"preprompt": prompt, "article": article})


    return jsonify({'message': output})

@app.route('/info', methods=['POST'])
def infos():
    url = request.json['url']
    g = Goose()

    article = g.extract(url=url).cleaned_text

    preprompt = """
        instructions:
        Analyse the provided article and show us if it's right or left oriented.
        At the end, provide the global orientation, from 0% to 100% (0% being the most left-leaning and 100% being the most right-leaning)


        response_template:
        text

        global orientation
    """

    template = """
    {preprompt}

    article:
    {article}
    """

    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt_template = PromptTemplate(input_variables=["preprompt", "article"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    prompt = prompt_template.format(preprompt=preprompt, article=article)
    all_text = chain.run({"preprompt": prompt, "article": article})

    template = """
    {preprompt}

    previous analysis:
    {previous_analysis}

    article:
    {article}
    """

    preprompt = """
    Based on the provided analysis,
    Please pick the two polarzied sided.
    Then clearly label the first side as "side 1" and the second side as "side 2."
    Just clearly name the sides with one clear word, related to the topic.
    Then List them without formatting or any additional information.
    example:
    side 1: "side 1"
    side 2: "side 2"
    """

    prompt_template = PromptTemplate(input_variables=["preprompt", "previous_analysis", "article"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    prompt = prompt_template.format(preprompt=preprompt, previous_analysis=all_text, article=article)
    two_sides = chain.run({"preprompt": prompt, "previous_analysis": all_text, "article": article})

    template = """
    {preprompt}

    previous analysis:
    {previous_analysis}

    sides:
    {two_sides}

    original article:
    {article}
    """


    preprompt = """
    based on the previous analysis
    Pick the top three adjectives describing the each of the two sides and also list them in a table.
    Use the adjective from the original article.
    Then clearly label the first side as "side 1" and the second side as "side 2."
    Then provide the adjectives without any additional information or formatting (no table or bullet points).
    example:
    side 1: "adjective 1", "adjective 2", "adjective 3"
    side 2: "adjective 1", "adjective 2", "adjective 3"
    """

    prompt_template = PromptTemplate(input_variables=["preprompt", "two_sides", "previous_analysis", "article"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    prompt = prompt_template.format(preprompt=preprompt, two_sides=two_sides, previous_analysis=all_text, article=article)
    adjectives = chain.run({"preprompt": prompt, "two_sides": two_sides, "previous_analysis": all_text, "article": article})

    template = """
    {preprompt}

    previous analysis:
    {previous_analysis}

    article:
    {article}
    """

    preprompt = """
    based on the previous analysis
    explain whether this article is baised against any of the sides in a summary fashion.
    do not add any formatting to your response.
    """

    prompt_template = PromptTemplate(input_variables=["preprompt", "previous_analysis", "article"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    prompt = prompt_template.format(preprompt=preprompt, previous_analysis=all_text, article=article)
    bias = chain.run({"preprompt": prompt, "previous_analysis": all_text, "article": article})

    return jsonify({'two_sides': two_sides, 'adjectives': adjectives, 'bias': bias})

if __name__ == '__main__':
    app.run(debug=True)
