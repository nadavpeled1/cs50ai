import os
import random
import re
import sys

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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    """
    The corpus is a Python dictionary mapping a page name to a set of all pages linked to by that page.
    The page is a string representing which page the random surfer is currently on.
    The damping_factor is a floating point number representing the damping factor to be used when generating the probabilities.
    """
    # we define an empty dict that will be the returned prob_dist
    probab_dist = dict()

    # 1 - Every page in corpus gets an initial value of :
    #   for each pg, dict[pg] = (1/NumOfPages) * (1 - d)
    for pg in corpus:
        probab_dist[pg] = 1 / (len(corpus)) * (1 - damping_factor)

    # 2 - Each linked page of the possible links of 'page' gets an equal amount of the remain probability to sum to 1
    # which is: d * 1/(numOfPossibleLinks)
    for link in corpus[page]:
        probab_dist[link] += damping_factor * (1 / len(corpus[page]))

    return probab_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # 1 Init a result dict() with the the pages as keys
    pages_list = list(corpus.keys())
    page_ranks = dict()
    for pg in pages_list:  # init rank 0 for each page. Ultimately all will sum up to 1.
        page_ranks[pg] = 0

    # 2 We random the first page to begin with with random.choice.
    first_page = random.choice(pages_list)
    page_ranks[first_page] += (1 / n)  # add the probability for the first random pick
    next_probab = transition_model(corpus, first_page, damping_factor)

    # 3 we go 'n' times in a loop, randomizing the next link:
    # Each time, randomizing a page according to the transition model of the current page.
    # After that, we add a token to the resulted page, and updating the transition model for the next iteration
    for i in range(n - 1):  # we decrease 1 because we already random the first one
        current_page = random.choices(list(next_probab.keys()), list(next_probab.values()))[0]
        page_ranks[current_page] += (1 / n)
        next_probab = transition_model(corpus, current_page, damping_factor)

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
