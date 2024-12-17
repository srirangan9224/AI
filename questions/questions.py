import nltk
import sys
import os
import string
import math
nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = {}
    for file in os.listdir(directory):
        content = open(os.path.join(directory,file)).read()
        data[file] = content
    return data



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    words= nltk.tokenize.word_tokenize(document)
    final = []
    for i in words:
        if i not in string.punctuation and i not in nltk.corpus.stopwords.words("english"):
            final.append(i)
    return final

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    idfs = {}
    keys = set()
    for doc in documents:
        keys.update(documents[doc])
    for word in keys:
        count = 0
        for i in documents.values():
            if word in i:
                count += 1
        idfs[word] = math.log(len(documents)/count)
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    top_files = {}
    for document in files:
        fullscore = 0
        content = files[document]
        for word in query:
            if word in content:
                tf = content.count(word)
                idf = idfs[word]
                score = tf * idf
                fullscore += score
        top_files[document] = fullscore
    final = [file for file,score in sorted(top_files.items(),key=lambda x:x[1])][::-1][:n]
    return final


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    top_sentences = {}
    for sentence in sentences:
        density = 0
        score = 0
        content = sentences[sentence]
        for word in query:
            if word in content:
                score += idfs[word]
                density += 1
        density /= len(content)
        top_sentences[sentence] = [score,density]

    final = [file for file,score in sorted(top_sentences.items(),key=lambda x:(x[1][0],x[1][1]))][::-1][:n]
    return final



if __name__ == "__main__":
    main()
