# Formal Core
**UAF v2.0 — Mathematical Kernel**

This file contains the minimum mathematical kernel of UAF.  
Every claim in `THEORY.md` traces back to a definition here.

---

## 1. State and observation spaces

Each level $k \in \{-1, 0, 1, \ldots, 8\}$ has:
- hidden state space: $\mathcal{X}_k$
- observation space: $\mathcal{O}_k$
- belief distribution: $Q_k(s_k)$ over $\mathcal{X}_k$
- generative model: $P_k(o_k, s_k) = P_k(o_k \mid s_k)\, P_k(s_k)$

The boundary $B_k$ is the set of observable channels from $\mathcal{O}_k$ that the system can access.

---

## 2. Surprise

$$\mathcal{S}_k(o) = -\ln P_k(o), \quad P_k(o) = \int P_k(o \mid s)\, P_k(s)\, ds$$

Because $P_k(o)$ is generally intractable, systems minimize the variational upper bound.

---

## 3. Variational free energy

$$\mathcal{F}_k[Q_k] = \mathbb{E}_{Q_k(s)}\left[\ln Q_k(s) - \ln P_k(o, s)\right]$$

**Decomposition 1 (inaccuracy + complexity):**

$$\mathcal{F}_k = \underbrace{\mathbb{E}_{Q_k}[-\ln P_k(o \mid s)]}_{\text{inaccuracy}} + \underbrace{D_{\mathrm{KL}}(Q_k(s) \| P_k(s))}_{\text{complexity}}$$

**Decomposition 2 (KL from posterior + negative evidence):**

$$\mathcal{F}_k = D_{\mathrm{KL}}(Q_k(s) \| P_k(s \mid o)) - \ln P_k(o) \geq -\ln P_k(o) = \mathcal{S}_k(o)$$

Free energy is a tractable upper bound on surprise. Minimizing $\mathcal{F}$ is equivalent to approximate Bayesian inference.

---

## 4. Belief update (gradient flow)

The belief update is gradient descent on free energy:

$$\dot{Q}_k = -\nabla_{Q_k} \mathcal{F}_k + \eta(t)$$

For a Gaussian model with mean $\mu_k$ and fixed variance $\sigma_k^2$:

$$\dot{\mu}_k = \pi_k \, \varepsilon_k - (\mu_k - \mu_k^{\mathrm{prior}}) / \sigma_{\mathrm{prior}}^2$$

where:
- $\varepsilon_k = o_k - \mu_k$ is the prediction error,
- $\pi_k = 1/\sigma_k^2$ is the precision (inverse variance of likelihood),
- $\mu_k^{\mathrm{prior}}$ is the prior mean (from level $k+1$).

In discrete-time form:

$$\mu_k(t+1) = \mu_k(t) - \delta_t \left[ -\pi_k \varepsilon_k + (\mu_k - \mu_k^{\mathrm{prior}}) \right]$$

---

## 5. Precision dynamics

Precision $\pi_k$ is the inverse variance assigned to prediction error signals. It governs how much the system trusts each signal:

$$\mathcal{F}_k^{\text{weighted}} = \frac{\pi_k}{2} \|\varepsilon_k\|^2 + D_{\mathrm{KL}}(Q_k \| P_k)$$

Precision itself is a learnable parameter. Its update:

$$\dot{\pi}_k = \alpha_\pi \left( \|\varepsilon_k\| - \pi_k^{-1/2} \, c_{\mathrm{target}} \right)$$

with $\alpha_\pi \ll \alpha_{\mu}$ (precision updates on a slower timescale than beliefs) and hard clip $\pi_k \in [\pi_{\min}, \pi_{\max}]$.

**v2.0 constraint:** unbounded precision leads to divergence in the presence of growing environmental non-stationarity. The clip and slow learning rate are mathematically necessary for stability, not engineering hacks.

---

## 6. Multi-level coupling

Let $\Pi_{k \to k+1}: \mathcal{X}_k \to \mathcal{X}_{k+1}$ be a representation map (e.g., a learned neural network or a fixed sufficient statistic).

The cross-level coherence penalty:

$$\mathcal{C}_{k \to k+1} = \lambda_k \, D_{\mathrm{KL}}\!\left(\Pi_{k \to k+1} Q_k \| Q_{k+1}\right)$$

Full multi-level objective:

$$\mathcal{F}_{\mathrm{total}} = \sum_k \mathcal{F}_k + \sum_k \lambda_k \, D_{\mathrm{KL}}(\Pi_{k \to k+1} Q_k \| Q_{k+1}) + \sum_k \gamma_k \mathcal{T}_k$$

**Hierarchy protocol:**
- Bottom-up: prediction errors $\varepsilon_k$ pass upward as inputs to $Q_{k+1}$.
- Top-down: $Q_{k+1}$ constrains the prior of $Q_k$.

Crucially: what passes upward is the **precision-weighted prediction error**, not the raw observation:

$$\mathrm{input}_{k+1} = \pi_k \cdot \varepsilon_k$$

This is the v2.0 correction to the v1.3 implementation, where raw errors were passed, causing lower-level divergence.

---

## 7. Topological complexity

A possible topological penalty based on persistent homology:

$$\mathcal{T}_k = \sum_{i} \sum_{\gamma \in H_i(\mathcal{X}_k)} \epsilon(\gamma), \quad \epsilon(\gamma) = t_{\mathrm{death}}(\gamma) - t_{\mathrm{birth}}(\gamma)$$

