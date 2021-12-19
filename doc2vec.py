from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from constant import ACTIONS, D2V_MODEL_PATH

# import nltk
# nltk.download('punkt')
# uncomment above if running for the first time

def load_model(model_path):
    return Doc2Vec.load(model_path)

def update_model(docs, model_path):
    max_epochs = 100
    vec_size = 20
    alpha = 0.025

    tagged_data = [
        TaggedDocument(words=word_tokenize(doc.lower()), tags=[str(i)]) 
        for i, doc in enumerate(docs)
    ]
    model = Doc2Vec(size=vec_size,
                    alpha=alpha, 
                    min_alpha=0.00025,
                    min_count=1,
                    dm =1)
    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        if epoch % 100 == 0:
            print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    model.save(model_path)
    print("model saved")

if __name__=="__main__":
    update_model(ACTIONS, D2V_MODEL_PATH)

#to find the vector of a document which is not in training data
# test_data = word_tokenize("slow down".lower())
# v1 = model.infer_vector(test_data)

# # to find most similar doc using vector
# similar_doc = model.docvecs.most_similar([v1])
# print(similar_doc)
