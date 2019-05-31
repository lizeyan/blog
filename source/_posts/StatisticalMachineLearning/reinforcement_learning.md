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
    

## Markov Decision Process

History is the sequence of observations ,actions, rewards
$$
H_t=O_1,R_1,A_1,...,A_{t-1},O_t,R_t
$$
Formmaly, state is a function of the history
$$
S_t=f(H_t)
$$
A state $S_t$ is Markov iff
$$
\mathbb{P}[S_{t+1}|S_t]=\mathbb{P}[S_{t+1}|S_1,...,S_t]
$$
The state is a sufficient statictic of the future. Once you get the state, you can throw the history away.

A Markov Decision Process is a tuple $<\mathcal S,\mathcal A,\mathcal P,\mathcal R,\gamma>$

$\mathcal S$ is a finite set of states.

$\mathcal A$ is a finite set of actions

$\mathcal P$ is a state transition probability matrix

$\mathcal R$ is a reward function

$\gamma$ is a discount factor



How to solve the optimal policy in MDP?

-   Value-Based RL
-   Policy-Based RL
-   Molde-Based RL



State value function $V^{\pi}(s)=E[\sum_{t=1}^{T}r_t|s]$

State-action value function $Q^{\pi}(s,a)=E[\sum_{t=1}^{T}r_t|s,a]=\sum_{s'}P(s'|s,a)(R(s,a,s')+V^{\pi}(s'))$
$$
V^{\pi}(s)=\sum_a\pi(a|s)Q(s,a)
$$


## Value Based Methods

## Policy Search

## Model-Based Method

## Deep Reinforcement Learning