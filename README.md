# BioModel Studio: Ecological, Evolutionary & Epidemiological Dynamics

An interactive Python desktop visualization platform for simulating dynamical systems across **population ecology**, **population genetics & evolutionary dynamics**, and **mathematical epidemiology**.

The application provides real-time numerical integration for ordinary differential equations (ODE via Runge-Kutta 4(5)) alongside exact discrete-time difference recursions, interactive phase-space portraits, nullcline analysis, cobweb return maps, multi-run trajectory overlays, and publication-ready data and figure exports.

---

## Key Features

- **Collapsible Navigation Drawer (☰):**
  - Smooth collapsible sidebar organized into three major biological topic umbrellas:
    - **Ecology Models** (Single-species growth, competition, consumer-resource)
    - **Evolution Models** (Haploid & diploid selection, mutation, migration)
    - **Epidemiology Models** (SIR, SIS, SEIR compartmental dynamics)
  - Keyboard shortcut: <kbd>Ctrl</kbd>+<kbd>M</kbd> / <kbd>Cmd</kbd>+<kbd>M</kbd>.

- **Dual Continuous & Discrete Dynamics:**
  - **Continuous Mode**: Adaptive high-accuracy Runge-Kutta numerical integration (RK45).
  - **Discrete Mode**: Exact generation-by-generation difference recurrence relations visualized with stepped ladder plots and cobweb return maps.
  - Interactive mode badge toggle with instant visual feedback.

- **Multi-Run Comparison & Overlay Mode:**
  - **"Keep Previous Trajectories"** toggle (<kbd>Ctrl</kbd>+<kbd>K</kbd> / <kbd>Cmd</kbd>+<kbd>K</kbd>): Retains prior simulation runs faintly rendered in the background with progressive opacity scaling.
  - Live parameter sensitivity and bifurcation exploration with debounced real-time simulation.
  - Companion **Clear** button to reset background overlays with a single click.

- **Dual-View Biological Graphs:**
  - **Left Subplot**: Dynamic time series trajectories ($n(t)$, allele frequencies $p(t)/q(t)$, or epidemic compartments $S(t), I(t), R(t)$).
  - **Right Subplot**: Phase space portrait (or cobweb return map for single-variable systems) with trajectory curves, start ($\bullet$) and end ($\times$) markers, directional flow vectors, and zero-growth isoclines (nullclines).

- **Unified Export (Images & Raw Data):**
  - Save publication-quality 300 DPI raster graphics (**PNG**, **JPEG**), vector formats (**SVG**, **PDF**), or raw simulation time series (**CSV**).
  - Native file dialog automatically configures export format from file extension.

- **Model Information & Equations Badge (ℹ):**
  - Clickable info badge displaying governing differential and difference equations, variable definitions, and empirical biological scenario descriptions.

- **Light & Dark Theme Support:**
  - Modern, accessible styling with high-contrast light and dark themes.
  - Quick header toggle button (**`☀️ Light Mode` / `🌙 Dark Mode`**) or menu bar selection (**Settings $\to$ Theme**).
  - Automatically synchronizes Matplotlib canvas, axes, spines, legends, and exported files.

- **Preloaded Empirical Scenarios:**
  - Curated empirical presets across models (e.g., Gause's *Paramecium* and yeast cultures, Lack's island pheasants, classic lynx-hare oscillations, sickle-cell heterozygote advantage, mutation-selection balance, COVID-19/measles latency waves).

---

## Mathematical Models Implemented

### 1. Ecology Models

#### A. Single-Species Population Growth
* **Exponential Growth Model:**
  - *Continuous ODE*:
    $$\frac{dn}{dt} = r n = (b - d) n$$
  - *Discrete Recursion*:
    $$n(t+1) = R \, n(t) = (1 + r_d) \, n(t) = (1 - d)(1 + b) \, n(t)$$
  - *Biological Scenarios*: Unchecked colonization, island introductions, bacterial binary fission in nutrient excess, and exponential demographic decline.

* **Logistic Growth Model:**
  - *Continuous ODE*:
    $$\frac{dn}{dt} = r n \left(1 - \frac{n}{K}\right)$$
  - *Discrete Recursion*:
    $$n(t+1) = n(t) + r_d \, n(t) \left(1 - \frac{n(t)}{K}\right)$$
  - *Biological Scenarios*: Density-dependent carrying capacity regulation, microbial batch culture saturation, delayed feedback overshoots, period-doubling bifurcations, and deterministic chaos in discrete time.

---

