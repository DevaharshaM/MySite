// ─── STATE & GLOBAL VARIABLES ──────────────────────────────────────────────
let activeNode = 0; // Explicitly declared state variable
const BLOGS_PER_PAGE = 6;
let currentBlogPage = 1;
let currentDemoPage = 1;
let selectedCategoryFilter = null;
let selectedDemoCategoryFilter = null;
let currentSortOrder = "newest";
let currentDemoSortOrder = "newest";

// ─── DATA ARRAYS (PRESERVED INTACT) ──────────────────────────────────────────
const nodes = [
  {
    badge:"BTech · ECE", heading:"Foundations",
    desc:"Where it all began — understanding the physical layer of computation. Circuits, signals, and systems gave me a mental model of how information moves through hardware.",
    connector:{icon:"⬡",label:"Connects to Systems",text:"Understanding circuits directly enables writing firmware that talks to peripherals at the register level."},
    cards:[
      {label:"What it is",title:"BTech in Electronics and Communication",text:"Undergraduate foundation covering analog & digital circuits, signal processing, microprocessors, and communication systems.",tags:["Circuits","Signal Processing","Microprocessors","VLSI"]},
      {label:"What I did",title:"Core Engineering Fundamentals",text:"Studied semiconductor physics, digital logic design, and embedded microcontrollers. Built prototypes using 8-bit MCUs.",tags:["8051","Logic Design","PCB Basics"]},
      {label:"What I learned",title:"The Hardware Mental Model",text:"Every software abstraction sits on physical reality. Understanding silicon teaches you why timing, power, and noise are first-class engineering problems.",tags:[]}
    ]
  },
  {
    badge:"MTech · Embedded Systems", heading:"Systems",
    desc:"Moving deeper into the machine — this phase was about making hardware do reliable, real-world work. Writing code close to metal, in real-time, with real constraints.",
    connector:{icon:"⬡",label:"Connects to Intelligence",text:"Real-time systems expertise is the foundation for deploying ML inference on constrained embedded targets."},
    cards:[
      {label:"What it is",title:"MTech in Embedded Systems",text:"Postgraduate specialisation in RTOS, MCU peripherals, power management, and hardware-software co-design.",tags:["RTOS","Bare-metal C","FreeRTOS","CAN / I2C / SPI"]},
      {label:"What I did",title:"Post-Silicon Validation & Firmware Engineering",text:"Validated silicon post-fabrication, wrote production firmware for MCUs, and debugged hardware with oscilloscopes and logic analysers.",tags:["JTAG","Firmware","Validation","Debugging"]},
      {label:"What I learned",title:"Reliability is a Design Choice",text:"Real-time means guarantees, not averages. Learned how to reason about timing, memory safety, and fault handling in constrained environments.",tags:[]}
    ]
  },
  {
    badge:"MSc · Artificial Intelligence", heading:"Intelligence",
    desc:"Bridging the gap between compute and cognition — this phase added machine learning as a tool in the systems engineer's toolbox, not as a separate discipline.",
    connector:{icon:"⬡",label:"Connects to Current Focus",text:"ML fundamentals + systems thinking = the ability to deploy efficient, real-time inference at the edge."},
    cards:[
      {label:"What it is",title:"MSc in Artificial Intelligence",text:"Graduate programme covering machine learning theory, deep learning, optimisation, and intelligent systems design.",tags:["ML","Deep Learning","PyTorch","Optimisation"]},
      {label:"What I did",title:"ML Fundamentals + System-Level Thinking",text:"Studied neural networks, CNNs, model training pipelines, and mapped AI concepts to embedded deployment constraints.",tags:["Neural Networks","Model Compression","Inference"]},
      {label:"What I learned",title:"Intelligence Has a Cost",text:"Every model has a compute, memory, and energy budget. Systems thinking transforms this from a limitation into a design parameter.",tags:[]}
    ]
  },
  {
    badge:"Current · Edge AI", heading:"Current Focus",
    desc:"The synthesis — bringing ML inference to microcontrollers and embedded platforms. This is where all three phases converge: hardware knowledge, firmware craft, and AI capability.",
    connector:{icon:"★",label:"The Synthesis Point",text:"Edge AI is where circuits, real-time systems, and machine learning become a single, unified engineering problem."},
    cards:[
      {label:"What it is",title:"Edge AI Systems Engineering",text:"Running trained ML models on embedded devices with strict power, memory, and latency constraints — without a cloud connection.",tags:["TensorFlow Lite","CMSIS-NN","MCU","Quantisation"]},
      {label:"What I'm building",title:"Real-Time Intelligent Decision Systems",text:"Deploying lightweight neural networks on microcontrollers for sensor fusion, anomaly detection, and on-device inference backed by an RTOS.",tags:["TFLite Micro","FreeRTOS","Cortex-M","INT8"]},
      {label:"What's next",title:"Closing the Silicon-to-Intelligence Gap",text:"Making embedded systems not just reliable and real-time, but aware — capable of learning from their environment without leaving the device.",tags:[]}
    ]
  }
];

const modalData = {
  Matter: {
    title: "Matter",
    description: "How physical matter became controllable computation.",
    explores: ["Silicon", "Doping", "Wafer fabrication", "Transistors", "CPUs"]
  },
  Computation: {
    title: "Computation",
    description: "The hidden abstractions that make software appear independent from physics.",
    explores: ["Software abstraction", "Registers", "Memory", "CPU behavior", "State"]
  },
  Interaction: {
    title: "Interaction",
    description: "The moment software crossed into physical consequence.",
    explores: ["Interfaces", "GPIO", "Sensors", "Actuators", "Physical systems"]
  },
  Coordination: {
    title: "Coordination",
    description: "Why isolated computation evolved into synchronized systems.",
    explores: ["UART", "SPI", "I2C", "Interrupts", "RTOS", "Timing"]
  },
  Intelligence: {
    title: "Intelligence",
    description: "How systems evolved from deterministic control into adaptive intelligence.",
    explores: ["Edge AI", "TinyML", "NPUs", "On-device AI", "Distributed intelligence"]
  }
};

