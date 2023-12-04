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
    """
    PR(p) = (1 - d)/N + (d * Sigma_i { PR(i) / NumLinks(i) } )
    In this formula, d is the damping factor, N is the total number of pages in the corpus,
    i ranges over all pages that link to page p, and NumLinks(i) is the number of links present on page i.
    """
    # 1 - Def. the result dictionary to return, starting each page(key) with 1/N rank
    pageRanks = dict()
    pages_list = list(corpus.keys())
    num_Pages = len(pages_list)
    for page in pages_list:
        pageRanks[page] = 1 / num_Pages

    # 2 - Using the iteration method and the formula in the comment, we will fix the pageranks
    # we need to go-through all pages, and check if they link to the current page.
    # if so, we need to add rank to the current page according to the linking page PR.
    # This process should repeat until no PageRank value changes by more than 0.001 between
    # the current rank values and the new rank values.
    # Track the changes in each iteration, the stop condition will be all vals of changes are under threshold
    track_changes = {}
    threshold = 0.001
    for page in pages_list:
        track_changes[page] = threshold + 0.01

    while any(value > threshold for value in track_changes.values()):
        for current_page_updated in pages_list:
            sigma = 0
            for linking_page in pages_list:
                # go through all pages, check if they link to the current page of we are updating (it's PR)
                if current_page_updated in corpus[linking_page]:
                    sigma += pageRanks[linking_page] / len(corpus[linking_page])  # PR(i)/numlink(i)
                # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                elif len(corpus[linking_page]) == 0:
                    sigma += pageRanks[linking_page] / len(pages_list)

            old_Rank = pageRanks[current_page_updated]
            new_Rank = ((1 - damping_factor) / num_Pages) + (damping_factor * sigma) # given formula

            change = abs(old_Rank - new_Rank)
            pageRanks[current_page_updated] = new_Rank
            track_changes[current_page_updated] = change

    return pageRanks


if __name__ == "__main__":
    main()
