# BioModel Studio: Ecological & Evolutionary Dynamics

An interactive Python desktop visualization software for exploring classic biological interaction models in population ecology and evolutionary dynamics.

The application models **Lotka-Volterra Competition & Multi-Species Interactions** and **General Consumer-Resource / Predator-Prey Systems**, providing real-time ODE numerical integration, phase-space portraits, and high-resolution JPEG graph exports.

---

## Key Features

- **Light & Dark Themes + Top Settings Menu:**
  - Designed with a clean **Light Theme by default**, with full support for **Dark Theme**.
  - Accessible via macOS top menu bar: **`Settings` $\to$ `Theme` $\to$ `Light Theme` / `Dark Theme`**.
  - Quick **`☀️ Light Mode` / `🌙 Dark Mode`** toggle button directly on the window header.
  - Automatically adapts the Matplotlib plotting canvas, backgrounds, axis labels, grids, and exported JPEG files.
- **Sandwich / Hamburger Navigation Drawer (☰):**
  - Smooth collapsible sidebar to switch between competition and consumer-resource models.
- **Dynamic Parameter & Scenario Panel:**
  - Interactive inputs with real-time badges (e.g. automatic relationship classification for mutualism, competition, parasitism, commensalism).
  - Preloaded biological scenarios (Stable Coexistence, Competitive Exclusion, Neutral Cycles, Paradox of Enrichment Limit Cycles, Chemostat Equilibria).
  - Continuous ODE solving (adaptive **Runge-Kutta RK45** and **LSODA**) and discrete-time recursion.
- **Dual-View Biological Graphs:**
  - **Left:** Population dynamics over time ($n_1(t)$ and $n_2(t)$ vs $t$).
  - **Right:** Phase space portrait ($n_2$ vs $n_1$) displaying trajectory, start ($\bullet$) and end ($\times$) states, flow direction arrows, and zero-growth isoclines (nullclines).
- **High-Resolution JPEG Export:**
  - One-click native export to 300 DPI publication-ready JPEG files.

---

## Mathematical Models Implemented

### 1. Lotka-Volterra Model of Competition & Species Interactions
$$\frac{dn_1}{dt} = r_1 n_1 \left(1 - \frac{n_1 + \alpha_{12} n_2}{K_1}\right)$$
$$\frac{dn_2}{dt} = r_2 n_2 \left(1 - \frac{n_2 + \alpha_{21} n_1}{K_2}\right)$$

| $\alpha_{12}$ | $\alpha_{21}$ | Ecological Relationship |
| :---: | :---: | :--- |
| $-$ | $-$ | **Mutualistic** |
| $-$ | $0$ | **Commensal** |
| $0$ | $-$ | **Commensal** |
| $+$ | $-$ | **Parasitic / Exploitative** |
| $-$ | $+$ | **Parasitic / Exploitative** |
| $+$ | $+$ | **Competitive** |

Also supports the discrete-time recursion version:
$$n_1(t+1) = n_1(t) + r_1 n_1(t) \left(1 - \frac{n_1(t) + \alpha_{12} n_2(t)}{K_1}\right)$$
$$n_2(t+1) = n_2(t) + r_2 n_2(t) \left(1 - \frac{n_2(t) + \alpha_{21} n_1(t)}{K_2}\right)$$

---

### 2. Consumer-Resource Models
$$\frac{dn_1}{dt} = f(n_1) - g(n_1, n_2)$$
$$\frac{dn_2}{dt} = \varepsilon \, g(n_1, n_2) - h(n_2)$$

Modular functional components:
* **Resource Renewal $f(n_1)$:**
  - Constant Inflow: $\theta$ (Abiotic / Chemostat)
  - Constant Outflow: $-\psi$
  - Exponential (Biotic): $r n_1$
  - Logistic: $r n_1 \left(1 - \frac{n_1}{K}\right)$
  - Exponential Decline: $r n_1 e^{-a n_1}$
* **Resource Consumption $g(n_1, n_2)$:**
  - Linear (Type I): $a c n_1 n_2$
  - Saturating (Type II / Holling II): $\frac{a c n_1}{b + n_1} n_2$
  - Generalized (Type III / Holling III): $\frac{a c n_1^k}{b + n_1^k} n_2$
* **Consumer Loss $h(n_2)$:**
  - Constant per capita death: $\delta n_2$
  - Density-dependent death: $(\delta + \gamma n_2) n_2$

#### Classic Configurations:
- **Nutrient Inflow / Chemostat Model:**
  $$\frac{dn_1}{dt} = \theta - a c n_1 n_2, \quad \frac{dn_2}{dt} = \varepsilon a c n_1 n_2 - \delta n_2$$
- **Classic Lotka-Volterra Predator-Prey Model:**
  $$\frac{dn_1}{dt} = r n_1 - a c n_1 n_2, \quad \frac{dn_2}{dt} = \varepsilon a c n_1 n_2 - \delta n_2$$
- **Rosenzweig-MacArthur Model:** Logistic prey growth with Holling Type II saturating response (demonstrating limit cycles and the Paradox of Enrichment).
- **Generalized Type III Model:** Sigmoidal response representing prey switching or habitat refuges.
- **Modular Custom Builder:** Freely mix and match any $f(n_1)$, $g(n_1, n_2)$, and $h(n_2)$.

---

## Getting Started

### 1. Requirements & Setup
Clone the repository and set up a virtual environment:
```bash
git clone https://github.com/deniztotuk/Biological-Modelling.git
cd Biological-Modelling

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launching the Desktop Application
```bash
python run_app.py
```

### 3. Keyboard Shortcuts
- **Enter / Return**: Run simulation and update plot
- **Ctrl + M** / **Cmd + M**: Toggle Sandwich Menu (Show / Hide)
- **Ctrl + S** / **Cmd + S**: Save Graph as JPEG

### 4. Running Automated Tests
```bash
python tests/run_tests.py
```

---

## Collaborating on GitHub

1. **Clone the repository:**
   ```bash
   git clone https://github.com/deniztotuk/Biological-Modelling.git
   ```
2. **Create a branch for new features or models:**
   ```bash
   git checkout -b feature/epidemiological-sir-models
   ```
3. **Commit and push changes:**
   ```bash
   git add .
   git commit -m "Add SIR epidemiological model"
   git push -u origin feature/epidemiological-sir-models
   ```
4. **Open a Pull Request** on GitHub for code review and merging into `main`.
