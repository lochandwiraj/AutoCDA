AutoCDA uses a microservices architecture with event-driven workflow orchestration.



\\`\\`\\`

┌─────────────────────────────────────────────────────────────┐

│                         User Interface                       │

│                    (Streamlit/Gradio - Day 7)               │

└───────────────────────┬─────────────────────────────────────┘

&nbsp;                       │ HTTP/WebSocket

┌───────────────────────▼─────────────────────────────────────┐

│                      FastAPI Backend                         │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │

│  │   REST API   │  │  WebSocket   │  │  Auth Layer  │     │

│  └──────────────┘  └──────────────┘  └──────────────┘     │

└───────────────────────┬─────────────────────────────────────┘

&nbsp;                       │

┌───────────────────────▼─────────────────────────────────────┐

│                    Temporal.io Orchestration                 │

│                                                               │

│  ┌─────────────────────────────────────────────────────┐   │

│  │         Circuit Generation Workflow                  │   │

│  │                                                       │   │

│  │  1. NLP Intent Extraction                           │   │

│  │  2. DSL Generation                                  │   │

│  │  3. Circuit Validation                              │   │

│  │  4. SKiDL Code Generation                           │   │

│  │  5. KiCad Schematic Creation                        │   │

│  │  6. Ngspice Simulation                              │   │

│  └─────────────────────────────────────────────────────┘   │

└───────────────────────┬─────────────────────────────────────┘

&nbsp;                       │

&nbsp;       ┌───────────────┴───────────────┐

&nbsp;       │                               │

┌───────▼────────┐            ┌────────▼────────┐

│   PostgreSQL    │            │   File Storage  │

│   Database      │            │   (Schematics,  │

│                 │            │    Netlists)    │

└─────────────────┘            └─────────────────┘

```



\## Data Flow



\### 1. User Input → Intent Extraction

\- \*\*Input\*\*: Natural language description

\- \*\*Process\*\*: LLM-based extraction (OpenAI/Claude API)

\- \*\*Output\*\*: Structured intent JSON



\### 2. Intent → DSL

\- \*\*Input\*\*: Intent JSON

\- \*\*Process\*\*: Template-based DSL generation

\- \*\*Output\*\*: Circuit DSL (custom format)



\### 3. DSL → Validation

\- \*\*Input\*\*: Circuit DSL

\- \*\*Process\*\*: Rule-based electrical validation

\- \*\*Output\*\*: Validation report (pass/fail + warnings)



\### 4. DSL → SKiDL Code

\- \*\*Input\*\*: Validated DSL

\- \*\*Process\*\*: Code generation from templates

\- \*\*Output\*\*: Python SKiDL code



\### 5. SKiDL → Netlist

\- \*\*Input\*\*: SKiDL code

\- \*\*Process\*\*: Execute SKiDL script

\- \*\*Output\*\*: SPICE netlist



\### 6. Netlist → Schematic

\- \*\*Input\*\*: SPICE netlist

\- \*\*Process\*\*: KiCad CLI conversion

\- \*\*Output\*\*: .kicad\_sch file



\### 7. Netlist → Simulation

\- \*\*Input\*\*: SPICE netlist

\- \*\*Process\*\*: Ngspice execution

\- \*\*Output\*\*: Simulation results + plots



\## Technology Stack



\### Backend

\- \*\*API Framework\*\*: FastAPI (async Python)

\- \*\*Database\*\*: PostgreSQL (SQLAlchemy ORM)

\- \*\*Workflow Orchestration\*\*: Temporal.io

\- \*\*Package Manager\*\*: uv (fast Python package management)



\### Circuit Generation

\- \*\*NLP\*\*: OpenAI GPT-4 / Anthropic Claude

\- \*\*Netlist Generation\*\*: SKiDL (Python-based DSL)

\- \*\*Schematic Tool\*\*: KiCad (CLI automation)

\- \*\*Simulation\*\*: Ngspice



\### Infrastructure

\- \*\*Containerization\*\*: Docker + Docker Compose

\- \*\*CI/CD\*\*: GitHub Actions

\- \*\*Code Review\*\*: CodeRabbit.ai (automated)

\- \*\*Monitoring\*\*: Prometheus + Grafana (planned)



\## Module Breakdown



\### `app/api/` - REST API Endpoints

\- Circuit design CRUD operations

\- Simulation endpoints

\- Status/health checks



\### `app/core/` - Business Logic

\- DSL parser and generator

\- Validation engine

\- Component library management



\### `app/services/` - External Integrations

\- LLM service (OpenAI/Claude)

