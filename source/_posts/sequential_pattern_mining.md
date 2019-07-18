# Sequential Pattern Mining

## Sequence

A sequence is an ordered list of itemsets.

$\alpha$ is called a subseuquence of $\beta$, denoted as $\alpha \subseteq \beta$, if there exist indices $1\le j_1 \le j_2 \le ... \le j_n\le m$, such that $\alpha_1 \subseteq b_{j_1}, ...., a_n\subseteq b_{j_n}$.

| SID  | Sequence                                |
| ---- | --------------------------------------- |
| 1    | <{a}, {**a,b**,c},{a,**c**},{d}, {c,f}> |
| 2    | <{a,d},{c},{b,c},{a,e}>                 |
| 3    | <{e,f},{**a,b**},{d,f},{**c**},{b}>     |
| 4    | <{e},{g},{a,f},{c},{b},{c}>             |

Then <{a,b}, {c}> is a sequential pattern with support=2.

## Mining Algorithms

-   Apriori-Based Algorithms
    -   GSP
    -   SPADE
-   Pattern-Growth-Based Approaches
    -   FreeSpan
    -   PrefixSpan

### The Apriori Property

If a sequence is not frequent, then none of its super-sequence can be frequent.

### GSP

1.  Initialize candidates with all length-1 itemset.

2.  Scan the databse once, count supports for all candidates.
