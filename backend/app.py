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
        Annotate this article line by line and show us if it's right or left oriented.
        provide the orientation, from 0% to 100% (0% being the most left-leaning and 100% being the most right-leaning)
        At the end, provide the global orientation, from 0% to 100% (0% being the most left-leaning and 100% being the most right-leaning)
        Please pick the two polarzied sided this next text information and review the content directly.  List them in a table.  Then pick the top three adjectives describing the each of the two sides.  Then based on what you absorbed, explain whether this article is baised against any of the sides.;
        response_template:
        "line"
        - analysis, orientation percentage
        "line"
        - analysis, orientation percentage
        ......
        "line"
        - analysis, orientation percentage

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
    output = chain.run({"preprompt": prompt, "article": article})
    return jsonify({'message': output})

if __name__ == '__main__':
    app.run(debug=True)