// EXPLORATION STORAGE (DYNAMIC CONTENT)
const blogPosts = [
  {
  id:"chemistry-intelligence-part1",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:1,
  title:"Part 1 — Why Silicon?",
  subtitle:"Before processors, memory, or artificial intelligence, there is a material choice. Computation did not emerge from just any element — it emerged from silicon. The question is why.",
  date:"28th March,  2026",
  tags:["Chemistry","Silicon","Semiconductors","Systems"],
  sections:[
    {
      heading:"1. Every Material Behaves Differently",
      content:[
        {
          type:"p",
          text:"If you zoom far enough down, every system eventually becomes a question of material behavior."
        },
        {
          type:"p",
          text:"Copper moves electrons easily. Rubber resists them. Glass interacts with light differently from metal."
        },
        {
          type:"p",
          text:"Computation also depends on material behavior — specifically, how electrons move through matter."
        },
        {
          type:"quote",
          text:"The modern digital world exists because one material behaves in a very particular way."
        }
      ]
    },
    {
      heading:"2. The Periodic Table is a Map of Behavior",
      content:[
        {
          type:"p",
          text:"Elements are arranged into groups because they share similar outer electron structures."
        },
        {
          type:"p",
          text:"These outer electrons — called valence electrons — determine how atoms bond and interact."
        },
        {
          type:"p",
          text:"Silicon belongs to Group 14, meaning it has four valence electrons."
        },
        {
          type:"p",
          text:"That number turns out to be extremely important."
        }
      ]
    },
    {
      heading:"3. Why Four Electrons Matter",
      content:[
        {
          type:"p",
          text:"Atoms naturally seek stable electron configurations."
        },
        {
          type:"p",
          text:"With four valence electrons, silicon can form stable bonds in multiple directions at once."
        },
        {
          type:"p",
          text:"When billions of silicon atoms arrange together, they create an organized crystal lattice where electrons are shared across the structure."
        },
        {
          type:"quote",
          text:"At this stage, silicon is stable — but not yet useful for computation."
        }
      ]
    },
    {
      heading:"4. Why Not Carbon?",
      content:[
        {
          type:"p",
          text:"Carbon also belongs to Group 14. In theory, it can form similar structures."
        },
        {
          type:"p",
          text:"But engineering is rarely about what is theoretically possible. It is about controllability."
        },
        {
          type:"p",
          text:"Silicon became dominant because it is abundant, stable at practical temperatures, and forms a natural oxide layer useful for manufacturing."
        },
        {
          type:"p",
          text:"That oxide layer — silicon dioxide — became one of the key reasons modern chip fabrication became scalable."
        },
        {
          type:"quote",
          text:"The success of silicon was not just chemistry.\nIt was manufacturability."
        }
      ]
    },
    {
      heading:"5. The Strange Position of Silicon",
      content:[
        {
          type:"p",
          text:"Silicon sits between conductors and insulators."
        },
        {
          type:"p",
          text:"Copper allows electrons to move very freely. Rubber barely allows movement at all."
        },
        {
          type:"p",
          text:"Silicon exists somewhere in between."
        },
        {
          type:"p",
          text:"Under normal conditions, it does not conduct well enough to behave like metal."
        },
        {
          type:"p",
          text:"But under the right conditions, its behavior can be controlled."
        },
        {
          type:"quote",
          text:"That controllability is what makes computation possible."
        }
      ]
    }
  ],
  closing:{
    heading:"Closing Thought",
    paragraphs:[
      "Long before software existed, the foundations of computation were already hidden inside material behavior.",
      "The story of intelligence does not begin with algorithms or processors."
    ],
    quote:"It begins with a material capable of controlling electrons without letting them move too freely."
  },
  footer:"Part 1 of a 5-part exploration on how intelligence emerges from chemistry, structure, and computation."
},
  {
  id:"chemistry-intelligence-part2",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:2,
  title:"Part 2 — From Sand to Silicon",
  subtitle:"Silicon is everywhere. Beaches contain it. Rocks contain it. The challenge was never finding silicon — the challenge was purifying it enough for computation.",
  date:"5th April, 2026",
  tags:["Silicon","Manufacturing","Semiconductors","Materials"],
  sections:[
    {
      heading:"1. Silicon Begins as Ordinary Sand",
      content:[
        {
          type:"p",
          text:"One of the strangest things about modern computing is that its foundation begins as one of the most common materials on Earth."
        },
        {
          type:"p",
          text:"Silicon is typically found inside silica — a compound made of silicon and oxygen."
        },
        {
          type:"p",
          text:"Silica exists in sand, quartz, and rocks all around us."
        },
        {
          type:"quote",
          text:"The starting point of modern intelligence looks surprisingly ordinary."
        }
      ]
    },
    {
      heading:"2. Raw Silicon is Not Good Enough",
      content:[
        {
          type:"p",
          text:"The problem is purity."
        },
        {
          type:"p",
          text:"Computation depends on extremely predictable electrical behavior. Even tiny impurities can disrupt how electrons move through the material."
        },
        {
          type:"p",
          text:"For construction, impurities rarely matter.\nFor semiconductors, they matter enormously."
        },
        {
          type:"p",
          text:"This means raw silicon extracted from sand is still far too inconsistent for electronics."
        },
        {
          type:"quote",
          text:"A processor requires material precision far beyond what nature naturally provides."
        }
      ]
    },
    {
      heading:"3. Purification: Creating Electronic-Grade Silicon",
      content:[
        {
          type:"p",
          text:"The silicon purification process removes unwanted atoms until the material reaches extraordinary levels of purity."
        },
        {
          type:"p",
          text:"Modern semiconductor manufacturing works with silicon purity levels exceeding 99.9999999%."
        },
        {
          type:"p",
          text:"At this stage, the goal is no longer mining.\nIt is atomic-level control."
        },
        {
          type:"p",
          text:"The cleaner the crystal structure becomes, the more predictable electron behavior becomes."
        }
      ]
    },
    {
      heading:"4. Growing a Crystal",
      content:[
        {
          type:"p",
          text:"Once purified, the silicon is melted and carefully grown into a single continuous crystal."
        },
        {
          type:"p",
          text:"This process matters because random crystal structures create inconsistent electrical behavior."
        },
        {
          type:"p",
          text:"Instead, semiconductor manufacturing tries to create one highly ordered atomic structure extending throughout the material."
        },
        {
          type:"quote",
          text:"The goal is not just purity.\nThe goal is order."
        }
      ]
    },
    {
      heading:"5. Why Structure Matters",
      content:[
        {
          type:"p",
          text:"Computation depends on predictability."
        },
        {
          type:"p",
          text:"Every transistor inside a processor must behave almost identically to billions of others."
        },
        {
          type:"p",
          text:"That level of consistency only becomes possible when the underlying material itself is highly structured."
        },
        {
          type:"p",
          text:"At this point, silicon is no longer just a material."
        },
        {
          type:"quote",
          text:"It has become a controlled electronic foundation."
        }
      ]
    }
  ],
  closing:{
    heading:"Closing Thought",
    paragraphs:[
      "Modern processors are often described as products of software and electronics.",
      "But before either could exist, industry first had to learn how to control matter itself."
    ],
    quote:"The journey from sand to intelligence begins with purification, precision, and structure."
  },
  footer:"Part 2 of a 5-part exploration on how intelligence emerges from chemistry, structure, and computation."
},
  {
  id:"chemistry-intelligence-part3",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:3,
  title:"Part 3 — From Silicon to Wafer",
  subtitle:"Purified silicon alone is still not enough. Computation requires not only clean material, but a surface precise enough to build billions of microscopic structures repeatedly and reliably.",
  date:"11th April, 2026",
  tags:["Wafer","Semiconductors","Manufacturing","Silicon"],
  sections:[
    {
      heading:"1. A Crystal is Still Not a Processor",
      content:[
        {
          type:"p",
          text:"By this stage, silicon has already been purified and grown into a highly ordered crystal."
        },
        {
          type:"p",
          text:"But a crystal alone cannot perform computation."
        },
        {
          type:"p",
          text:"The challenge now becomes manufacturing — how do you build billions of microscopic electronic structures on top of this material with precision?"
        },
        {
          type:"quote",
          text:"Computation requires not just material control, but geometric control."
        }
      ]
    },
    {
      heading:"2. Slicing the Crystal",
      content:[
        {
          type:"p",
          text:"The large silicon crystal is sliced into extremely thin circular discs."
        },
        {
          type:"p",
          text:"These discs become wafers — the foundation on which processors, memory, sensors, and microcontrollers are built."
        },
        {
          type:"p",
          text:"Each wafer must remain remarkably flat and smooth."
        },
        {
          type:"p",
          text:"Even microscopic irregularities can affect how future transistor structures behave."
        },
        {
          type:"quote",
          text:"At nanometer scales, tiny imperfections become engineering problems."
        }
      ]
    },
    {
      heading:"3. Why Wafers Are Circular",
      content:[
        {
          type:"p",
          text:"The circular shape is not aesthetic."
        },
        {
          type:"p",
          text:"It emerges naturally from how the crystal itself is grown and processed."
        },
        {
          type:"p",
          text:"Circular wafers also distribute thermal and mechanical stress more evenly during manufacturing."
        },
        {
          type:"p",
          text:"This matters because semiconductor fabrication involves repeated heating, cooling, coating, etching, and chemical processing."
        }
      ]
    },
    {
      heading:"4. The Wafer as a Manufacturing Surface",
      content:[
        {
          type:"p",
          text:"A wafer is not a chip."
        },
        {
          type:"p",
          text:"It is better understood as a construction platform."
        },
        {
          type:"p",
          text:"Modern wafers may contain hundreds of identical processor dies fabricated simultaneously across a single surface."
        },
        {
          type:"p",
          text:"This is one reason semiconductor manufacturing became scalable."
        },
        {
          type:"quote",
          text:"Instead of building one processor at a time, industry learned how to manufacture entire fields of computation together."
        }
      ]
    },
    {
      heading:"5. Preparing for Structure",
      content:[
        {
          type:"p",
          text:"At this point, the wafer is still mostly passive material."
        },
        {
          type:"p",
          text:"No intelligence exists yet. No instructions execute. No logic gates operate."
        },
        {
          type:"p",
          text:"But the foundation is now ready for the next transformation."
        },
        {
          type:"p",
          text:"The surface has become precise enough to begin engineering electrical behavior directly into the material itself."
        },
        {
          type:"quote",
          text:"The wafer is where chemistry begins turning into architecture."
        }
      ]
    }
  ],
  closing:{
    heading:"Closing Thought",
    paragraphs:[
      "The modern processor is often imagined as a tiny object hidden inside a device.",
      "But before it becomes a processor, it first exists as a carefully engineered surface designed for microscopic construction."
    ],
    quote:"Before computation can emerge, matter must first become manufacturable."
  },
  footer:"Part 3 of a 5-part exploration on how intelligence emerges from chemistry, structure, and computation."
},
{
  id:"chemistry-intelligence-part4",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:4,
  title:"Part 4 — From Wafer to Transistor",
  subtitle:"A wafer is still only structured material. Intelligence begins much later — when we learn how to control the movement of electrons across specific regions of silicon.",
  date:"18th April, 2026",
  tags:["Transistor","Semiconductors","Photolithography","Electronics"],
  sections:[
    {
      heading:"1. The Problem of Control",
      content:[
        {
          type:"p",
          text:"At this stage, we have a highly purified silicon wafer with an extremely precise surface."
        },
        {
          type:"p",
          text:"But the wafer itself still does nothing."
        },
        {
          type:"p",
          text:"For computation to exist, engineers needed a way to control how electrons move through very small regions of material."
        },
        {
          type:"quote",
          text:"The challenge was no longer creating silicon.\nThe challenge was engineering behavior into it."
        }
      ]
    },
    {
      heading:"2. Writing Patterns with Light",
      content:[
        {
          type:"p",
          text:"Modern processors are not carved mechanically."
        },
        {
          type:"p",
          text:"Instead, semiconductor manufacturing uses light, chemistry, and extremely precise patterning."
        },
        {
          type:"p",
          text:"A light-sensitive layer called photoresist is applied to the wafer."
        },
        {
          type:"p",
          text:"Ultraviolet light passes through masks containing microscopic circuit patterns."
        },
        {
          type:"p",
          text:"These patterns define where future electronic structures will exist."
        },
        {
          type:"quote",
          text:"At this scale, architecture is physically printed into matter."
        }
      ]
    },
    {
      heading:"3. Doping: Changing Electrical Behavior",
      content:[
        {
          type:"p",
          text:"The next step is modifying selected regions of silicon itself."
        },
        {
          type:"p",
          text:"This process — called doping — introduces carefully chosen impurities into the material."
        },
        {
          type:"p",
          text:"Some regions gain extra electrons.\nOthers develop electron shortages called holes."
        },
        {
          type:"p",
          text:"This changes how electrical charge moves through different parts of the wafer."
        },
        {
          type:"quote",
          text:"The material is no longer uniform.\nDifferent regions now behave differently."
        }
      ]
    },
    {
      heading:"4. The Birth of the Junction",
      content:[
        {
          type:"p",
          text:"When differently doped regions meet, a junction forms."
        },
        {
          type:"p",
          text:"This boundary behaves in unusual ways."
        },
        {
          type:"p",
          text:"Current may flow under certain conditions and stop under others."
        },
        {
          type:"p",
          text:"For the first time, electrical behavior becomes controllable."
        },
        {
          type:"quote",
          text:"This is the moment silicon stops being passive material and starts behaving like a system."
        }
      ]
    },
    {
      heading:"5. The Transistor",
      content:[
        {
          type:"p",
          text:"A transistor is ultimately a controllable electronic switch."
        },
        {
          type:"p",
          text:"Small electrical signals determine whether current is allowed to flow or blocked."
        },
        {
          type:"p",
          text:"Individually, a transistor is simple."
        },
        {
          type:"p",
          text:"But modern processors contain billions of them interacting together."
        },
        {
          type:"quote",
          text:"Computation emerges when billions of microscopic switches begin coordinating behavior."
        }
      ]
    }
  ],
  closing:{
    heading:"Closing Thought",
    paragraphs:[
      "At the beginning of this series, silicon was just a material found in sand.",
      "Now it has become something else entirely — a controllable electronic structure capable of making decisions."
    ],
    quote:"The transistor is where chemistry stops looking like matter and starts looking like intelligence."
  },
  footer:"Part 4 of a 5-part exploration on how intelligence emerges from chemistry, structure, and computation."
},
  {
  id:"chemistry-intelligence-part5",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:5,
  title:"Part 5 — From Transistor to CPU",
  subtitle:"A transistor alone does not compute. Intelligence only begins to emerge when billions of switches become organized into systems capable of storing state, processing signals, and coordinating decisions.",
  date:"25th April, 2026",
  tags:["CPU","Logic Gates","Transistors","Computation"],
  sections:[
    {
      heading:"1. A Single Transistor Changes Nothing",
      content:[
        {
          type:"p",
          text:"By itself, a transistor is remarkably simple."
        },
        {
          type:"p",
          text:"It controls whether electrical current flows or stops."
        },
        {
          type:"p",
          text:"Individually, that behavior is not intelligent.\nIt is just controlled switching."
        },
        {
          type:"quote",
          text:"Computation does not emerge from a single switch.\nIt emerges from organization."
        }
      ]
    },
    {
      heading:"2. Building Logic",
      content:[
        {
          type:"p",
          text:"When transistors are connected together, they begin forming logic gates."
        },
        {
          type:"p",
          text:"These gates create predictable decision behavior:"
        },
        {
          type:"p",
          text:"AND gates require multiple conditions.\nOR gates accept alternative conditions.\nNOT gates reverse states."
        },
        {
          type:"p",
          text:"At this stage, electrical switching starts becoming logical structure."
        },
        {
          type:"quote",
          text:"Matter is no longer only conducting electricity.\nIt is beginning to process relationships."
        }
      ]
    },
    {
      heading:"3. From Logic to Memory",
      content:[
        {
          type:"p",
          text:"Logic alone is not enough."
        },
        {
          type:"p",
          text:"A useful system must also remember previous states."
        },
        {
          type:"p",
          text:"Special transistor arrangements create memory cells capable of storing binary values."
        },
        {
          type:"p",
          text:"Now the system can preserve information over time."
        },
        {
          type:"quote",
          text:"The moment a system remembers state, behavior becomes far more complex."
        }
      ]
    },
    {
      heading:"4. Coordination Through Timing",
      content:[
        {
          type:"p",
          text:"As transistor networks grow larger, coordination becomes critical."
        },
        {
          type:"p",
          text:"Signals must move in the correct order and at predictable times."
        },
        {
          type:"p",
          text:"This is why processors depend on clocks — synchronized timing systems controlling when operations occur."
        },
        {
          type:"p",
          text:"Without timing, billions of transistors would behave chaotically."
        },
        {
          type:"quote",
          text:"Computation is not only logic.\nIt is organized timing."
        }
      ]
    },
    {
      heading:"5. The CPU",
      content:[
        {
          type:"p",
          text:"Eventually, these systems become organized into processors."
        },
        {
          type:"p",
          text:"Arithmetic units perform calculations.\nRegisters store temporary state.\nControl logic coordinates execution."
        },
        {
          type:"p",
          text:"Instructions move through these structures continuously."
        },
        {
          type:"p",
          text:"Every operation — from simple addition to artificial intelligence inference — ultimately becomes orchestrated electrical behavior across billions of transistors."
        },
        {
          type:"quote",
          text:"The CPU is not a thinking machine.\nIt is a precisely coordinated system of physical decisions."
        }
      ]
    }
  ],
  closing:{
    heading:"Closing Thought",
    paragraphs:[
      "At the beginning of this series, intelligence seemed distant from chemistry.",
      "Now the connection becomes unavoidable."
    ],
    quote:"Modern computation is ultimately the result of matter organized carefully enough to control information, timing, and behavior."
  },
  footer:"Part 5 of a 5-part exploration on how intelligence emerges from chemistry, structure, and computation."
},
{
  id:"illusion-of-software",
  category:"Computation",
  series:"System Explorations",
  title:"The Illusion of Software",
  subtitle:"We often talk about software as if it exists independently from hardware. But the deeper you go into embedded systems, the harder that separation becomes to believe.",
  date:"3rd May, 2026",
  tags:["Embedded Systems","Firmware","Hardware","Systems Thinking"],
  sections:[
    {
      heading:"1. Software Feels Abstract",
      content:[
        {
          type:"p",
          text:"Most modern software development happens several layers above the machine itself."
        },
        {
          type:"p",
          text:"Frameworks call libraries. Libraries call operating systems. Operating systems eventually interact with hardware."
        },
        {
          type:"p",
          text:"At some point, the physical system underneath disappears from view."
        },
        {
          type:"quote",
          text:"Modern software succeeds partly because it hides the machine beneath it."
        }
      ]
    },
    {
      heading:"2. Embedded Systems Break the Illusion",
      content:[
        {
          type:"p",
          text:"Embedded systems feel different because the hardware never fully disappears."
        },
        {
          type:"p",
          text:"Memory is limited. Timing matters. Voltage levels matter. Physical interfaces matter."
        },
        {
          type:"p",
          text:"Even small delays can change how the system behaves."
        },
        {
          type:"quote",
          text:"In embedded systems, software is constantly negotiating with physics."
        }
      ]
    },
    {
      heading:"3. A Register Write is a Physical Event",
      content:[
        {
          type:"p",
          text:"Consider a simple firmware operation:"
        },
        {
          type:"code",
          text:"GPIOA->ODR |= (1 << 5);"
        },
        {
          type:"p",
          text:"But underneath, transistors switch states. Electrical paths change. Voltage appears on a physical pin."
        },
        {
          type:"p",
          text:"Eventually, something in the real world responds."
        },
        {
          type:"quote",
          text:"That line of code ultimately becomes movement inside silicon."
        }
      ]
    },
    {
      heading:"4. Timing Changes Everything",
      content:[
        {
          type:"p",
          text:"In many computing systems, delays are inconvenient."
        },
        {
          type:"p",
          text:"In embedded systems, delays can destabilize communication, corrupt signals, or break synchronization entirely."
        },
        {
          type:"p",
          text:"This changes how software is written."
        },
        {
          type:"p",
          text:"Correctness alone is not enough.\nBehavior must also happen at the correct time."
        },
        {
          type:"quote",
          text:"Real-time systems care not only about what happens — but when it happens."
        }
      ]
    },
    {
      heading:"5. Why This Matters for Intelligence",
      content:[
        {
          type:"p",
          text:"As computation moves toward the edge, the distinction between software and hardware becomes even less clear."
        },
        {
          type:"p",
          text:"Machine learning models now run under constraints involving power consumption, memory bandwidth, latency, thermal behavior, and scheduling."
        },
        {
          type:"p",
          text:"The model itself becomes only one part of the system."
        },
        {
          type:"quote",
          text:"At the edge, intelligence becomes a hardware problem again."
        }
      ]
    }
  ],
  closing:{
    heading:"Closing Thought",
    paragraphs:[
      "Software often feels abstract because modern systems are designed to hide physical complexity.",
      "Embedded systems rarely let you forget that complexity completely."
    ],
    quote:"The deeper you go into real systems, the more software starts disappearing.\n\nWhat remains is timing, behavior, physics, and control."
  },
  footer:""
},
  {
  id:"why-systems-need-interfaces",
  category:"Interaction",
  series:"System Explorations",
  title:"Why Systems Need Interfaces",
  subtitle:"A processor can compute internally forever. But without interfaces, it cannot observe, respond, or interact with the physical world around it.",
  date:"9th May, 2026",
  tags:["Embedded Systems","Interfaces","GPIO","Communication"],
  sections:[
    {
      heading:"1. A CPU Exists in Isolation",
      content:[
        {
          type:"p",
          text:"By the time a processor exists, an enormous amount of engineering has already happened."
        },
        {
          type:"p",
          text:"Silicon has been purified. Transistors have been fabricated. Logic has been organized into computation."
        },
        {
          type:"p",
          text:"But even after all of that, a CPU still has a limitation."
        },
        {
          type:"quote",
          text:"A processor cannot naturally see or affect the physical world."
        },
        {
          type:"p",
          text:"It only processes internal electrical states."
        }
      ]
    },
    {
      heading:"2. Reality is Not Digital",
      content:[
        {
          type:"p",
          text:"The physical world is continuous."
        },
        {
          type:"p",
          text:"Temperature changes gradually. Sound behaves as waves. Light intensity varies continuously."
        },
        {
          type:"p",
          text:"Processors, however, operate through discrete electrical states — transitions interpreted as binary information."
        },
        {
          type:"p",
          text:"This creates a boundary between computation and reality."
        },
        {
          type:"quote",
          text:"Embedded systems exist largely to bridge that boundary."
        },
        {
          type:"image",
          src:"Images/Interaction.png",
          alt:"Embedded systems interfaces and communication architecture",
          caption:"Interfaces allow computation to observe and influence the physical world."
        }
      ]
    },
    {
      heading:"3. GPIO: The Simplest Connection",
      content:[
        {
          type:"p",
          text:"One of the simplest forms of interaction is General Purpose Input/Output — GPIO."
        },
        {
          type:"p",
          text:"At first glance, GPIO feels like software changing a value."
        },
        {
          type:"code",
          text:"GPIOA->ODR |= (1 << 5);"
        },
        {
          type:"p",
          text:"But underneath, this changes voltage on a physical pin."
        },
        {
          type:"p",
          text:"Eventually, something outside the processor responds:\nen LED turns on, a relay switches, a motor moves."
        },
        {
          type:"quote",
          text:"Interfaces are where software starts influencing reality."
        }
      ]
    },
    {
      heading:"4. Why One Interface Was Not Enough",
      content:[
        {
          type:"p",
          text:"As systems became more complex, simple pins were no longer sufficient."
        },
        {
          type:"p",
          text:"Some devices needed faster communication.\nOthers needed multiple devices sharing connections.\nSome needed longer-distance reliability."
        },
        {
          type:"p",
          text:"This is why multiple communication models emerged."
        },
        {
          type:"p",
          text:"UART prioritized simplicity.\nSPI prioritized speed.\nI2C prioritized scalable device communication."
        },
        {
          type:"quote",
          text:"Different interfaces exist because systems optimize for different constraints."
        }
      ]
    },
    {
      heading:"5. Embedded Systems are Really About Interaction",
      content:[
        {
          type:"p",
          text:"At a distance, embedded systems appear to be about processors and software."
        },
        {
          type:"p",
          text:"But much of embedded engineering is actually about controlled interaction with the outside world."
        },
        {
          type:"p",
          text:"Sensors continuously feed information inward.\nActuators push decisions outward.\nCommunication buses coordinate systems together."
        },
        {
          type:"p",
          text:"The processor becomes the center of an ongoing exchange between computation and reality."
        },
        {
          type:"quote",
          text:"A processor becomes useful only when it stops computing in isolation and starts interacting with the world around it."
        }
      ]
    }
  ],
  closing:{
    heading:"Closing Thought",
    paragraphs:[
      "Modern computation often feels abstract because most systems hide the physical world beneath layers of software.",
      "Embedded systems rarely allow that separation completely."
    ],
    quote:"Interfaces are not just connections between devices.\n\nThey are connections between computation and reality."
  },
  footer:""
},
{
  id:"the-physical-edge-of-software",
  category:"Interaction",
  series:"System Explorations",
  title:"The Physical Edge of Software",
  subtitle:"How discrete logic becomes physical consequence through GPIO.",
  date:"17th May, 2026",
  tags:["Embedded Systems", "Hardware", "GPIO", "Systems Thinking"],
  sections:[
    {
      heading:"1. The Solitary Nature of Computation",
      content:[
        {
          type:"p",
          text:"Computation is, by default, an internal process. A processor can cycle through billions of instructions per second, moving data between registers and performing complex arithmetic, yet remain completely disconnected from the world surrounding it."
        },
        {
          type:"p",
          text:"In this state, software is a closed loop of logic. It exists as varying electrical charges trapped within a silicon substrate, invisible and without external consequence."
        },
        {
          type:"quote",
          text:"A system that only computes is a mind without a body. It possesses logic, but lacks agency."
        }
      ]
    },
    {
      heading:"2. GPIO: The Architecture of Intent",
      content:[
        {
          type:"p",
          text:"General Purpose Input/Output (GPIO) represents the first true boundary between the abstract world of software and the physical world of matter. It is the architectural point where a software decision manifests as an electrical reality."
        },
        {
          type:"p",
          text:"Before sophisticated communication protocols existed, the industry needed a way to let a processor interact with voltage directly. GPIO was the solution—a simple, programmable gate that allowed software to control the state of a physical pin."
        },
        {
          type:"image",
          src:"Images/GPIO.png",
          alt:"The path from software instruction to physical voltage change",
          caption:"GPIO acts as the bridge where software states are translated into physical potential."
        }
      ]
    },
    {
      heading:"3. From Memory to Matter",
      content:[
        {
          type:"p",
          text:"To a high-level developer, interacting with hardware often looks like a simple memory operation. A single line of code is written to a specific address, and the task is considered complete."
        },
        {
          type:"code",
          text:"GPIOA->ODR |= (1 << 5);"
        },
        {
          type:"p",
          text:"While this appears to be software manipulating a variable, it is actually a physical event. That instruction triggers a cascade: the processor's bus logic selects a peripheral, a register holds a bit, and that bit controls a transistor gate. That transistor then allows current to flow, changing the voltage on a physical copper lead."
        },
        {
          type:"p",
          text:"At this moment, software is no longer just information. It is energy."
        }
      ]
    },
    {
      heading:"4. The Scaling of Interaction",
      content:[
        {
          type:"p",
          text:"GPIO provides the foundation for agency, but it is inherently limited. To control a motor, we toggle it. To read a sensor, we measure it. But as systems grow in complexity, managing every physical interaction with individual pins becomes unsustainable."
        },
        {
          type:"p",
          text:"When we need to send a temperature reading, a single pin can only say 'high' or 'low.' To convey a number, we must either use many pins or begin toggling a single pin in a specific pattern over time."
        },
        {
          type:"quote",
          text:"Complexity in systems engineering is often solved by moving from raw signals to structured protocols."
        },
        {
          type:"p",
          text:"This fundamental limitation of GPIO is what necessitated the evolution of UART, SPI, and I2C. We moved from simply controlling voltage to using voltage as a language."
        }
      ]
    }
  ],
  closing:{
    heading:"Closing Thought",
    paragraphs:[
      "GPIO is often dismissed as the simplest part of embedded engineering, yet it remains the most profound. It is the moment where the wall between a logical instruction and a physical movement finally breaks down.",
      "Every complex system, no matter how advanced its intelligence, eventually relies on this single, humble transition: a bit becoming a voltage."
    ],
    quote:"Engineering is the art of making the invisible visible through controlled interaction."
  },
  footer:"Exploring the boundaries where computation meets reality."
}
];