where $H_i$ are the $i$-th homology groups of the state space filtration and $\epsilon(\gamma)$ is the persistence (lifetime) of topological feature $\gamma$.

This connects UAF to persistent homology, Betti numbers, and Mapper algorithms, particularly for the CMB anomaly experiment (004) and the spin topology experiment (001).

---

## 8. Active inference — Expected Free Energy

For policy $\pi$ over future time horizon $\tilde{t}$, with predicted future observations $\tilde{o}$ and states $\tilde{s}$:

$$G(\pi) = \underbrace{D_{\mathrm{KL}}(Q(\tilde{o} \mid \pi) \| \tilde{P}(\tilde{o}))}_{\text{risk}} + \underbrace{\mathbb{E}_{Q(\tilde{s} \mid \pi)}\left[H\left[P(\tilde{o} \mid \tilde{s})\right]\right]}_{\text{ambiguity}}$$

Decomposition of risk: $D_{\mathrm{KL}}(Q(\tilde{o} \mid \pi) \| \tilde{P}(\tilde{o})) = $ expected surprise under $\pi$ minus entropy of preferred outcomes.

Policy selection:

$$\pi^* = \arg\min_\pi G(\pi)$$

For the discrete Gaussian case used in the Active Inference Engine:

$$G_{\mathrm{Gauss}}(\pi) = \frac{1}{2}\|\mu_{\pi} - \mu_{\mathrm{pref}}\|^2 + \frac{1}{2}\sum_j \ln(2\pi e \, \sigma_{\pi,j}^2)$$

The first term is risk (distance from preferred outcome). The second is ambiguity (entropy of predicted outcomes).

---

## 9. Outcome model update (Bayesian)

The agent maintains a Gaussian model of outcomes for each action $a$:

$$P(o \mid a) = \mathcal{N}(o; \mu_a, \Sigma_a)$$

Update after observing actual outcome $o^*$:

$$\mu_a \leftarrow (1 - \alpha)\, \mu_a + \alpha\, o^*$$
$$\Sigma_a \leftarrow \max\left[(1 - \alpha)\, \Sigma_a + \alpha\, (o^* - \mu_a)^2,\, \sigma_{\min}^2 \mathbf{I}\right]$$

This is a Bayesian exponential moving average — consistent with free energy minimization in the limit of streaming data.

---

## 10. Normalized Predictive Gain

Given model $M$, baseline $B$, dataset $D$, and loss $L$ (e.g., negative log-likelihood):

$$\mathrm{NPG}(M; D, B) = \frac{L(B, D) - L(M, D)}{L(B, D) + \varepsilon}$$

**Possible loss functions:**
- Negative log-likelihood: $L(M, D) = -\frac{1}{N}\sum_i \ln P_M(o_i)$
- Cross-entropy: $L(M, D) = -\frac{1}{N}\sum_i \sum_c y_{ic} \ln \hat{y}_{ic}$
- Brier score: $L(M, D) = \frac{1}{N}\sum_i \|P_M(o_i) - \mathbf{1}_{o_i}\|^2$
- MDL description length: $L(M, D) = K(D \mid M) + K(M)$

**Baseline invariance:** NPG is defined relative to a fixed reference baseline $B$. In the implementation, baseline must be computed before the run begins and not adapted during training. A moving baseline removes the metric's discriminative power.

---

## 11. Truth attractor

Let the free energy landscape define a potential $V(Q) = \mathcal{F}[Q]$.  
The belief dynamics:

$$\dot{Q} = -\nabla_Q V(Q) + \eta(t)$$

An attractor set is:

$$\mathcal{A} = \left\{ Q : \|\nabla_Q V(Q)\|^2 < \delta, \quad \lambda_{\max}\left(\nabla^2_Q V(Q)\right) > 0 \right\}$$

(local minimum with positive-definite Hessian, i.e., stable basin).

A theory $M$ is "true in domain $D$" to degree:

$$\mathrm{Truth}(M, D) = \mathrm{NPG}(M; D, B) \cdot \mathrm{Stability}(M, D)$$

where Stability measures how far the attractor basin extends under distributional perturbation of $D$.

---

## 12. Formula 131ym — formal statement

$$\mathcal{T}^* = \lim_{t \to \infty} \arg\min_{\mathcal{T}} \frac{1}{t} \int_0^t \left[ \sum_{i=1}^m \mathcal{F}_i(\mathcal{T} \mid o_i(\tau)) + \lambda(\tau)\, C(\{Q_i(\tau)\}) \right] d\tau$$

where:
- $\mathcal{T}$: candidate theory,
- $m$: number of agents (AI + human),
- $\mathcal{F}_i(\mathcal{T} \mid o_i)$: free energy of agent $i$ with respect to theory $\mathcal{T}$ given its observations,
- $C(\{Q_i\})$: cross-agent consistency penalty $= \frac{1}{m^2}\sum_{i,j} D_{\mathrm{KL}}(Q_i \| Q_j)$,
- $\lambda(\tau)$: consistency pressure, increasing over iterations.

Human control signal:

$$\Gamma_H(t) = \alpha\, v_{\mathrm{direction}}(t) + \beta\, \mathrm{Precision}_H(t) + \gamma\, I_{\mathrm{consistency}}(t)$$

where $v_{\mathrm{direction}}$ is the directional velocity in theory space, $\mathrm{Precision}_H$ is the sharpness of the human's rejection signal, and $I_{\mathrm{consistency}}$ is an indicator that the human enforces cross-session coherence.
