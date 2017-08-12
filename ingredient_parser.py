import nltk
import pycrfsuite
import sklearn_crfsuite

# w[-2]=1
# w[-1]=tsp
# w[0]=pure
# w[1]=almond
# w[2]=extract
# w[-1]|w[0]=tsp|pure
# w[0]|w[1]=pure|almond
# pos[-2]=CD
# pos[-1]=JJ
# pos[0]=NN
# pos[1]=NN
# pos[2]=NN
# pos[-2]|pos[-1]=CD|JJ
# pos[-1]|pos[0]=JJ|NN
# pos[0]|pos[1]=NN|NN
# pos[1]|pos[2]=NN|NN
# pos[-2]|pos[-1]|pos[0]=CD|JJ|NN
# pos[-1]|pos[0]|pos[1]=JJ|NN|NN
# pos[0]|pos[1]|pos[2]=NN|NN|NN

def word2features(sent, i):

    features = []
    if i >= 2:
        word_2, postag_2, *_ = sent[i-2]
        features.append('w[-2]=' + word_2)
    if i >= 1:
        word_1, postag_1, *_ = sent[i-1]
        features.append('w[-1]=' + word_1)
    word, postag, *_ = sent[i]
    features.append('w[0]=' + word)
    if i < len(sent)-1:
        word_1a, postag_1a, *_ = sent[i+1]
        features.append('w[+1]=' + word_1a)
    if i < len(sent)-2:
        word_2a, postag_2a, *_ = sent[i+2]
        features.append('w[+2]=' + word_2a)
    if i >= 1:
        features.append('w[-1]|w[0]=' + word_1 + "|" + word)
    if i < len(sent)-1:
        features.append('w[0]|w[+1]=' + word + "|" + word_1a)
    # POS
    if i >= 2:
        features.append('pos[-2]=' + postag_2)
    if i >= 1:
        features.append('pos[-1]=' + postag_1)
    features.append('pos[0]=' + postag)
    if i < len(sent)-1:
        features.append('pos[+1]=' + postag_1a)
    if i < len(sent)-2:
        features.append('pos[+2]=' + postag_2a)

    if i >= 2:
        features.append('pos[-2]|pos[-1]=' + postag_2 + "|" + postag_1)
    if i >= 1:
        features.append('pos[-1]|pos[0]=' + postag_1 + "|" + postag)
    if i < len(sent)-1:
        features.append('pos[0]|pos[1]=' + postag + "|" + postag_1a)
    if i < len(sent)-2:
        features.append('pos[1]|pos[2]=' + postag_1a + "|" + postag_2a)
    if i >= 2:
        features.append('pos[-2]|pos[-1]|pos[0]=' + postag_2 + "|" + postag_1 + "|" + postag)
    if i >= 1 and i < len(sent)-1:
        features.append('pos[-1]|pos[0]|pos[1]=' + postag_1 + "|" + postag + "|" + postag_1a)
    if i < len(sent)-2:
        features.append('pos[0]|pos[1]|pos[2]=' + postag + "|" + postag_1a + "|" + postag_2a)

    if i == 0:
        features.append('__BOS__')
        
    if i == len(sent)-1:
        features.append('__EOS__')
                
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

def open_datafile(filename):
    sentences = []
    with open(filename, "r") as f:
        sentence = []
        for line in f:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence)
                sentence = []
                continue
            sentence.append(tuple(line.split('\t')))
    return sentences

def normalize(ingredient):
    "Normalizes the string"
    return ingredient.lower()

def parse_ingredient(ingredient):
    """Parse the ingredient string.

    Returns the Tree representation of this ingredient.
    """
    crf = sklearn_crfsuite.CRF(
        model_filename='ingredient_model.crfsuite'
    )
    ingredient = normalize(ingredient)
    tok = nltk.word_tokenize(ingredient)
    pos = nltk.pos_tag(tok)
    labels = crf.predict_single(sent2features(pos))
    grammar = r"""
    AMOUNT: {<QTY>+<UNIT>?}
    INGREDIENT: {<NAME>+}
    """
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(list(zip(tok, labels)))

    return tree

def train_model():
    """Train the CRF ingredient parser model.

    The model will be saved under `ingredient_model.crfsuite`
    """
    sents = open_datafile('token_pos_tagged.txt')
    train_sents = sents[:16000]
    test_sents = sents[16000:]
    
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs', 
        c1=0.073702600562077614, 
        c2=0.0048477100797884812, 
        max_iterations=100, 
        all_possible_transitions=True,
        model_filename='ingredient_model.crfsuite',
        verbose=True
    )
    crf.fit(X_train, y_train, X_test, y_test)

if __name__ == '__main__':
    
    # train_model()
    tree = parse_ingredient("1 1/2 lb of asparagus stalks, trimmed roughly the length of your bread")
    tree.draw()