// DEMONSTRATION STORAGE (DYNAMIC EDGE AI PROJECTS)
const demoPosts = [
  {
    id: "edge-ai-uno-mpu6050",
    category: "Intelligence",
    series: "Edge AI Prototypes",
    title: "Intelligence Under Constraint",
    subtitle: "How to squeeze a real gesture-recognition algorithm inside an Arduino Uno with only 2KB of RAM.",
    date: "23rd May, 2026",
    tags: ["Arduino Uno", "MPU6050", "Edge AI", "Fixed-Point Math"],
    sections: [
      {
        heading: "1. The 2KB RAM Wall",
        content: [
          { type: "p", text: "When we talk about Edge AI, we usually think of powerful chips, massive neural networks, and gigabytes of memory. But what happens when your target is a basic Arduino Uno running an 8-bit ATmega328P processor?" },
          { type: "p", text: "You get exactly 2 Kilobytes of SRAM. If your code uses even a byte more, the stack crashes, variables corrupt, and the system resets. On this scale, running a heavy AI framework like TensorFlow Lite is out of the question. You have to build smart, efficient code by hand." }
        ]
      },
      {
        heading: "2. The Hardware: Pulling Raw Sensor Vectors",
        content: [
          { type: "p", text: "For this setup, I wired an MPU6050 accelerometer and gyroscope to the Uno using the I2C pins (A4 and A5). The sensor continuously measures acceleration and rotation along the X, Y, and Z axes." },
          { type: "p", text: "Instead of saving hundreds of sensor readings into a massive array—which would instantly kill our 2KB RAM budget—we process the values on the fly. As soon as the raw bytes arrive over the I2C bus, we immediately convert them into basic features like averages, moving peaks, and signal direction." },
          { type: "code", text: "// Reading raw accelerometer data over the I2C bus\nWire.beginTransmission(0x68); // MPU6050 address\nWire.write(0x3B);             // Register for Accel X High Byte\nWire.endTransmission(false);\nWire.requestFrom(0x68, 6);    // Pull 6 bytes for X, Y, and Z\n\nint16_t rawX = (Wire.read() << 8) | Wire.read();" }
        ]
      },
      {
        heading: "3. Dropping Floats for Speed and Space",
        content: [
          { type: "p", text: "The Arduino Uno does not have a hardware Floating Point Unit (FPU). Every time you use a decimal number (like 1.45 or -0.82), the processor has to emulate the math via software, which is incredibly slow and blows up your compiled file size." },
          { type: "p", text: "To get around this, we use fixed-point quantization. Instead of working with decimals, we scale our values up into raw integers. For example, multiplying a threshold by 1000 lets us do all of our pattern checks using simple, lightning-fast integer logic." }
        ]
      },
      {
        heading: "4. Turning Logic Into Arrays",
        content: [
          { type: "p", text: "Instead of a deep learning model, I trained a highly optimized Decision Tree on my computer using gesture data. Once the tree structure was ready, I exported its exact boundaries as plain C++ conditional logic blocks and small arrays." },
          { type: "p", text: "The result is an automated processing path that checks raw signals against tight integer limits to map movements instantly." },
          { type: "quote", text: "if (currentAccelX > 4000) {\n  if (gyroZ < -1500) return GESTURE_WAVE;\n} else {\n  return GESTURE_IDLE;\n}" }
        ]
      }
    ],
    closing: {
      heading: "How it Performs",
      paragraphs: [
        "Because everything is written in clean, direct C++ code, the entire pattern-matching sequence runs in less than 4 milliseconds.",
        "The model uses under 1.1KB of RAM, leaving plenty of room for stable system execution. It proves you don't need expensive hardware to create an intelligent, self-contained edge device."
      ],
      quote: "True efficiency shines when you build intelligent behavior directly into the hardware limits."
    }
  }
];

