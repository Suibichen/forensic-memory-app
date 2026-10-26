# forensic-memory-app
### NeuroBench: Real-Time Short-Term Memory Encoding & Retrieval Testing Interface

An empirical software framework developed to analyze the mathematical correlations between visual exposure duration, cognitive load metrics, and retrieval latency. This application synthesizes core principles of computational neuroscience and cognitive psychology into a scalable, web-deployed laboratory environment for multi-subject testing. 

### Core Architectural Features

* **Counterbalanced Exposure Loop:** Employs single-exposure video playback mechanisms paired with time-bounded, automated cache-destruction sequences to isolate sensory memory pathways cleanly.
* **Granular Latency Telemetry:** Tracks reaction time metrics with high precision down to the second, mapping the mathematical distribution of retrieval speeds against multi-variant accuracy weights.
* **Cross-Examination Validation Registry:** Enforces rigorous data-integrity rules to cross-examine eyewitness validation reports across multiple physical vector domains (e.g., tracking jacket, jeans, and cap color variations).

### Technology Stack

* **Frontend/Interface:** Streamlit App Framework
* **Statistical Tracking:** Multi-variable state vectors executing concurrent session cache calculations.
* **State Preservation:** Custom continuous data logging frameworks to prevent page-refresh volatility during trial loops.

### Technical Refactoring & Optimization Strategies

### 1. State-Cache Persistence Management

In early builds of single-exposure loop simulations, the application faced data volatility limits where user actions or intermediate widget toggles would trigger accidental browser-refresh operations, prematurely resetting the global trial arrays. 

* **Resolution:** Implemented an explicit Session State lifecycle architecture (st.session_state). By mapping trials, retrieval speeds, and accuracy matrices to isolated, persistent state variables, the data pipeline maintains complete stability across multi-stage testing loops without relying on disk-write bottlenecks.

### 2. Time-Critical Boundary Cascades

Designed an automated countdown mechanism to enforce rapid-destruction boundaries on video assets, ensuring precise control over subject encoding timelines.
