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

    Agent's goal is learn a policy to maximize long-term total reward:

    $\sum_{t=1}^{T}r_t$ or $\sum_{t=1}^{\infty}\gamma^tr_t$

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

    the prediction of future reward given a state and an action

    Q-value function gives expected total reward
    $$
    Q^{\pi}(s, a)=\mathbb{E}[r_{t+1}+\gamma r_{t+2}+\gamma^2r_{t+3}+...|s,a]
    $$
    It can be decompose into a Bellman equation
    $$
    Q^{\pi}(s, a)=\mathbb{E}_{s',a'}[r+\gamma Q^\pi(s',a')|s,a]
    $$

-   Model

    A model predicts what the environment will do next
    $$
    \mathcal{P}_{ss'}^a=\mathbb{P}[S_{t+1}=s'|S_t=s,A_t=a]\\
    \mathcal{R}_s^a=\mathbb{E}[R_{t+1}|S_t=s,A_t=a]
    $$
    