// ─── NAVIGATION ──────────────────────────────────────────────────────────────
function showPage(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
  
  document.getElementById('page-' + page).classList.add('active');
  
  const navKey = (page === 'blog-post') ? 'blogs' : page;
  const navEl = document.getElementById('nav-' + navKey);
  if (navEl) navEl.classList.add('active');
  
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  if (page === 'journey') renderJourney();
  if (page === 'blogs') renderBlogs(currentBlogPage);
  if (page === 'demos') renderDemos(currentDemoPage);
}

// ─── MODAL CONTROLLERS ───────────────────────────────────────────────────────
function openModal(nodeKey) {
  const data = modalData[nodeKey];
  if (!data) return;
  
  const wrapper = document.getElementById('modal-content-wrapper');
  wrapper.innerHTML = `
    <h2 class="modal-title">${escHtml(data.title)}</h2>
    <p class="modal-desc">${escHtml(data.description)}</p>
    <div class="modal-explores-label">Explores:</div>
    <ul class="modal-explores-list">
      ${data.explores.map(item => `<li class="modal-explores-item">${escHtml(item)}</li>`).join('')}
    </ul>
    <div style="display:flex; gap:0.75rem;">
      <button class="btn-primary" style="flex:1; justify-content:center; font-size:0.8rem; padding:0.6rem;" onclick="filterLayerRoute('${nodeKey}', 'blogs')">Explorations</button>
      <button class="btn-ghost" style="flex:1; justify-content:center; font-size:0.8rem; padding:0.6rem; border-color:var(--blue); color:var(--blue);" onclick="filterLayerRoute('${nodeKey}', 'demos')">Demos</button>
    </div>
  `;
  
  document.getElementById('nodeModal').classList.add('active');
}

