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

export const DEMO_LESSON_ELEVATOR: GeneratedDemoLesson = {
  id: "elevator-apparent-weight-01",
  title: "Apparent Weight in an Accelerating Elevator",
  subject: "Classical Mechanics & Physics",
  targetEquation: "F_N = m(g \\pm a) = W \\left(1 \\pm \\frac{a}{g}\\right)",
  estimatedDuration: "3 min 45 sec",
  conceptDetected: "Newton's Second Law and Normal Force",
  prerequisites: [
    "Newton's Second Law (\\sum F = ma)",
    "Free-Body Diagrams (Normal Force vs True Gravity)",
    "Frame of Reference & Coordinate Conventions"
  ],
  steps: [
    {
      id: 1,
      title: "Foundational Gap: What Does a Scale Actually Measure?",
      duration: "0:50",
      category: "prerequisite",
      boardContent: [
        "True Weight ($W$): The gravitational pull of the Earth on mass $m$: $W = mg$ (points downward).",
        "Normal Force ($F_N$): The contact force the scale floor exerts upward on your feet.",
        "Pedagogical Truth: A bathroom scale NEVER measures your mass or gravity directly!",
        "A scale only measures the normal contact force: $\\text{Scale Reading} = F_N$."
      ],
      spokenScript: "Before we solve any equations, let's diagnose the foundational gap that trips up nearly every physics student: a scale does not measure gravity directly. It only measures the upward normal contact force it exerts on your feet to support you.",
      latexSnippets: [
        "W = mg",
        "\\text{Scale Reading} = F_N"
      ]
    },
    {
      id: 2,
      title: "Case 1: Elevator Accelerating Upward (+a)",
      duration: "1:15",
      category: "concept",
      boardContent: [
        "Coordinate convention: Define upward direction as positive ($+y$).",
        "Newton's Second Law: $\\sum F_y = F_N - mg = ma$",
        "Solve for Normal Force: $F_N = mg + ma = m(g + a)$",
        "Apparent Weight Ratio: $\\boxed{F_N = W\\left(1 + \\frac{a}{g}\\right) > W}$",
        "Physical Sensation: Floor presses upward harder — you feel distinctly HEAVIER."
      ],
      spokenScript: "When the elevator accelerates upward, the floor must not only counteract gravity, but also provide the net upward force to accelerate your mass. Setting sum of forces equal to m a gives F_N equals m times g plus a. The scale reading surges, and you feel pressed into the floor.",
      latexSnippets: [
        "\\sum F_y = F_N - mg = ma",
        "\\boxed{F_N = m(g + a)}"
      ]
    },
    {
      id: 3,
      title: "Case 2: Elevator Accelerating Downward (-a) & Free Fall",
      duration: "1:10",
      category: "solution",
      boardContent: [
        "Downward Acceleration: Acceleration vector points down ($-a$).",
        "Newton's Equation: $F_N - mg = -ma \\implies F_N = m(g - a)$",
        "Apparent Weight: $\\boxed{F_N = W\\left(1 - \\frac{a}{g}\\right) < W}$ (You feel LIGHTER).",
        "Extreme Case (Cable snaps, Free Fall $a = g$): $F_N = m(g - g) = 0\\text{ N}$",
        "Apparent Weightlessness: Scale drops to 0, even though gravity $mg$ is still fully present!"
      ],
      spokenScript: "Now consider accelerating downward. The elevator floor drops away beneath you. Rearranging gives F_N equals m times g minus a. You feel lighter. And in the catastrophic limit where the cable snaps and a equals g, the normal force drops to exactly zero. You float in apparent weightlessness.",
      latexSnippets: [
        "F_N = m(g - a)",
        "\\boxed{\\text{Free Fall: } F_N = 0\\text{ N}}"
      ]
    },
    {
      id: 4,
      title: "Summary: The Universal Apparent Weight Formula",
      duration: "0:30",
      category: "verification",
      boardContent: [
        "Universal Elevator Equation: $\\boxed{F_N = m(g \\pm a)}$",
        "• Moving with constant velocity ($a = 0$): Scale reads true weight $F_N = mg$.",
        "• Accelerating upward ($+a$): Apparent weight increases ($F_N > mg$).",
        "• Accelerating downward ($-a$): Apparent weight decreases ($F_N < mg$)."
      ],
      spokenScript: "In summary: speed does not change your weight—only acceleration does. At constant velocity, acceleration is zero and you weigh true mg. Only when acceleration is non-zero does the scale deviate as m times g plus or minus a.",
      latexSnippets: [
        "\\boxed{F_N = m(g \\pm a)}",
        "a = 0 \\implies F_N = mg"
      ]
    }
  ]
};

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
