import { GeneratedDemoLesson, SubjectOption } from "./types";

export const SUBJECT_OPTIONS: SubjectOption[] = [
  {
    id: "electrical",
    label: "Electrical Eng.",
    iconName: "Lightning",
    popularTopics: ["Thevenin & Norton", "AC Phasors", "Laplace in S-domain", "Op-Amp Stability"],
    sampleProblem: "Find the Thevenin equivalent circuit across terminals A-B for a bridged-T network with 2 independent voltage sources.",
  },
  {
    id: "maths",
    label: "Mathematics",
    iconName: "Function",
    popularTopics: ["Gaussian Integrals", "Eigenvalue Decompositions", "Green's Theorem", "PDE Separation"],
    sampleProblem: "Evaluate the improper integral ∫ exp(-x²) dx from -∞ to +∞ using polar coordinate transformation.",
  },
  {
    id: "physics",
    label: "Physics",
    iconName: "Atom",
    popularTopics: ["Lagrangian Mechanics", "Maxwell's Equations", "Quantum Harmonic Oscillator", "Carnot Cycles"],
    sampleProblem: "Derive the equations of motion for a double pendulum using Euler-Lagrange formalism.",
  },
  {
    id: "chemistry",
    label: "Chemistry & ChemE",
    iconName: "Flask",
    popularTopics: ["Gibbs Free Energy", "Reaction Kinetics", "Buffer pH Equations", "Distillation Trays"],
    sampleProblem: "Derive the Henderson-Hasselbalch equation from acid dissociation constant Ka and solve for 0.1M acetate buffer.",
  },
  {
    id: "mechanical",
    label: "Mechanical Eng.",
    iconName: "GearSix",
    popularTopics: ["Navier-Stokes", "Mohr's Circle of Stress", "Bernoulli Boundary Layer", "Vibration Modes"],
    sampleProblem: "Compute principal stresses and maximum in-plane shear stress using Mohr's Circle for a shaft under combined torsion and bending.",
  },
  {
    id: "computer_science",
    label: "Theory of CS",
    iconName: "Cpu",
    popularTopics: ["Master Theorem", "NP-Completeness Proofs", "DFA Minimization", "Fast Fourier Transform"],
    sampleProblem: "Prove whether the 3-SAT problem polynomial-time reduces to Clique with step-by-step gadget construction.",
  },
];

