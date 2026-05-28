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
    # Check for false page links
    if page not in corpus:
        raise Exception("Page not found in corpus")
    
    prob_dist = {}
    for key in corpus:
        prob_dist[key] = 0.0  # Initialise probabilities
    links = corpus[page]  # Possible links
    N = len(prob_dist)  # Number of keys

    # If no links, choose randomly
    if len(links) == 0:
        for key in prob_dist:
            prob_dist[key] = 1 / N  # Each key gets equal prob 
        return prob_dist

    else:
        for key in prob_dist:
            prob_dist[key] = (1 - damping_factor) / N  # Probs adjusted for damping factor

        for link in links:
            prob_dist[link] += damping_factor / len(links)  # Higher probs for links

        return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)  # Length of corpus
    pagerank_dict = {}
    for key in corpus:
        pagerank_dict[key] = 0  # Initial values of 0

    # Initialise index
    index = []
    for key in corpus:
        index.append(key)  

    r = random.randint(0, N-1)  # Random page choice
    page_visited = index[r]  # Go to page
    pagerank_dict[page_visited] += 1/n  # Add rank factor

    n_count = 1  # How many visits so far
    # Iterate over total visits
    while n_count < n:
        prob_dist = transition_model(corpus, page_visited, damping_factor)  # Next page probs
        r = random.random()

        # Add rank factor to next page and store next page
        for link, value in prob_dist.items():
            if r < value:
                page_visited = link  # Store next page
                pagerank_dict[page_visited] += 1/n  # Add rank factor
                n_count += 1
                break
            else:
                r -= value

    return pagerank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = {}
    N = len(corpus)
    for key in corpus:
        pagerank_dict[key] = 1/N

    # Random page pagerank contribution
    PR1 = (1 - damping_factor) / N
    uncertainty_met = False

    while uncertainty_met == False:
        pagerank_dict_previous = pagerank_dict.copy()  # Store previous rankings
        for page in corpus:  # Iterate over all pages
            PR2 = 0  # Linking page pagerank contribution
            for linking_page, links in corpus.items():  # Check pages with links to page

                # Equal for all pages if no links
                if len(links) == 0:
                    PR2 += damping_factor * (pagerank_dict[linking_page] / N)

                # Split between linking pages if links
                elif page in links:
                    numlinks = len(links)
                    PR2 += damping_factor * (pagerank_dict[linking_page] / numlinks)

            pagerank_dict[page] = PR1 + PR2  # Sum pagerank contributions

        # Check if needed precision met
        uncertainty_met = True
        for page in pagerank_dict:
            if abs(pagerank_dict[page] - pagerank_dict_previous[page]) >= 0.001:
                uncertainty_met = False
                break

    return pagerank_dict


if __name__ == "__main__":
    main()
