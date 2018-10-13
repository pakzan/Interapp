from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

with open('data/data.txt', 'r') as myfile:
    data = myfile.read().splitlines()
    
max_epochs = 100
vec_size = 20
alpha = 0.025

tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

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

model.save("data/d2v.model")
print("model saved")

#to find the vector of a document which is not in training data
# test_data = word_tokenize("slow down".lower())
# v1 = model.infer_vector(test_data)

# # to find most similar doc using vector
# similar_doc = model.docvecs.most_similar([v1])
# print(similar_doc)
