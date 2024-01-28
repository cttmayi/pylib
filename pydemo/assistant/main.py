
from utils.spinner import Spinner

def main():

    with Spinner('Thinking ...'):
        from langchain_openai import ChatOpenAI
        from prompts.classifier import Classifier
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.0)
        embeddings = OpenAIEmbeddings()
        db = Chroma('test', embeddings, persist_directory='default.db')
        classifier = Classifier(llm, db)
        classifier.init_for_test()
        question = 'Create a presentation about climate change.'
        ret = classifier(question)
        print(ret.content)
        #assert(ret.content.find('RequiresContext: true') >= 0)
        #assert(ret.content.find('Categories: presentation') >= 0)
    print('Think Done')


if __name__ == '__main__':
    main()