\- KiCad CLI wrapper

\- Ngspice wrapper

\- File storage service



\### `temporal\_workflows/` - Workflow Definitions

\- Circuit generation workflow

\- Activity definitions

\- Worker configuration



\### `app/models/` - Data Models

\- SQLAlchemy ORM models

\- Pydantic schemas for API



\## Security Considerations



\- API rate limiting

\- Input sanitization for LLM prompts

\- Sandboxed execution for generated code

\- Secure storage of API keys (environment variables)

\- HTTPS enforcement in production



\## Scalability



\- Horizontal scaling of API workers

\- Temporal.io handles workflow distribution

\- PostgreSQL connection pooling

\- CDN for static assets (schematics, plots)

EOF

```



\*\*Create DSL Specification:\*\*

```markdown

\# Save as docs/DSL\_SPEC.md



\# AutoCDA Domain-Specific Language (DSL)



\## Overview



The AutoCDA DSL is a JSON-based intermediate representation for electronic circuits.



\## Schema



\\`\\`\\`json

{

&nbsp; "circuit": {

&nbsp;   "name": "string",

&nbsp;   "type": "string",  // filter, amplifier, power\_supply, etc.

&nbsp;   "description": "string"

&nbsp; },

&nbsp; "components": \[

&nbsp;   {

&nbsp;     "id": "string",  // R1, C1, U1, etc.

&nbsp;     "type": "string",  // resistor, capacitor, ic, etc.

&nbsp;     "value": "string",  // 1k, 100n, LM741, etc.

&nbsp;     "parameters": {},  // Additional parameters

&nbsp;     "nets": \["string"]  // Connected net names

&nbsp;   }

&nbsp; ],

&nbsp; "nets": \[

&nbsp;   {

&nbsp;     "name": "string",  // VCC, GND, OUT, N1, etc.

&nbsp;     "type": "string"  // power, signal, ground

&nbsp;   }

&nbsp; ],

&nbsp; "constraints": {

&nbsp;   "frequency": "string",  // 1kHz, 100MHz, etc.

&nbsp;   "voltage": "string",  // 5V, 12V, etc.

&nbsp;   "current": "string",  // 100mA, 1A, etc.

&nbsp;   "custom": {}

&nbsp; }

}

\\`\\`\\`



\## Example: RC Low-Pass Filter



\\`\\`\\`json

{

&nbsp; "circuit": {

&nbsp;   "name": "RC Low-Pass Filter",

&nbsp;   "type": "filter",

&nbsp;   "description": "1kHz cutoff frequency"

&nbsp; },

&nbsp; "components": \[

&nbsp;   {

&nbsp;     "id": "R1",

&nbsp;     "type": "resistor",

&nbsp;     "value": "1k",

&nbsp;     "parameters": {"tolerance": "5%"},

&nbsp;     "nets": \["IN", "OUT"]

&nbsp;   },

&nbsp;   {

&nbsp;     "id": "C1",

&nbsp;     "type": "capacitor",

&nbsp;     "value": "159n",

&nbsp;     "parameters": {"voltage": "50V"},

&nbsp;     "nets": \["OUT", "GND"]

&nbsp;   }

&nbsp; ],

&nbsp; "nets": \[

&nbsp;   {"name": "IN", "type": "signal"},

&nbsp;   {"name": "OUT", "type": "signal"},

&nbsp;   {"name": "GND", "type": "ground"}

&nbsp; ],

&nbsp; "constraints": {

&nbsp;   "frequency": "1kHz",

&nbsp;   "voltage": "5V"

&nbsp; }

}

\\`\\`\\`



\## Validation Rules



1\. \*\*Component IDs\*\*: Must be unique within circuit

2\. \*\*Net Connectivity\*\*: Each component must connect to at least 2 nets

3\. \*\*Ground Reference\*\*: At least one GND net must exist

4\. \*\*Value Format\*\*: Must match regex patterns (e.g., `\\d+\[kMGµnp]?\[ΩFH]?`)

5\. \*\*Net Completeness\*\*: All nets referenced in components must be defined



\## Component Types



\- `resistor`: R value in Ohms

\- `capacitor`: C value in Farads

\- `inductor`: L value in Henries

\- `diode`: Standard or Zener

\- `transistor`: BJT or MOSFET

\- `ic`: Integrated circuits (op-amps, 555, etc.)

\- `source`: Voltage or current sources



\## Net Types



\- `power`: VCC, VDD, V+, etc.

\- `ground`: GND, VSS, 0V

\- `signal`: General purpose signal nets

EOF

```

