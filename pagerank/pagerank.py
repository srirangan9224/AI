import os
import math
import random
import re
import sys

from copy import *

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # create a dictionary with the probabilities for each page
    value = dict()
    # create a list of pages liked to the given page and adds the given page to the list
    all_pages = list(corpus[page])
    all_pages.insert(0, page)

    # if pages are linked to the given page, then sufer should choose any page with equal probability
    if len(all_pages) != 1 and len(corpus[page]) != 0:
        for Page in all_pages:
            value[Page] = (1 - damping_factor) / len(all_pages)
        all_pages.pop(0)
        for Page in all_pages:
            value[Page] += damping_factor / len(all_pages)

    else:
        for key in corpus:
            value[key] = 1 / len(corpus)

    return value


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialise a dictionary of page ranks
    value = dict()

    # first choose a random page
    for key in corpus:
        value[key] = 0
    sample = random.choice(list(value.keys()))
    value[sample] += 1

    # the for the remaining iterations choose a page with a probability by using the transition model function
    for i in range(1, n):
        state = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(state.keys()), weights=list(state.values()), k=1)[
            0
        ]
        value[sample] += 1

    for key in value:
        value[key] /= n

    return value


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialise threshold,N,ranks,new_ranks and change in ranks (rankDelta)
    threshold = 0.001
    N = len(corpus)
    ranks = {page: (1 / N) for page in corpus}
    new_rank = {page: 0 for page in corpus}
    rankDelta = 1

    # while the change in ranks is greater than threshold value
    while rankDelta > threshold:
        rankDelta = 0

        # update page rank of the pages in new rank
        for page_1 in corpus:
            Sum = 0
            for page_2 in corpus:
                if len(corpus[page_2]) == 0:
                    Sum += ranks[page_2] / N
                elif page_1 in corpus[page_2]:
                    Sum += ranks[page_2] / len(corpus[page_2])

            pageRank = (damping_factor * Sum) + ((1 - damping_factor) / N)
            new_rank[page_1] = pageRank

        # normalise the values to sum to 1
        pageSum = sum(new_rank.values())
        for page in new_rank:
            new_rank[page] /= pageSum

        # check the change in value for the pages to see if the highest change is less than threshold
        for page in corpus:
            delta = abs(ranks[page] - new_rank[page])
            if delta > rankDelta:
                rankDelta = delta
        # update the value of ranks
        ranks = deepcopy(new_rank)

    return ranks


if __name__ == "__main__":
    main()
