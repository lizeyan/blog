---
title: LaTex Snippets
categories: []
---

{% raw %}

``` latex
% preamble.tex
% simple macros for replacement
\newcommand{\IE}{\textit{i.e.}}
\newcommand{\EG}{\textit{e.g.}}
\newcommand{\WRT}{\textit{w.r.t.}}

% macros for math
\newcommand{\dd}{\mathrm{d}}
\newcommand{\vv}[1]{\bm{\mathrm{{#1}}}}
\newcommand{\E}{\operatorname{\mathbb{E}}}
\newcommand{\EE}[1]{\operatorname{\mathbb{E}}\left[{#1}\right]}
\newcommand{\EEE}[2]{\operatorname{\mathbb{E}}_{{#1}}\left[{#2}\right]}
\newcommand{\Var}{\operatorname{Var}}
\newcommand{\Varr}[1]{\operatorname{Var}\left[{#1}\right]}
\newcommand{\Varrr}[2]{\operatorname{Var_{{#1}}}\left[{#2}\right]}
\newcommand{\KLD}{\operatorname{KL}}
\newcommand{\KLDD}[2]{\operatorname{KL}\left[{#1}\,\big\|\,{#2}\right]}
\newcommand{\abs}[1]{\left|#1\right|}
\newcommand{\Entropy}{\operatorname{H}}
\newcommand{\Entropyy}[1]{\operatorname{H}\left[#1\right]}
%\newcommand{\T}{{\small \mathrm{T}}}

\newcommand{\anomalyprob}{\operatorname{\hat{P}}}

\newcommand{\TP}[0]{\text{TP}}
\newcommand{\TN}[0]{\text{TN}}
\newcommand{\FP}[0]{\text{FP}}
\newcommand{\FN}[0]{\text{FN}}

\newcommand{\argmax}[0]{\text{argmax}}
\newcommand{\argmin}[0]{\text{argmin}}
\newcommand{\diag}[0]{\text{diag}}

\newcommand{\dev}[1]{\textcolor{red}{#1}}

\newcommand{\ignore}[1]{\iffalse#1\fi}

% reference
\crefname{chapter}{Chapter}{Chapters}
\crefname{figure}{Fig.}{Figs}
\crefname{equation}{Eqn.}{Eqns}
\crefname{table}{Table}{Tables}
\crefformat{section}{$\S{}$#2#1#3}
\crefformat{subsection}{$\S{}$#2#1#3}
\crefformat{subsubsection}{$\S{}$#2#1#3}

\newcommand{\BR}[0]{\\~\\}
\newcommand{\tab}[1]{~~~~#1}
```

{% endraw %}