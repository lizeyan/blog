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

    Q-value function gives expected total reward
    $$
    Q^{\pi}(s, a)=\mathbb{E}[r_{t+1}+\gamma r_{t+2}+\gamma^2r_{t+3}+...|s,a]
    $$
    