export const DEMO_LESSON_THEVENIN: GeneratedDemoLesson = {
  id: "thevenin-circuit-01",
  title: "Thevenin Equivalent of a Bridge Network",
  subject: "Electrical Engineering",
  targetEquation: "V_{th} = V_{oc},\\quad R_{th} = \\left.\\frac{V_{oc}}{I_{sc}}\\right|_{sources=0}",
  estimatedDuration: "4 min 32 sec",
  conceptDetected: "Thevenin's Theorem & Source Deactivation",
  prerequisites: [
    "Kirchhoff's Voltage Law (KVL)",
    "Voltage Divider Principle",
    "Independent Source Zeroing (Short/Open)"
  ],
  steps: [
    {
      id: 1,
      title: "Prerequisite Recall: Why Thevenin Exists",
      duration: "0:48",
      category: "prerequisite",
      boardContent: [
        "A linear two-terminal network can be replaced by an ideal source $V_{th}$ in series with $R_{th}$.",
        "Crucial Rule: Independent voltage sources $\\rightarrow$ Short circuit ($0\\text{ V}$)",
        "Independent current sources $\\rightarrow$ Open circuit ($0\\text{ A}$)",
        "Load current relation: $I_L = \\frac{V_{th}}{R_{th} + R_L}$"
      ],
      spokenScript: "So let's work through this problem together. Before we write any numbers, let's understand why we use Thevenin's theorem. Whenever a load changes repeatedly, solving the entire five-resistor network over and over is exhausting. Thevenin proves that from the load's perspective, everything to the left collapses into a single ideal voltage source and one resistor.",
      latexSnippets: [
        "V_{th} = V_{A} - V_{B}",
        "I_{load} = \\frac{V_{th}}{R_{th} + R_L}"
      ]
    },
    {
      id: 2,
      title: "Computing Open-Circuit Voltage (V_th)",
      duration: "1:22",
      category: "concept",
      boardContent: [
        "Step 1: Remove the load resistor between terminals A and B.",
        "Notice: With terminals open, zero current flows across the bridge.",
        "Branch 1 Voltage Division: $V_A = 24\\text{ V} \\cdot \\left(\\frac{6\\,\\Omega}{6\\,\\Omega + 3\\,\\Omega}\\right) = 16.00\\text{ V}$",
        "Branch 2 Voltage Division: $V_B = 24\\text{ V} \\cdot \\left(\\frac{4\\,\\Omega}{4\\,\\Omega + 8\\,\\Omega}\\right) = 8.00\\text{ V}$",
        "Open-Circuit Voltage: $\\boxed{V_{th} = V_A - V_B = 16\\text{ V} - 8\\text{ V} = 8.00\\text{ V}}$"
      ],
      spokenScript: "Now, let's isolate terminals A and B. Notice what happens here: since the terminals are completely open, no current can cross the bridge. The circuit simply splits into two parallel voltage dividers. For Node A: 24 volts divides across 3 ohms and 6 ohms, giving us 16 volts. Repeating for Node B gives 8 volts. Taking the difference gives an open-circuit voltage of 8 volts. Let's box that answer.",
      latexSnippets: [
        "V_A = V_s \\cdot \\frac{R_2}{R_1 + R_2} = 16.00\\text{ V}",
        "\\boxed{V_{th} = 16\\text{ V} - 8\\text{ V} = 8.00\\text{ V}}"
      ]
    },
    {
      id: 3,
      title: "Deactivating Sources & Calculating R_th",
      duration: "1:35",
      category: "solution",
      boardContent: [
        "Step 2: Replace independent $24\\text{ V}$ source with a plain $0\\,\\Omega$ wire.",
        "Look into terminal A: $R_{eq1} = 3\\,\\Omega \\parallel 6\\,\\Omega = \\frac{3 \\times 6}{3 + 6} = 2.00\\,\\Omega$",
        "Look into terminal B: $R_{eq2} = 8\\,\\Omega \\parallel 4\\,\\Omega = \\frac{8 \\times 4}{8 + 4} = 2.67\\,\\Omega$",
        "Equivalent Resistance: $\\boxed{R_{th} = R_{eq1} + R_{eq2} = 2.00\\,\\Omega + 2.67\\,\\Omega = 4.67\\,\\Omega}$"
      ],
      spokenScript: "Next, we need the equivalent resistance. Remember our fundamental rule: we deactivate the 24-volt independent source by replacing it with a plain wire. Looking into terminals A and B, the top and bottom rails are now tied together. That means R1 and R2 are in parallel, and R3 and R4 are in parallel, joined in series across our terminals. Summing them gives 4.67 ohms.",
      latexSnippets: [
        "R_{th} = (R_1 \\parallel R_2) + (R_3 \\parallel R_4)",
        "\\boxed{R_{th} = 2.00\\,\\Omega + 2.67\\,\\Omega = 4.67\\,\\Omega}"
      ]
    },
    {
      id: 4,
      title: "Final Chalkboard Synthesis & Sanity Check",
      duration: "0:47",
      category: "verification",
      boardContent: [
        "Assembled Thevenin Model: $V_{th} = 8.00\\text{ V},\\; R_{th} = 4.67\\,\\Omega$",
        "Now connect the problem's test load ($R_L = 10.00\\,\\Omega$):",
        "Load Current: $\\boxed{I_L = \\frac{V_{th}}{R_{th} + R_L} = \\frac{8.00\\text{ V}}{4.67\\,\\Omega + 10.00\\,\\Omega} = 0.545\\text{ A}}$",
        "Sanity Check: Power delivered $P_L = I_L^2 \\cdot R_L = (0.545\\text{ A})^2 \\times 10\\,\\Omega = 2.97\\text{ W}$"
      ],
      spokenScript: "And that's the entire problem. Instead of wrestling with a messy 5-resistor bridge, you now have an 8-volt source in series with a 4.67 ohm resistor. If your professor asks for the current through a 10-ohm load, one simple Ohm's Law step gives 0.545 amps. Always box your final answer and verify units.",
      latexSnippets: [
        "\\boxed{I_L = \\frac{8.00\\text{ V}}{14.67\\,\\Omega} = 0.545\\text{ A}}",
        "P_L = I_L^2 \\cdot R_L = 2.97\\text{ W}"
      ]
    }
  ]
};

export const QUICK_PROMPT_PRESETS = [
  {
    title: "🌱 The Nitrogen Cycle",
    badge: "Biology & Chem",
    query: "Explain how the nitrogen cycle works from atmospheric N2 triple bond to soil bacteria fixation, nitrification, and back to the air.",
    subject: "chemistry" as const,
  },
  {
    title: "⚡ Thevenin Equivalent Circuit",
    badge: "Electrical",
    query: "Find the Thevenin equivalent circuit across terminals A-B for a bridged-T network with a 24V source and 4 bridge resistors.",
    subject: "electrical" as const,
  },
  {
    title: "∫ Integration by Parts & LIATE",
    badge: "Mathematics",
    query: "Evaluate indefinite integral of x * ln(x) dx using integration by parts and LIATE rule.",
    subject: "maths" as const,
  },
  {
    title: "📐 Navier-Stokes Boundary Layer",
    badge: "Physics / Mech",
    query: "Derive Prandtl boundary layer equations from 2D steady incompressible Navier-Stokes momentum equations.",
    subject: "physics" as const,
  },
  {
    title: "⚛️ Henderson-Hasselbalch Buffer",
    badge: "Chemistry",
    query: "Derive the Henderson-Hasselbalch equation from Ka equilibrium and calculate pH shift when adding 0.02M HCl to 0.1M acetate.",
    subject: "chemistry" as const,
  },
];
