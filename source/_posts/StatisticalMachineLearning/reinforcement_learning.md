---
title: Reinforcement Learning
---

[TOC]

## Introduction

-   Agent:

    At each step $t$, the agent

    -    Receives state $s_t$
    -   Receives scalar reward $r_t$
    -   Executes action $a_t$

-   Environment

    -   Receives action $a_t$
    -   Emits state $s_t$
    -   Emits scalar reward $r_t$

-   Policy

    Agent's behavior
    $$
    a=\pi(s)
    $$
    or
    $$
    \pi(a|s)=\mathbb{P}[A_t=a|S_t=s]
    $$

-   Value Function

    the prediction of future reward

    