function closeModal(event) {
  if (event === null || event.target === document.getElementById('nodeModal')) {
    document.getElementById('nodeModal').classList.remove('active');
  }
}

function filterLayerRoute(category, targetPage) {
  document.getElementById('nodeModal').classList.remove('active');
  if (targetPage === 'blogs') {
    selectedCategoryFilter = category;
    document.getElementById('clearFilterBtn').style.display = 'block';
    document.getElementById('blogsBackToTreeBtn').style.display = 'block';
    document.getElementById('blogsPageTitle').innerText = `Articles: ${category}`;
    document.getElementById('blogsPageSubtitle').innerText = `Showing explorations inside the "${category}" layer.`;
    showPage('blogs');
  } else {
    selectedDemoCategoryFilter = category;
    document.getElementById('clearDemoFilterBtn').style.display = 'block';
    document.getElementById('demosBackToTreeBtn').style.display = 'block';
    document.getElementById('demosPageTitle').innerText = `Demos: ${category}`;
    document.getElementById('demosPageSubtitle').innerText = `Showing hardware demonstrations inside the "${category}" layer.`;
    showPage('demos');
  }
}

function clearBlogFilter() {
  selectedCategoryFilter = null;
  document.getElementById('clearFilterBtn').style.display = 'none';
  document.getElementById('blogsBackToTreeBtn').style.display = 'none';
  document.getElementById('blogsPageTitle').innerText = 'Articles & Write-ups';
  document.getElementById('blogsPageSubtitle').innerText = 'Exploring how systems evolve from hardware to intelligence.';
  renderBlogs(1);
}

