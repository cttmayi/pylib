


def test_prompts_classifier():
    # from langchain.llms import OpenAI
    from langchain_community.llms import OpenAI
    # from langchain.chat_models import ChatOpenAI
    # from langchain_community.chat_models import ChatOpenAI    
    from langchain_openai import ChatOpenAI

    from prompts.classifier import Classifier
    # from langchain.vectorstores import Chroma
    from langchain_community.vectorstores import Chroma

    #from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain_openai import OpenAIEmbeddings

    # llm = OpenAI(model_name='text-davinci-003', temperature=0.0)
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.0)
    

    embeddings = OpenAIEmbeddings()
    db = Chroma('test', embeddings, persist_directory='default.db')

    classifier = Classifier(llm, db)

    classifier.init_for_test()

    question = 'Create a presentation about climate change.'
    ret = classifier(question)
    print(ret)
    assert(ret.content.find('RequiresContext: true') >= 0)
    assert(ret.content.find('Categories: presentation') >= 0)

def test_prompts_explain():
    from prompts.explain import Explain
    # from langchain.chat_models import ChatOpenAI
    # from langchain_community.chat_models import ChatOpenAI
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.0)
    explain = Explain(llm)

    ret = explain('SWOT')
    print(ret)



if __name__ == '__main__':
    test_prompts_classifier()
    # test_prompts_explain()
