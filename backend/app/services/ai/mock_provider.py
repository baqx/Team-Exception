import re
from typing import Optional, List
from app.core.models import LessonPlan, ScenePlan, ChalkAction
from app.core.providers.ai_base import BaseAIProvider

class MockAIProvider(BaseAIProvider):
    """
    Smart Offline Mock AI provider that returns pedagogical, Organic Chemistry Tutor styled
    chalkboard lessons with authentic chalk actions, schematics, and timing intents.
    Covers Calculus, Electrical Engineering, Biology/Nitrogen Cycle, Physics, and Dynamic Fallback.
    """

    async def generate_lesson_plan(
        self,
        query: str,
        subject: str = "general",
        target_duration_sec: int = 240,
        image_bytes: Optional[bytes] = None,
        image_mime: Optional[str] = None,
        language: Optional[str] = "en",
    ) -> LessonPlan:
        q = query.lower()

        # 1. BIOLOGY / NITROGEN CYCLE / CHEMISTRY
        if any(term in q for term in ["nitrogen", "cycle", "biology", "bacteria", "rhizobium", "fixation", "nitrification", "denitrification"]):
            return LessonPlan(
                problem_title="Understanding the Nitrogen Cycle: Fixation to Denitrification",
                subject="Biology & Environmental Chemistry",
                core_concept="Biogeochemical Nitrogen Cycling & Microbial Transformation",
                prerequisites=["Molecular nitrogen triple bond (N#N)", "Oxidation states of nitrogen", "Microbial symbiosis in root nodules"],
                estimated_duration_sec=target_duration_sec,
                scenes=[
                    ScenePlan(
                        step_number=1,
                        title="Prerequisite Recall: Why Nitrogen Must Be Fixed",
                        category="prerequisite",
                        spoken_script="So let's work through the nitrogen cycle together. ... Take a deep breath: 78 percent of our atmosphere is nitrogen gas, N2. ... But notice what happens chemically: the two nitrogen atoms are locked together by an extremely strong triple covalent bond. ... Animals and plants cannot break this bond directly to synthesize DNA and proteins. ... That's why biological nitrogen fixation is the fundamental gateway of all life on Earth.",
                        key_latex_formula="N_2 \\quad (\\text{Triple Bond: } N \\equiv N, \\; \\Delta H = 945\\text{ kJ/mol})",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="\\text{Atmospheric Nitrogen: } N_2 \\; (78\\% \\text{ of air})", color="white", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="N \\equiv N \\quad (\\text{Inert Triple Bond: } 945\\text{ kJ/mol})", color="yellow", timing="synchronous"),
                            ChalkAction(action_type="write_latex", content="\\implies \\text{Plants cannot absorb } N_2 \\text{ directly}", color="cyan", timing="synchronous")
                        ]
                    ),
                    ScenePlan(
                        step_number=2,
                        title="The Complete 5-Stage Nitrogen Cycle",
                        category="concept",
                        spoken_script="Now let's sketch out the entire cycle on the board so you have the big picture. ... At the top, we have atmospheric N2. ... Diazotroph bacteria like Rhizobium in legume root nodules fix it into ammonium, NH4+. ... Next, soil bacteria like Nitrosomonas oxidize ammonium into nitrites, and then Nitrobacter oxidizes nitrites into nitrates, NO3-. ... Plants readily absorb these nitrates through their roots to build amino acids. ... Finally, denitrifying bacteria return excess nitrate back to the atmosphere as N2 gas, completing the closed cycle.",
                        key_latex_formula="\\text{Atmosphere } \\rightarrow \\text{Fixation } \\rightarrow \\text{Nitrification } \\rightarrow \\text{Assimilation } \\rightarrow \\text{Denitrification}",
                        chalk_actions=[
                            ChalkAction(action_type="draw_schematic", content="nitrogen_cycle_diagram", color="white", timing="write_first")
                        ]
                    ),
                    ScenePlan(
                        step_number=3,
                        title="Nitrification & Chemical Transformations",
                        category="solution",
                        spoken_script="Next, let's write down the key chemical equations for nitrification. ... First, ammonia is oxidized to nitrite by Nitrosomonas: 2 NH4+ plus 3 O2 yields 2 NO2- plus 4 H+ and water. ... Notice that this reaction releases acid into the soil. ... In the second step, Nitrobacter rapidly oxidizes nitrite into nitrate: 2 NO2- plus O2 yields 2 NO3-. ... Nitrate has a negative charge, allowing it to dissolve easily in soil water for plant uptake.",
                        key_latex_formula="2\\text{NH}_4^+ + 3\\text{O}_2 \\longrightarrow 2\\text{NO}_2^- + 4\\text{H}^+ + 2\\text{H}_2\\text{O}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="2\\text{NH}_4^+ + 3\\text{O}_2 \\xrightarrow{\\text{Nitrosomonas}} 2\\text{NO}_2^- + 4\\text{H}^+ + 2\\text{H}_2\\text{O}", color="cyan", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="2\\text{NO}_2^- + \\text{O}_2 \\xrightarrow{\\text{Nitrobacter}} 2\\text{NO}_3^-", color="white", timing="synchronous")
                        ]
                    ),
                    ScenePlan(
                        step_number=4,
                        title="Denitrification & Verified Cycle Balance",
                        category="verification",
                        spoken_script="And that brings us to the final stage: denitrification. ... In anaerobic soils, bacteria like Pseudomonas reduce nitrates back into nitrogen gas: nitrate to nitrite, then nitric oxide, nitrous oxide, and finally stable N2 gas escaping back into the sky. ... Without denitrification, all atmospheric nitrogen would end up trapped in the oceans. ... Always box your final key summary.",
                        key_latex_formula="\\boxed{\\text{NO}_3^- \\longrightarrow \\text{NO}_2^- \\longrightarrow \\text{NO} \\longrightarrow \\text{N}_2\\text{O} \\longrightarrow \\text{N}_2 \\uparrow}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="\\text{Anaerobic Reduction: } \\text{NO}_3^- \\rightarrow \\text{NO}_2^- \\rightarrow \\text{N}_2 \\uparrow", color="white", timing="synchronous"),
                            ChalkAction(action_type="box_answer", content="\\boxed{\\text{Closed Cycle Verified: } \\text{Atmospheric } N_2 \\text{ is fully balanced}}", color="yellow", timing="write_last")
                        ]
                    )
                ]
            )

        # 2. CALCULUS / INTEGRALS
        is_calculus = any(term in q for term in ["integral", "integrate", "calculus", "dx", "ln", "parts", "derivative"])
        if is_calculus:
            return LessonPlan(
                problem_title="Evaluate indefinite integral of x * ln(x)",
                subject="Calculus",
                core_concept="Integration by Parts & LIATE Rule",
                prerequisites=["Derivative of natural log", "Power rule of integration", "LIATE selection order"],
                estimated_duration_sec=target_duration_sec,
                scenes=[
                    ScenePlan(
                        step_number=1,
                        title="Prerequisite Recall: The LIATE Rule",
                        category="prerequisite",
                        spoken_script="So let's work through this problem together. We want to evaluate the indefinite integral of x times the natural log of x with respect to x. ... Whenever you see a product of two different function types, think integration by parts. ... Remember the LIATE rule: Logarithmic functions come before Algebraic functions. ... That tells us we must choose u = ln(x), not x.",
                        key_latex_formula="\\int x \\ln(x) \\, dx",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="\\int x \\ln(x) \\, dx", color="white", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="\\text{Recall LIATE: } \\text{Logarithmic} > \\text{Algebraic} \\implies u = \\ln(x)", color="yellow", timing="synchronous")
                        ]
                    ),
                    ScenePlan(
                        step_number=2,
                        title="Differentiating & Integrating Parts",
                        category="concept",
                        spoken_script="Now let's write down our two parts. ... On the left side, we choose u = ln(x). Differentiating gives du = 1 over x dx. ... On the right side, dv = x dx. Integrating using the power rule gives v = x squared over 2.",
                        key_latex_formula="u = \\ln(x), \\; du = \\frac{1}{x}dx, \\; dv = x dx, \\; v = \\frac{x^2}{2}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="u = \\ln(x) \\implies du = \\frac{1}{x} \\, dx", color="cyan", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="dv = x \\, dx \\implies v = \\frac{x^2}{2}", color="cyan", timing="synchronous")
                        ]
                    ),
                    ScenePlan(
                        step_number=3,
                        title="Substitution into By-Parts Formula",
                        category="solution",
                        spoken_script="Next, let's substitute everything into our integration by parts formula: u times v minus the integral of v times du. ... We get x squared over 2 times the natural log of x, minus the integral of x squared over 2, times 1 over x dx. ... Now look closely at the integrand: notice that the x in the denominator cancels with one factor of x in the numerator. ... That simplifies our integral to just 1 half times the integral of x dx.",
                        key_latex_formula="\\int u \\, dv = uv - \\int v \\, du",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="= \\frac{x^2}{2}\\ln(x) - \\int \\left(\\frac{x^2}{2}\\right)\\left(\\frac{1}{x}\\right) \\, dx", color="white", timing="write_first"),
                            ChalkAction(action_type="strike_through", content="cancel_integrand", color="yellow", cancel_label="1", timing="synchronous"),
                            ChalkAction(action_type="write_latex", content="= \\frac{x^2}{2}\\ln(x) - \\frac{1}{2}\\int x \\, dx", color="cyan", timing="synchronous")
                        ]
                    ),
                    ScenePlan(
                        step_number=4,
                        title="Final Integration & Boxed Result",
                        category="verification",
                        spoken_script="Now, integrating x one more time gives x squared over 2. ... Multiplying by 1 half gives minus x squared over 4. ... And don't forget your constant of integration, plus C. ... Factoring out x squared over 4 gives our final simplified answer. ... Always box your final result.",
                        key_latex_formula="\\boxed{\\frac{x^2}{4}\\Big(2\\ln(x) - 1\\Big) + C}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="= \\frac{x^2}{2}\\ln(x) - \\frac{x^2}{4} + C", color="white", timing="synchronous"),
                            ChalkAction(action_type="box_answer", content="\\boxed{\\frac{x^2}{4}\\Big(2\\ln(x) - 1\\Big) + C}", color="yellow", timing="write_last")
                        ]
                    )
                ]
            )

        # 3. PHYSICS / MECHANICS / FREE FALL / KINEMATICS
        is_physics = any(term in q for term in ["motion", "fall", "free fall", "gravity", "kinematics", "projectile", "velocity", "acceleration", "trajectory", "physics"])
        if is_physics or (subject and "physics" in subject.lower()):
            return LessonPlan(
                problem_title="Motion Under Free Fall: Derivation & Kinematic Analysis",
                subject="Physics & Classical Mechanics",
                core_concept="One-Dimensional Motion Under Constant Gravitational Acceleration",
                prerequisites=[
                    "Constant acceleration kinematic equations",
                    "Sign convention for displacement and gravity (a = -g)",
                    "Terminal states and zero-velocity at maximum height"
                ],
                estimated_duration_sec=target_duration_sec,
                scenes=[
                    ScenePlan(
                        step_number=1,
                        title="Prerequisite Recall: Governing Kinematic Equations",
                        category="prerequisite",
                        spoken_script="So let's work through this physics problem together. ... When an object moves solely under the influence of Earth's gravity with no air resistance, we call this free fall. ... Notice that near the Earth's surface, the acceleration is constant at 9.8 meters per second squared pointing downward. ... Let's write down our fundamental kinematic relation on the board.",
                        key_latex_formula="a(t) = -g = -9.80\\,\\text{m/s}^2, \\quad y(t) = y_0 + v_0 t - \\frac{1}{2}g t^2",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="\\text{Free Fall Condition: } a = -g = -9.80\\,\\text{m/s}^2", color="white", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="y(t) = y_0 + v_0 t - \\frac{1}{2}g t^2", color="yellow", timing="synchronous"),
                            ChalkAction(action_type="write_latex", content="v(t) = v_0 - g t", color="cyan", timing="synchronous")
                        ]
                    ),
                    ScenePlan(
                        step_number=2,
                        title="Setting Up Initial Conditions & Dropped Object",
                        category="concept",
                        spoken_script="Now let's examine what happens when an object is released from rest from a height of 45 meters. ... Because it is dropped from rest, the initial velocity v naught is exactly zero. ... Substituting v naught equals zero immediately simplifies our position equation. ... Let's solve for the exact time it takes to reach the ground.",
                        key_latex_formula="v_0 = 0\\,\\text{m/s}, \\quad y_0 = 45.0\\,\\text{m} \\implies y(t) = 45.0 - \\frac{1}{2}(9.80)t^2",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="\\text{Released from Rest: } v_0 = 0\\,\\text{m/s}, \\; y_0 = 45.0\\,\\text{m}", color="cyan", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="0 = 45.0 - 4.90 t^2", color="white", timing="synchronous")
                        ]
                    ),
                    ScenePlan(
                        step_number=3,
                        title="Calculating Time of Flight",
                        category="solution",
                        spoken_script="Next, let's isolate t squared to find the time of flight. ... 4.90 t squared equals 45.0 meters. ... Dividing 45 by 4.90 yields 9.18. ... Taking the positive square root gives 3.03 seconds. ... That is the precise duration of free fall.",
                        key_latex_formula="t = \\sqrt{\\frac{2 y_0}{g}} = \\sqrt{\\frac{2(45.0)}{9.80}} = 3.03\\,\\text{s}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="t^2 = \\frac{45.0}{4.90} = 9.184", color="white", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="t = \\sqrt{9.184} = 3.03\\,\\text{s}", color="cyan", timing="synchronous"),
                            ChalkAction(action_type="box_answer", content="\\boxed{t_{\\text{fall}} = 3.03\\,\\text{s}}", color="yellow", timing="write_last")
                        ]
                    ),
                    ScenePlan(
                        step_number=4,
                        title="Impact Velocity & Sanity Check",
                        category="verification",
                        spoken_script="Finally, let's determine the impact velocity right before striking the ground. ... Using v equals minus g times t, negative 9.8 times 3.03 gives negative 29.7 meters per second. ... The negative sign confirms the velocity vector points downward as expected. ... Always box your final answer.",
                        key_latex_formula="\\boxed{v_{\\text{impact}} = -g t = -(9.80)(3.03) = -29.7\\,\\text{m/s}}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="v_{\\text{impact}} = v_0 - g t = 0 - (9.80)(3.03)", color="white", timing="synchronous"),
                            ChalkAction(action_type="box_answer", content="\\boxed{v_{\\text{impact}} = -29.7\\,\\text{m/s} \\quad (\\text{Downward})}", color="yellow", timing="write_last")
                        ]
                    )
                ]
            )

        # 4. ELECTRICAL ENGINEERING (THEVENIN / CIRCUITS)
        is_ee = any(term in q for term in ["circuit", "thevenin", "resistor", "voltage", "current", "ohm", "bridge", "kirchhoff", "electrical"])
        if is_ee or (subject and any(ee_term in subject.lower() for ee_term in ["electrical", "circuit", "ee"])):
            return LessonPlan(
                problem_title="Thevenin Equivalent of a Bridge Network",
                subject="Electrical Engineering",
                core_concept="Thevenin Reduction & Independent Source Deactivation",
                prerequisites=["Voltage division", "Kirchhoff's Laws", "Source zeroing"],
                estimated_duration_sec=target_duration_sec,
                scenes=[
                    ScenePlan(
                        step_number=1,
                        title="Circuit Schematic & Thevenin Theorem",
                        category="prerequisite",
                        spoken_script="So let's work through this circuit problem together. ... First, let's look at the circuit schematic on our board. We have a 24-volt DC source feeding a bridge network of four resistors. ... Whenever a load resistor across terminals A and B changes repeatedly, solving the entire bridge every time is exhausting. ... Thevenin proves that any linear two-terminal circuit collapses into a single voltage source and one resistor.",
                        key_latex_formula="V_{th} = V_{oc}, \\quad R_{th} = \\left.\\frac{V_{oc}}{I_{sc}}\\right|_{sources=0}",
                        chalk_actions=[
                            ChalkAction(action_type="draw_schematic", content="circuit_bridge_schematic", color="white", timing="write_first")
                        ]
                    ),
                    ScenePlan(
                        step_number=2,
                        title="Computing Open-Circuit Voltage (V_th)",
                        category="concept",
                        spoken_script="Now let's compute our open-circuit voltage across terminals A and B. ... With terminals A and B open, zero current crosses between them. The network separates into two parallel voltage dividers. ... For Node A, 24 volts divides across 3 ohms and 6 ohms, giving 16 volts. ... Repeating for Node B across 4 ohms and 8 ohms gives 8 volts. ... Taking the difference gives an open-circuit voltage of 8 volts.",
                        key_latex_formula="\\boxed{V_{th} = V_A - V_B = 16\\text{ V} - 8\\text{ V} = 8.00\\text{ V}}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="V_A = 24\\text{ V} \\cdot \\left(\\frac{6\\,\\Omega}{3\\,\\Omega + 6\\,\\Omega}\\right) = 16.00\\text{ V}", color="cyan", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="V_B = 24\\text{ V} \\cdot \\left(\\frac{4\\,\\Omega}{4\\,\\Omega + 8\\,\\Omega}\\right) = 8.00\\text{ V}", color="cyan", timing="synchronous"),
                            ChalkAction(action_type="box_answer", content="\\boxed{V_{th} = 16\\text{ V} - 8\\text{ V} = 8.00\\text{ V}}", color="yellow", timing="write_last")
                        ]
                    ),
                    ScenePlan(
                        step_number=3,
                        title="Deactivating Sources & Calculating R_th",
                        category="solution",
                        spoken_script="Next, we calculate the internal equivalent resistance. ... Remember our fundamental rule: we deactivate the 24-volt independent source by replacing it with a plain wire. ... Looking into terminals A and B, R1 and R2 are in parallel, and R3 and R4 are in parallel. ... 3 parallel 6 is 2 ohms, and 8 parallel 4 is 2.67 ohms. ... Summing them gives 4.67 ohms.",
                        key_latex_formula="\\boxed{R_{th} = (R_1 \\parallel R_2) + (R_3 \\parallel R_4) = 4.67\\,\\Omega}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="R_{eq1} = 3\\,\\Omega \\parallel 6\\,\\Omega = 2.00\\,\\Omega", color="white", timing="write_first"),
                            ChalkAction(action_type="write_latex", content="R_{eq2} = 8\\,\\Omega \\parallel 4\\,\\Omega = 2.67\\,\\Omega", color="white", timing="synchronous"),
                            ChalkAction(action_type="box_answer", content="\\boxed{R_{th} = 2.00\\,\\Omega + 2.67\\,\\Omega = 4.67\\,\\Omega}", color="yellow", timing="write_last")
                        ]
                    ),
                    ScenePlan(
                        step_number=4,
                        title="Final Thevenin Model & Load Current",
                        category="verification",
                        spoken_script="And that is our final assembled model. ... Instead of a messy five-resistor bridge, you now have an 8-volt source in series with a 4.67 ohm resistor. ... If your homework problem asks for the current with a 10 ohm load attached, Ohm's law gives 0.545 amps. ... Always box your final answer.",
                        key_latex_formula="\\boxed{I_L = \\frac{8.00\\text{ V}}{14.67\\,\\Omega} = 0.545\\text{ A}}",
                        chalk_actions=[
                            ChalkAction(action_type="write_latex", content="I_L = \\frac{V_{th}}{R_{th} + R_L} = \\frac{8.00\\text{ V}}{4.67\\,\\Omega + 10.00\\,\\Omega}", color="white", timing="synchronous"),
                            ChalkAction(action_type="box_answer", content="\\boxed{I_L = 0.545\\text{ A}}", color="yellow", timing="write_last")
                        ]
                    )
                ]
            )

        # 4. DYNAMIC GENERAL SMART FALLBACK
        # For any query (e.g. Physics, Chemistry, CS), dynamically structure a coherent lesson
        clean_title = re.sub(r"[^a-zA-Z0-9\s]", "", query).strip()
        words = clean_title.split()[:5]
        display_title = " ".join(words).title() if words else "Step-by-Step Derivation"

        return LessonPlan(
            problem_title=f"Mastery: {display_title}",
            subject=subject.title() if subject else "Applied Sciences",
            core_concept=f"Foundational Principles of {display_title}",
            prerequisites=["Core definitions and governing laws", "Algebraic manipulation", "Dimensional sanity checks"],
            estimated_duration_sec=target_duration_sec,
            scenes=[
                ScenePlan(
                    step_number=1,
                    title="Prerequisite Recall & Governing Principles",
                    category="prerequisite",
                    spoken_script=f"So let's work through this problem together. Before we calculate anything, let's establish the foundational principle behind {display_title}. ... Always identify your known parameters and the governing equation first so you don't get lost in intermediate algebra.",
                    key_latex_formula=f"\\text{{Governing Law: }} F = ma \\quad \\text{{or}} \\quad \\Delta E = 0",
                    chalk_actions=[
                        ChalkAction(action_type="write_latex", content=f"\\text{{Target: }} \\text{{{display_title}}}", color="white", timing="write_first"),
                        ChalkAction(action_type="write_latex", content="\\text{{Identify Knowns: }} [x_0, v_0, t] \\implies \\text{{Apply Conservation Law}}", color="yellow", timing="synchronous")
                    ]
                ),
                ScenePlan(
                    step_number=2,
                    title="Setting Up the Mathematical Framework",
                    category="concept",
                    spoken_script="Now let's translate the physical concept into our mathematical framework. ... Notice what happens when we isolate our primary variable: each term directly corresponds to a component in our system. ... Let's write down the governing equation clearly on the board.",
                    key_latex_formula="y(t) = y_0 + v_0 t - \\frac{1}{2}g t^2",
                    chalk_actions=[
                        ChalkAction(action_type="write_latex", content="f(x) = a x^2 + b x + c = 0", color="cyan", timing="write_first"),
                        ChalkAction(action_type="write_latex", content="x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", color="white", timing="synchronous")
                    ]
                ),
                ScenePlan(
                    step_number=3,
                    title="Step-by-Step Algebraic Derivation",
                    category="solution",
                    spoken_script="Next, let's substitute our known values into the equation. ... Be very careful with signs and units. ... Notice that the common terms factor out cleanly, leaving us with a simplified expression ready for calculation.",
                    key_latex_formula="\\Delta x = \\frac{v_f^2 - v_i^2}{2a}",
                    chalk_actions=[
                        ChalkAction(action_type="write_latex", content="= \\frac{(24)^2 - (0)^2}{2(9.8)} = \\frac{576}{19.6}", color="white", timing="write_first"),
                        ChalkAction(action_type="write_latex", content="= 29.39\\text{ m}", color="cyan", timing="synchronous")
                    ]
                ),
                ScenePlan(
                    step_number=4,
                    title="Final Synthesis & Verification",
                    category="verification",
                    spoken_script="And that brings us to our verified final result. ... Doing a quick sanity check confirms the units are correct and the magnitude makes physical sense. ... Always box your final answer.",
                    key_latex_formula="\\boxed{\\text{Result Verified: } 29.39\\text{ m}}",
                    chalk_actions=[
                        ChalkAction(action_type="write_latex", content="\\text{Sanity Check: } [\\text{Units}] = \\frac{\\text{m}^2/\\text{s}^2}{\\text{m}/\\text{s}^2} = \\text{m} \\; \\checkmark", color="white", timing="synchronous"),
                        ChalkAction(action_type="box_answer", content="\\boxed{\\text{Final Solution Verified}}", color="yellow", timing="write_last")
                    ]
                )
            ]
        )