function clearDemoFilter() {
  selectedDemoCategoryFilter = null;
  document.getElementById('clearDemoFilterBtn').style.display = 'none';
  document.getElementById('demosBackToTreeBtn').style.display = 'none';
  document.getElementById('demosPageTitle').innerText = 'Edge AI Demonstrations';
  document.getElementById('demosPageSubtitle').innerText = 'Deploying neural networks and intelligent decision loops on raw silicon targets.';
  renderDemos(1);
}

function clearBlogFilterAndGoHome() { clearBlogFilter(); showPage('home'); }
function clearDemoFilterAndGoHome() { clearDemoFilter(); showPage('home'); }

function handleSortChange(type) {
  if (type === 'blogs') {
    currentSortOrder = document.getElementById('blogSortOrderSelect').value;
    renderBlogs(1);
  } else {
    currentDemoSortOrder = document.getElementById('demoSortOrderSelect').value;
    renderDemos(1);
  }
}

// ─── BLOG RENDER ENGINE ──────────────────────────────────────────────────────
function renderBlogs(page) {
  page = page || 1; currentBlogPage = page;
  const container = document.getElementById('blogList');
  if (!container) return;

  let processed = blogPosts.slice();
  if (currentSortOrder === "newest") processed.reverse();
  if (selectedCategoryFilter) processed = processed.filter(p => p.category === selectedCategoryFilter);

  if (processed.length === 0) {
    container.innerHTML = `<div style="text-align:center; color:var(--muted); font-family:var(--mono); padding:3rem 0;">// No write-ups found under this category</div>`;
    renderPagination(0, 'blogs');
    return;
  }

  const totalPages = Math.ceil(processed.length / BLOGS_PER_PAGE);
  const slice = processed.slice((page - 1) * BLOGS_PER_PAGE, page * BLOGS_PER_PAGE);

  container.innerHTML = slice.map(post => `
    <div class="blog-card" onclick="openItem('${post.id}', 'blogs')">
      <div class="blog-series">${escHtml(post.series || `Layer: ${post.category}`)}</div>
      <div class="blog-title">${escHtml(post.title)}</div>
      <div class="blog-subtitle">${escHtml(post.subtitle)}</div>
      <div class="blog-meta"><span>${escHtml(post.date)}</span></div>
    </div>
  `).join('');
  renderPagination(totalPages, 'blogs');
}