#### B. Competition & Multi-Species Interactions
* **Lotka-Volterra Model of Competition:**
  - *Continuous ODE*:
    $$\frac{dn_1}{dt} = r_1 n_1 \left(1 - \frac{n_1 + \alpha_{12} n_2}{K_1}\right)$$
    $$\frac{dn_2}{dt} = r_2 n_2 \left(1 - \frac{n_2 + \alpha_{21} n_1}{K_2}\right)$$
  - *Discrete Recursion*:
    $$n_1(t+1) = n_1(t) + r_1 n_1(t) \left(1 - \frac{n_1(t) + \alpha_{12} n_2(t)}{K_1}\right)$$
    $$n_2(t+1) = n_2(t) + r_2 n_2(t) \left(1 - \frac{n_2(t) + \alpha_{21} n_1(t)}{K_2}\right)$$
  - *Interaction Classification*:

    | $\alpha_{12}$ | $\alpha_{21}$ | Ecological Relationship |
    | :---: | :---: | :--- |
    | $-$ | $-$ | **Mutualistic** |
    | $-$ | $0$ | **Commensal** |
    | $0$ | $-$ | **Commensal** |
    | $+$ | $-$ | **Parasitic / Exploitative** |
    | $-$ | $+$ | **Parasitic / Exploitative** |
    | $+$ | $+$ | **Competitive** |

  - *Biological Scenarios*: Competitive exclusion (Gause's Principle), stable coexistence via niche partitioning ($\alpha_{12} < K_1/K_2$ and $\alpha_{21} < K_2/K_1$), and founder control / priority effects.

---

#### C. Consumer-Resource / Predator-Prey Models
* **General Consumer-Resource Framework:**
  $$\frac{dn_1}{dt} = f(n_1) - g(n_1, n_2)$$
  $$\frac{dn_2}{dt} = \varepsilon \, g(n_1, n_2) - h(n_2)$$

  *Modular Components*:
  - **Resource Renewal $f(n_1)$**: Constant Inflow $\theta$ (chemostat), Constant Outflow $-\psi$, Exponential $r n_1$, Logistic $r n_1(1 - n_1/K)$, Exponential Decline $r n_1 e^{-a n_1}$.
  - **Resource Consumption $g(n_1, n_2)$**: Linear Type I ($a c n_1 n_2$), Saturating Type II ($\frac{a c n_1}{b + n_1} n_2$), Sigmoidal Type III ($\frac{a c n_1^k}{b + n_1^k} n_2$).
  - **Consumer Loss $h(n_2)$**: Linear mortality ($\delta n_2$), Density-dependent mortality ($(\delta + \gamma n_2) n_2$).

* **Classic Formulations:**
  - **Nutrient Inflow / Chemostat Model:** Constant abiotic substrate inflow ($\theta$) supporting consumer biomass in continuous culture bioreactors or upwelling plankton ecosystems.
  - **Classic Lotka-Volterra Predator-Prey Model:** Linear Holling Type I response yielding neutrally stable elliptical orbits and periodic boom-bust cycles.
  - **Rosenzweig-MacArthur Model:** Logistic prey growth with Holling Type II saturating functional response; exhibits stable limit cycles and the Paradox of Enrichment.
  - **Generalized Type III Predator-Prey Model:** Sigmoidal response representing predator prey-switching and physical prey refuges at low densities.
  - **Modular Custom Builder:** Interactive interface to freely pair any resource growth function with any functional response and mortality term.

---

### 2. Evolution Models (Population Genetics)

Models tracking allele frequency dynamics ($p$ for allele $A$, $q = 1 - p$ for allele $a$) under natural selection, mutation, and migration based on Otto & Day (2007).

#### A. Haploid Natural Selection
* *Continuous Allele Dynamics ODE*:
  $$\frac{dp}{dt} = s_c \, p (1 - p), \quad \text{where } s_c = \frac{W_A - W_a}{W_a}$$
* *Discrete Generational Recursion*:
  $$p(t+1) = \frac{W_A \, p(t)}{W_A \, p(t) + W_a \, (1 - p(t))}$$
* *Biological Scenarios*: Directional selection toward fixation, purifying selection against deleterious alleles, neutral evolution ($W_A = W_a$), and selective sweeps.

---

#### B. Diploid Natural Selection & Gamete Union
* *Continuous Fitness Marginals ODE*:
  $$\frac{dp}{dt} = \frac{p(1-p)}{\bar{W}} \Big[ p(W_{AA} - W_{Aa}) + (1-p)(W_{Aa} - W_{aa}) \Big]$$
  $$\bar{W} = p^2 W_{AA} + 2p(1-p) W_{Aa} + (1-p)^2 W_{aa}$$
* *Discrete Hardy-Weinberg Random Mating Recursion*:
  $$p(t+1) = \frac{p(t)^2 W_{AA} + p(t)(1-p(t)) W_{Aa}}{\bar{W}(t)}$$
* *Biological Scenarios*:
  - **Directional Selection**: Additive fitness advantage driving dominant or additive alleles to fixation.
  - **Heterozygote Advantage (Overdominance)**: Heterozygote fitness exceeds homozygotes ($W_{Aa} > W_{AA}, W_{aa}$), maintaining stable balanced polymorphism (e.g., sickle-cell trait under malaria pressure).
  - **Heterozygote Disadvantage (Underdominance)**: Disruptive selection with an unstable threshold equilibrium.
  - **Dominance vs. Recessiveness**: Masked recessive alleles rising slowly when rare vs. dominant alleles fixing slowly.

---

#### C. Mutation-Selection Balance & Dynamics
* *Continuous Selection & Two-Way Mutation ODE*:
  $$\frac{dp}{dt} = s_c \, p(1-p) - \mu \, p + \nu \, (1-p)$$
* *Discrete Selection & Mutation Recursion*:
  $$p^* = \frac{W_A \, p(t)}{W_A \, p(t) + W_a \, (1 - p(t))}, \quad p(t+1) = p^* (1 - \mu) + (1 - p^*) \nu$$
* *Biological Scenarios*:
  - **Null Hypothesis: Neutral Drift**: Equal fitness ($W_A = W_a$) and zero mutation ($\mu = \nu = 0$) preserving allele frequencies.
  - **Mutation-Selection Balance**: Purifying selection balanced by recurrent forward mutation ($\mu$), maintaining mutation load ($\hat{q} \approx \mu / s$).
  - **Mutational Equilibrium**: Opposing mutation rates ($\mu, \nu$) equilibrating at $\hat{p} = \nu / (\mu + \nu)$.

---

#### D. Continent-Island Migration & Selection
* *Continuous Selection & Mainland Gene Flow ODE*:
  $$\frac{dp}{dt} = s_c \, p(1-p) + m \, (p_m - p)$$
* *Discrete Selection & Island Gene Flow Recursion*:
  $$p^* = \frac{W_A \, p(t)}{W_A \, p(t) + W_a \, (1 - p(t))}, \quad p(t+1) = (1 - m) p^* + m \, p_m$$
* *Biological Scenarios*:
  - **Migration-Selection Balance**: Local adaptation maintained against continuous influx of maladapted continental migrants ($p_m$).
  - **Gene Swamping**: High migration overpowers weak local selection ($m > s$), eradicating locally adapted alleles.
  - **Island Rescue**: Continuous immigration of an advantageous mainland allele rescuing depleted island populations.
  - **Neutral Gene Flow**: In the absence of selection, island allele frequency asymptotically approaches mainland frequency $p_m$.

---

### 3. Epidemiology Models (Infectious Disease Dynamics)

Compartmental epidemiological models tracking disease transmission, herd immunity, and containment interventions.

#### A. Classic SIR Model (Kermack & McKendrick)
Tracks Susceptible ($S$), Infectious ($I$), and Recovered ($R$) hosts in a closed population:
* *Continuous ODE*:
  $$\frac{dS}{dt} = -\beta S I, \quad \frac{dI}{dt} = \beta S I - \gamma I, \quad \frac{dR}{dt} = \gamma I$$
* *Discrete Recursion*:
  $$\Delta I = \min(S(t), \, \beta S(t) I(t)), \quad \Delta R = \min(I(t), \, \gamma I(t))$$
  $$S(t+1) = S(t) - \Delta I, \quad I(t+1) = I(t) + \Delta I - \Delta R, \quad R(t+1) = R(t) + \Delta R$$
* *Key Indicators*:
  - **Basic Reproduction Number**: $R_0 = \frac{\beta S_0}{\gamma}$. An epidemic spreads if and only if $R_0 > 1$.
  - **Herd Immunity Threshold**: $S_c = \frac{\gamma}{\beta}$, corresponding to immune fraction $1 - \frac{1}{R_0}$.
  - **Peak Infection & Epidemic Burnout**: Peak infection occurs when $S(t) = S_c$, leaving a non-zero final size of uninfected individuals.

---

#### B. SIS Model (Endemic Diseases Without Permanent Immunity)
Models recurring infections where recovered individuals immediately return to the susceptible pool (e.g., bacterial infections, common cold):
* *Continuous ODE*:
  $$\frac{dS}{dt} = -\beta S I + \gamma I, \quad \frac{dI}{dt} = \beta S I - \gamma I$$
* *Discrete Recursion*:
  $$\Delta I = \min(S(t), \, \beta S(t) I(t)), \quad \Delta R = \min(I(t), \, \gamma I(t))$$
  $$S(t+1) = S(t) - \Delta I + \Delta R, \quad I(t+1) = I(t) + \Delta I - \Delta R$$
* *Key Indicators*:
  - **Transcritical Bifurcation**: Governed by $R_0 = \frac{\beta N}{\gamma}$.
  - **Endemic Equilibrium ($R_0 > 1$)**: Infection persists at stable steady state $I^* = N \left(1 - \frac{1}{R_0}\right)$ and $S^* = \frac{N}{R_0}$.
  - **Disease Eradication ($R_0 \le 1$)**: Pathogen decays monotonically to zero ($I \to 0, S \to N$).

---

#### C. SEIR Model with Incubation Period (Latency)
Incorporates an Exposed ($E$) compartment for individuals infected but not yet infectious during latent incubation time $\tau = 1/\sigma$:
* *Continuous ODE*:
  $$\frac{dS}{dt} = -\beta S I, \quad \frac{dE}{dt} = \beta S I - \sigma E, \quad \frac{dI}{dt} = \sigma E - \gamma I, \quad \frac{dR}{dt} = \gamma I$$
* *Discrete Recursion*:
  $$\Delta E = \min(S, \, \beta S I), \quad \Delta I = \min(E, \, \sigma E), \quad \Delta R = \min(I, \, \gamma I)$$
  $$S(t+1) = S(t) - \Delta E, \quad E(t+1) = E(t) + \Delta E - \Delta I, \quad I(t+1) = I(t) + \Delta I - \Delta R, \quad R(t+1) = R(t) + \Delta R$$
* *Key Indicators*:
  - **Latent Phase Delay**: Exposed peak $E(t)$ precedes infectious peak $I(t)$, introducing wave latency.
  - **Curve Flattening**: Extended incubation slows epidemic acceleration and spreads peak healthcare load over longer durations.
  - **Public Health Interventions**: Modeling contact rate reduction ($\beta$) via isolation, quarantine, and social distancing.

---

## Getting Started

### 1. Requirements & Setup
Clone the repository and set up a Python virtual environment:
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
- <kbd>Enter</kbd> / <kbd>Return</kbd>: Run simulation and refresh graphs
- <kbd>Ctrl</kbd>+<kbd>M</kbd> / <kbd>Cmd</kbd>+<kbd>M</kbd>: Toggle Sandwich Navigation Drawer
- <kbd>Ctrl</kbd>+<kbd>S</kbd> / <kbd>Cmd</kbd>+<kbd>S</kbd>: Open Unified Save Dialog (Images & CSV)
- <kbd>Ctrl</kbd>+<kbd>K</kbd> / <kbd>Cmd</kbd>+<kbd>K</kbd>: Toggle "Keep Previous Trajectories" (Overlay Mode)
- <kbd>Ctrl</kbd>+<kbd>T</kbd> / <kbd>Cmd</kbd>+<kbd>T</kbd>: Toggle Light / Dark Theme

### 4. Running the Test Suite
Run the full test suite (covering ODE integration, discrete difference recursions, GUI components, and PEP 8 linter compliance):
```bash
python tests/run_tests.py
```

---

## References

1. **Otto, S. P., & Day, T. (2007).** *A Biologist's Guide to Mathematical Modeling in Ecology and Evolution.* Princeton University Press.
2. **Kermack, W. O., & McKendrick, A. G. (1927).** A contribution to the mathematical theory of epidemics. *Proceedings of the Royal Society of London. Series A*, 115(772), 700–721.
3. **Lotka, A. J. (1925).** *Elements of Physical Biology.* Williams & Wilkins.
4. **Volterra, V. (1926).** Fluctuations in the abundance of a species considered mathematically. *Nature*, 118, 558–560.
5. **Holling, C. S. (1959).** The components of predation as revealed by a study of small-mammal predation of the European pine sawfly. *The Canadian Entomologist*, 91(5), 293–320.
6. **Rosenzweig, M. L., & MacArthur, R. H. (1963).** Graphical representation and stability conditions of predator-prey interactions. *The American Naturalist*, 97(895), 209–223.