// ─── DEMO RENDER ENGINE ──────────────────────────────────────────────────────
function renderDemos(page) {
  page = page || 1; currentDemoPage = page;
  const container = document.getElementById('demoList');
  if (!container) return;

  let processed = demoPosts.slice();
  if (currentDemoSortOrder === "newest") processed.reverse();
  if (selectedDemoCategoryFilter) processed = processed.filter(p => p.category === selectedDemoCategoryFilter);

  if (processed.length === 0) {
    container.innerHTML = `<div style="text-align:center; color:var(--muted); font-family:var(--mono); padding:3rem 0;">// No prototype deployments documented under this layer yet</div>`;
    renderPagination(0, 'demos');
    return;
  }

  const totalPages = Math.ceil(processed.length / BLOGS_PER_PAGE);
  const slice = processed.slice((page - 1) * BLOGS_PER_PAGE, page * BLOGS_PER_PAGE);

  container.innerHTML = slice.map(demo => `
    <div class="blog-card" onclick="openItem('${demo.id}', 'demos')">
      <div class="blog-series" style="color:var(--blue);">${escHtml(demo.series)} &middot; Layer: ${escHtml(demo.category)}</div>
      <div class="blog-title">${escHtml(demo.title)}</div>
      <div class="blog-subtitle">${escHtml(demo.subtitle)}</div>
      <div class="blog-meta"><span>${escHtml(demo.date)}</span></div>
    </div>
  `).join('');
  renderPagination(totalPages, 'demos');
}

function renderPagination(totalPages, type) {
  const navId = type === 'blogs' ? 'blogPagination' : 'demoPagination';
  const parentId = type === 'blogs' ? 'blogList' : 'demoList';
  const current = type === 'blogs' ? currentBlogPage : currentDemoPage;
  const triggerFunc = type === 'blogs' ? 'renderBlogs' : 'renderDemos';

  var old = document.getElementById(navId);
  if (old) old.remove();
  if (totalPages <= 1) return;

  var wrap = document.createElement('div');
  navId ? wrap.id = navId : null;
  wrap.style.cssText = 'margin-top:2.5rem;display:flex;align-items:center;justify-content:center;gap:0.5rem;flex-wrap:wrap';

  var parts = [];
  if (current > 1) {
    parts.push(`<button onclick="${triggerFunc}(${current - 1})" style="background:transparent;border:1px solid var(--border);border-radius:6px;color:var(--muted);font-family:var(--mono);font-size:0.75rem;padding:0.4rem 0.85rem;cursor:pointer;">← Prev</button>`);
  }
  for (var i = 1; i <= totalPages; i++) {
    parts.push(`<button onclick="${current === i ? '' : `${triggerFunc}(${i})`}" style="${i === current ? 'background:var(--blue);border:1px solid var(--blue);color:#fff;' : 'background:transparent;border:1px solid var(--border);color:var(--muted);'}border-radius:6px;font-family:var(--mono);font-size:0.75rem;padding:0.4rem 0.75rem;cursor:pointer;">${i}</button>`);
  }
  if (current < totalPages) {
    parts.push(`<button onclick="${triggerFunc}(${current + 1})" style="background:transparent;border:1px solid var(--border);border-radius:6px;color:var(--muted);font-family:var(--mono);font-size:0.75rem;padding:0.4rem 0.85rem;cursor:pointer;">Next →</button>`);
  }

  wrap.innerHTML = parts.join('');
  document.getElementById(parentId).after(wrap);
}

// ─── POST READER ENGINE ──────────────────────────────────────────────────────
function openItem(id, type) {
  const collection = type === 'blogs' ? blogPosts : demoPosts;
  const item = collection.find(p => p.id === id);
  if (!item) return;

  const backBtn = document.getElementById('readerBackBtn');
  if (type === 'blogs') {
    backBtn.innerText = "← Back to Exploration";
    backBtn.setAttribute('onclick', "showPage('blogs')");
  } else {
    backBtn.innerText = "← Back to Demonstration";
    backBtn.setAttribute('onclick', "showPage('demos')");
  }

  let label = item.series || item.category;
  let sectionsHtml = item.sections.map(sec => {
    let blocks = sec.content.map(b => {
      if (b.type === 'p') return `<p style="color:#CBD5E1;line-height:1.85;font-size:0.975rem;margin-bottom:1rem;white-space:pre-line">${escHtml(b.text)}</p>`;
      if (b.type === 'quote') return `<div class="blog-quote">${escHtml(b.text)}</div>`;
      if (b.type === 'code') return `<div class="blog-code" style="color:#A5F3FC;">${escHtml(b.text)}</div>`;
      return '';
    }).join('');
    return `<div style="margin-bottom:2.5rem"><h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.15rem;color:#fff;margin-bottom:1rem">${escHtml(sec.heading)}</h2>${blocks}</div>`;
  }).join('');

  document.getElementById('blog-post-content').innerHTML = `
    <div style="font-family:var(--mono);font-size:0.7rem;color:#64748B;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.6rem">${escHtml(label)}</div>
    <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(1.6rem,3vw,2.4rem);line-height:1.15;letter-spacing:-0.03em;color:#fff;margin-bottom:1rem">${escHtml(item.title)}</h1>
    <p style="color:#64748B;font-size:1rem;line-height:1.75;font-weight:300;margin-bottom:1rem">${escHtml(item.subtitle)}</p>
    <div class="tags" style="margin-bottom:3rem">${item.tags.map(t => `<span class="tag">${escHtml(t)}</span>`).join('')}</div>
    <div style="border-top:1px solid var(--border);margin-bottom:3rem"></div>
    ${sectionsHtml}
    <div style="margin-bottom:2.5rem">
      <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.15rem;color:#fff;margin-bottom:1rem">${escHtml(item.closing.heading)}</h2>
      ${item.closing.paragraphs.map(p => `<p style="color:#CBD5E1;line-height:1.85;font-size:0.975rem;margin-bottom:1rem">${escHtml(p)}</p>`).join('')}
      <div class="blog-quote">${escHtml(item.closing.quote)}</div>
    </div>
  `;
  showPage('blog-post');
}

// ─── JOURNEY ──────────────────────────────────────────────────────────────────
const stepLabels = ["Foundations","Systems","Intelligence","Current Focus"];
function renderJourney() {
  document.getElementById('node-selector').innerHTML = stepLabels.map((label, i) => `
    <button class="node-btn${activeNode === i ? ' active' : ''}" onclick="setNode(${i})">
      <span class="step-num">${String(i+1).padStart(2,'0')}</span>${escHtml(label)}
    </button>
  `).join('');

  const n = nodes[activeNode];
  document.getElementById('node-meta').innerHTML = `
    <span class="node-badge">${escHtml(n.badge)}</span>
    <h3 class="node-heading">${escHtml(n.heading)}</h3>
    <p class="node-desc">${escHtml(n.desc)}</p>
    <div class="node-connector">
      <div class="connector-icon">${n.connector.icon}</div>
      <div class="connector-text"><strong>${escHtml(n.connector.label)}</strong><br>${escHtml(n.connector.text)}</div>
    </div>
  `;

  document.getElementById('node-cards').innerHTML = n.cards.map(c => `
    <div class="info-card">
      <div class="info-card-label">${escHtml(c.label)}</div>
      <div class="info-card-title">${escHtml(c.title)}</div>
      <div class="info-card-text">${escHtml(c.text)}</div>
      ${c.tags.length ? `<div class="tags">${c.tags.map(t => `<span class="tag">${escHtml(t)}</span>`).join('')}</div>` : ''}
    </div>
  `).join('');
}

function setNode(i) { activeNode = i; renderJourney(); }
function escHtml(str) { return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

// ─── INIT ─────────────────────────────────────────────────────────────────────
renderBlogs(1);
renderDemos(1);

// ─── FEEDBACK FORM HANDLER ───────────────────────────────────────────────────
const feedbackForm = document.getElementById("feedback-form");
if (feedbackForm) {
  feedbackForm.addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission stalling page routing
    
    const textarea = document.getElementById("feedback-textarea");
    if (!textarea) return;
    
    const text = textarea.value;
    if (!text.trim()) return;
    
    // Normalize all line breaks to \r\n for maximum mail client compatibility
    const formattedText = text.replace(/\r?\n/g, "\r\n");
    
    // Sanitize the text cleanly
    const sanitizedText = encodeURIComponent(formattedText);
    
    // Explicitly trigger the mailto redirect
    window.location.href = "mailto:meesarapud@gmail.com?subject=prajnaedge%20feedback&body=" + sanitizedText;
  });
}
