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

const systemsTreeNodes = {
  Matter: {
    title: "Matter",
    description: "How physical matter became controllable computation.",
    explorations: [
      { id: "chemistry-intelligence-part1", title: "Why Silicon?" },
      { id: "chemistry-intelligence-part2", title: "From Sand to Crystal" },
      { id: "chemistry-intelligence-part3", title: "The Architecture of the Wafer" },
      { id: "chemistry-intelligence-part4", title: "The Birth of the Transistor" },
      { id: "chemistry-intelligence-part5", title: "The First Processor" }
    ]
  },
  Computation: {
    title: "Computation",
    description: "The hidden abstractions that make software appear independent from physics.",
    explorations: [
      { id: "illusion-of-software", title: "The Illusion of Software" },
      { id: "the-architecture-of-memory", title: "The Architecture of Memory" },
      { id: "the-hidden-geography-of-firmware", title: "The Hidden Geography of Firmware" },
      { id: "the-first-instruction", title: "The First Instruction" },
      { id: null, title: "Coming Soon" }
    ]
  },
  Interaction: {
    title: "Interaction",
    description: "The moment software crossed into physical consequence.",
    explorations: [
      { id: "why-systems-need-interfaces", title: "Why Systems Need Interfaces" },
      { id: "the-physical-edge-of-software", title: "The Physical Edge of Software" },
      { id: "why-embedded-systems-speak-in-protocols", title: "Why Embedded Systems Speak in Protocols" },
      { id: "uart-structured-asynchronous-communication", title: "UART: Structured Asynchronous Communication" },
      { id: null, title: "Coming Soon" }
    ]
  },
  Coordination: {
    title: "Coordination",
    description: "Why isolated computation evolved into synchronized systems.",
    explorations: [
      { id: null, title: "Coming Soon" }
    ]
  },
  Intelligence: {
    title: "Intelligence",
    description: "How systems evolved from deterministic control into adaptive intelligence.",
    explorations: [
      { id: null, title: "Coming Soon" }
    ]
  }
};

// EXPLORATION STORAGE (DYNAMIC CONTENT)
const blogPosts = [
  {
  id:"chemistry-intelligence-part1",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:1,
  title:"Why Silicon?",
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
  footer:"Reflections on chemistry and computation - PrajnaEdge.dev"
},
  {
  id:"chemistry-intelligence-part2",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:2,
  title:"From Sand to Crystal",
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
  footer:"Reflections on chemistry and computation - PrajnaEdge.dev"
},
  {
  id:"chemistry-intelligence-part3",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:3,
  title:"The Architecture of the Wafer",
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
  footer:"Reflections on chemistry and computation - PrajnaEdge.dev"
},
{
  id:"chemistry-intelligence-part4",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:4,
  title:"The Birth of the Transistor",
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
  footer:"Reflections on chemistry and computation - PrajnaEdge.dev"
},
  {
  id:"chemistry-intelligence-part5",
  category:"Matter",
  series:"The Chemistry of Intelligence",
  part:5,
  title:"The First Processor",
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
  footer:"Reflections on chemistry and computation - PrajnaEdge.dev"
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
},
{
  id: "the-architecture-of-memory",
  category:"Computation",
  series:"System Explorations",
  title: "The Architecture of Memory",
  subtitle: "How physical constraints and electrical charge define the boundaries of digital state.",
  date: "28th May, 2026",
  tags: ["Memory", "SRAM", "DRAM", "Flash", "Embedded Systems"],
  sections: [
    {
      heading: "1. The Hierarchy of State",
      content: [
        {
          type: "p",
          text: "Every processor is fundamentally a state machine. It executes instructions by reading data from memory, transforming it, and writing it back. But not all memory is created equal. The physical reality of silicon forces a compromise between speed, capacity, and cost."
        },
        {
          type: "p",
          text: "To build a useful system, we construct a hierarchy: registers and SRAM at the very top (tapering down near the CPU core for speed), backed by main DRAM system memory, and finally persistent NOR and NAND flash for mass storage. This tiered architecture ensures the CPU is never starved of instructions while keeping persistent data accessible."
        },
        {
          type: "image",
          src: "Images/memory_hierarchy.png",
          alt: "The Memory Hierarchy showing speed vs density trade-offs",
          caption: "A vertical structural view of memory layers tapering down as they approach the CPU core."
        }
      ]
    },
    {
      heading: "2. The Battle for the Bit: SRAM vs DRAM",
      content: [
        {
          type: "p",
          text: "At the volatile layer, the choice comes down to topology: how do we store a single bit of data?"
        },
        {
          type: "p",
          text: "Static RAM (SRAM) uses a cross-coupled latch constructed with 6 transistors (6T). This design creates an active, stable state that holds its value as long as power is applied. However, this complexity makes SRAM physically large and expensive, limiting its use to small, fast CPU caches and microcontroller registers."
        },
        {
          type: "p",
          text: "Dynamic RAM (DRAM) takes the opposite approach. It shrinks the cell down to a single transistor and a single storage capacitor (1T1C). While this allows massive densities (gigabytes on a single chip), the capacitor is a leaky reservoir. It naturally drains its charge within milliseconds, requiring a continuous refresh loop to prevent data corruption."
        },
        {
          type: "image",
          src: "Images/sram_vs_dram.png",
          alt: "SRAM 6T vs DRAM 1T1C circuit diagram",
          caption: "Circuit topologies representing the active stable latch of SRAM versus the leaky reservoir of DRAM."
        }
      ]
    },
    {
      heading: "3. Persistence: NOR vs NAND Flash",
      content: [
        {
          type: "p",
          text: "When power is removed, we rely on non-volatile flash memory to retain our programs and data. Flash operates by trapping charge within a floating gate transistor. The layout configuration of these gates determines how they can be accessed."
        },
        {
          type: "p",
          text: "NOR Flash connects storage transistors in parallel directly across word lines. This parallel alignment allows the processor to perform instant random byte reads, making it the standard choice for executing firmware binary code directly on-board."
        },
        {
          type: "p",
          text: "NAND Flash daisy-chains transistor arrays in a tight serial configuration. By eliminating the individual contacts needed for parallel routing, NAND achieves extraordinary densities. However, this serial chain prevents byte-level access, requiring the processor to read and write data in sequential sector blocks, ideal for mass storage filesystems."
        },
        {
          type: "image",
          src: "Images/nor_vs_nand.png",
          alt: "NOR parallel vs NAND serial micro-architectural layouts",
          caption: "Transistor cell layout detailing parallel random-access lines in NOR vs serial block lines in NAND."
        }
      ]
    },
    {
      heading: "4. The Address Map: Dividing Space",
      content: [
        {
          type: "p",
          text: "To the developer, all of these physical layers are abstracted into a single, contiguous address space. The microcontroller registers map specific memory regions to Flash and SRAM boundaries."
        },
        {
          type: "p",
          text: "From top to bottom, the register space is divided into proportional segments: .text (NOR Flash for execution), .data and .bss (RAM for initialized and zeroed variables), followed by the Stack (runtime context engine) and the Heap (dynamic allocation workspace)."
        },
        {
          type: "image",
          src: "Images/embedded_memory_map.png",
          alt: "Microcontroller memory map segment boundaries",
          caption: "The vertical register allocation of persistent Flash versus internal SRAM workspace segments."
        }
      ]
    }
  ],
  closing: {
    heading: "The Architecture of State",
    paragraphs: [
      "Memory is not just a passive buffer; it is the physical medium where logic meets reality. The boundaries of digital state are defined by the speeds, densities, and physical layout structures of silicon.",
      "Understanding these hardware constraints is what allows us to write firmware that pushes performance to the very edge."
    ],
    quote: "True efficiency is achieved when you align your software execution path with the physical layout of the silicon."
  },
  footer: "Reflections on Memory and State - PrajnaEdge.dev"
},
{
  id: "the-hidden-geography-of-firmware",
  category: "Computation",
  series: "System Explorations",
  title: "The Hidden Geography of Firmware",
  subtitle: "How linker scripts quietly decide where computation lives.",
  date: "4th June, 2026",
  tags: ["Linker Scripts", "Memory Mapping", "Firmware", "Systems Architecture"],
  sections: [
    {
      heading: "1. The Illusion of Uniform Memory",
      content: [
        {
          type: "p",
          text: "To a programmer working in a high-level application space, memory is often visualized as a flat, infinite landscape of bytes—a continuous array indexed from zero to the limits of physical RAM. You allocate memory, declare variables, and write functions under the assumption that all space is structurally equivalent."
        },
        {
          type: "p",
          text: "But beneath the abstraction layers of low-level firmware, this uniformity disappears. Memory is not a single contiguous pasture; it is a highly structured, compartmentalized terrain. A microcontroller's memory space is fragmented by physical and electrical realities. Code, initialized global variables, uninitialized flags, read-only constants, stack frames, and dynamic heaps must reside in completely different areas of the silicon to function."
        },
        {
          type: "image",
          src: "Images/firmware_memory_layout.png",
          alt: "Embedded Firmware Memory Layout Diagram",
          caption: "Firmware is not stored as one object. It is distributed across memory according to behavioral requirements."
        }
      ]
    },
    {
      heading: "2. The Birth of Memory Sections",
      content: [
        {
          type: "p",
          text: "Why do we slice firmware into segments? It is a direct response to different behavioral requirements. Different classes of information behave differently during execution, requiring distinct storage mediums."
        },
        {
          type: "p",
          text: "Consider instructions: executable code must be persistent and read-only, which is why the compiler assigns it to the '.text' section to reside in Flash memory. Constants and string literals share similar read-only behaviors and are grouped into the '.rodata' section, protected from runtime modification."
        },
        {
          type: "p",
          text: "Global variables, however, present a dual behavior. They must be modifiable at runtime (residing in RAM), but they must start with a pre-configured initial value. These are grouped into '.data'. Uninitialized global variables—those that simply need to be cleared to zero on startup—are routed to '.bss' (Block Started by Symbol) to save space in the flash binary."
        },
        {
          type: "p",
          text: "Finally, the Stack handles execution flow by dynamically pushing and popping function parameters and local variables, while the Heap manages runtime dynamic memory allocation workspace. The organization of these sections is the layout of digital life."
        }
      ]
    },
    {
      heading: "3. The Linker as a Cartographer",
      content: [
        {
          type: "p",
          text: "During compilation, the compiler translates individual source files (.c or .cpp) into independent object files (.o). At this stage, the compiler acts in isolation: it has no knowledge of how much total Flash or RAM exists on the chip, nor does it know where other object files will eventually be placed."
        },
        {
          type: "p",
          text: "This is where the Linker enters as a cartographer. The linker compiles these fragmented objects and maps their sections into a unified, physical landscape. It decides the precise layout of the firmware—stitching together the various '.text', '.data', and '.bss' fragments and matching them to the exact address boundaries of the target processor."
        },
        {
          type: "image",
          src: "Images/linker_to_memory_relationship.png",
          alt: "Linker to Memory Relationship Mapping",
          caption: "The compiler generates isolated segments; the linker script guides the linker to map them into physical memory blocks."
        },
        {
          type: "quote",
          text: "The linker does not create firmware. It decides where firmware physically exists."
        }
      ]
    },
    {
      heading: "4. The Linker Script",
      content: [
        {
          type: "p",
          text: "To direct the linker, we use a linker script—a blueprint that defines the physical boundaries of the MCU's address register space. It tells the linker exactly where Flash and RAM begin and how long they are."
        },
        {
          type: "code",
          text: "MEMORY\n{\n  FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 512K\n  RAM (rwx)  : ORIGIN = 0x20000000, LENGTH = 128K\n}"
        },
        {
          type: "p",
          text: "In this snippet, we define the region boundaries. 'FLASH' is marked as read-only and executable (rx) starting at origin address 0x08000000 with a length of 512 Kilobytes. 'RAM' is marked as readable, writable, and executable (rwx) starting at origin 0x20000000 with 128 Kilobytes."
        },
        {
          type: "p",
          text: "By establishing these constraints, the compiler can output absolute addresses, knowing that the code and variable segments will fall safely within the silicon boundaries."
        },
        {
          type: "image",
          src: "Images/mcu_memory_map.png",
          alt: "Microcontroller Memory Map Diagram",
          caption: "Microcontroller address registers are mapped to specific Flash (executable) and RAM (read-write) regions."
        }
      ]
    },
    {
      heading: "5. Startup: The First Migration",
      content: [
        {
          type: "p",
          text: "When power is applied, the microcontroller is in a primitive state. The RAM is filled with random electrical noise. However, global variables in the '.data' section must have their initial non-zero values ready for the application to read."
        },
        {
          type: "p",
          text: "Since RAM is volatile and loses all state when powered off, these initial values must be stored persistently inside Flash memory. This creates a logical conflict: the variables must be modifiable in RAM during execution, but their initial values are trapped in Flash."
        },
        {
          type: "p",
          text: "To resolve this, the system executes startup assembly or C initialization routines before your main() function is reached. This startup code performs the first migration: it reads the block of initial values from Flash and copies them into their RAM destinations. It then clears the '.bss' section in RAM to zero."
        },
        {
          type: "image",
          src: "Images/startup_initialization_flow.png",
          alt: "Startup Initialization Flow Diagram",
          caption: "Relocation sequence at startup, moving initialized variables from Flash to RAM and zeroing out the BSS."
        },
        {
          type: "quote",
          text: "Before the first line of user code executes, the system has already performed a carefully orchestrated relocation."
        }
      ]
    },
    {
      heading: "6. The Map File: The Firmware Census",
      content: [
        {
          type: "p",
          text: "Once the linker has completed its map, it outputs a map file—a census of the compiled firmware. The map file outlines exactly where every function, variable, and library symbol has been placed, along with the size of each segment."
        },
        {
          type: "p",
          text: "Experienced embedded engineers inspect map files regularly. When a firmware image suddenly overflows memory, the map file reveals which module or library is consuming the flash. It lets you identify compiler optimizations, alignment padding issues, and variables that were accidentally declared globally instead of locally."
        },
        {
          type: "code",
          text: ".text           0x08000240      0x8a4\n *(.text)\n .text          0x08000240      0x1c8 build/main.o\n                0x080002a0                SystemInit\n .text          0x08000408      0x6dc build/gpio.o\n                0x08000420                GPIO_Init\n\n.data           0x20000000       0x18 load address 0x08000ae4\n *(.data)\n .data          0x20000000       0x18 build/main.o\n                0x20000004                system_state\n\n.bss            0x20000018       0x40\n *(.bss)\n .bss           0x20000018       0x40 build/sensor.o\n                0x20000018                sensor_buffer"
        }
      ]
    },
    {
      heading: "7. When Geography Becomes Critical",
      content: [
        {
          type: "p",
          text: "Memory mapping eventually moves from a compiler detail to a system design challenge. In advanced architectures, you must place DMA (Direct Memory Access) buffers into specific memory regions that the DMA controller can actually access. If the buffer is mapped to a core-coupled RAM region that is inaccessible to the peripheral bus, the system will silently fail or crash."
        },
        {
          type: "p",
          text: "Similarly, separating a bootloader from an application requires carving Flash memory into separate, non-overlapping regions using custom linker scripts. The developer is no longer writing software alone—they are shaping the physical layout of logic."
        }
      ]
    }
  ],
  closing: {
    heading: "Shaping the City of Logic",
    paragraphs: [
      "Memory architecture defines the boundaries of what is electrically possible, but the linker script defines the geography where firmware actually lives.",
      "As you write embedded code, you are not just writing logic; you are organizing silicon."
    ],
    quote: "Every firmware image is a city. The linker simply decides where its citizens reside."
  },
  footer: "Exploring the hidden structures of firmware systems - PrajnaEdge.dev"
},
{
  id: "the-first-instruction",
  category: "Computation",
  series: "System Explorations",
  title: "The First Instruction",
  subtitle: "The hidden journey from power-on to main().",
  date: "7th June, 2026",
  tags: ["Firmware", "Hardware", "Bootloader", "Systems Architecture"],
  sections: [
    {
      heading: "1. The Myth of main()",
      content: [
        {
          type: "p",
          text: "To the software engineer working with high-level languages, the universe begins with a simple declaration: int main(). It is the clean boundary where our code begins to run, the genesis of application state, and the first frame in our debugger. We write code under the comforting assumption that before main(), the processor is a blank canvas, waiting for our instructions to bring it to life."
        },
        {
          type: "p",
          text: "But this is a convenient abstraction. In low-level systems, main() is not the beginning of the program; it is one of the final stages of a highly structured initialization sequence. Before the CPU ever executes the first instruction of your application, a complex choreography of physical and logical transitions must occur. Memory must be initialized, clock sources must stabilize, interrupt lines must be routed, and the execution environment must be built out of raw silicon."
        },
        {
          type: "p",
          text: "If firmware already exists inside non-volatile memory, how does it actually come alive? How does a block of inanimate code become a dynamic, executing system? To answer this, we must look before the beginning."
        },
        {
          type: "quote",
          text: "main() is not the beginning of firmware. It is the point at which the system finally hands control to the developer."
        }
      ]
    },
    {
      heading: "2. Power-On: The Silent Beginning",
      content: [
        {
          type: "p",
          text: "Before computation can occur, the physical environment must stabilize. When power is first applied to a microcontroller, the system undergoes an analog transition. The power rails do not instantly reach their nominal operating voltages; they climb along a capacitive ramp governed by the power supply circuitry."
        },
        {
          type: "p",
          text: "During this brief startup ramp, the voltage levels are insufficient to toggle digital logic gates predictably. If the CPU began fetching instructions immediately, it would read corrupted bytes, registers would settle into random states, and the system would crash. To prevent this, microcontrollers incorporate specialized supervisor circuitry—typically a hardware Reset circuit paired with Brownout Detection (BOD)."
        },
        {
          type: "p",
          text: "The Brownout Detection circuit acts as an analog sentinel. It holds the CPU's internal reset line low, forcing all digital registers and execution pipelines into safe, defined hardware default states. While the reset line is active, the system's main crystal oscillator is powered up. The oscillator requires time to stabilize, moving from thermal noise to a steady, rhythmic sine wave."
        },
        {
          type: "image",
          src: "Images/power_on_sequence.png",
          alt: "Power-On Sequence",
          caption: "The progression from raw electrical power application to voltage stabilization, reset release, and the birth of instruction execution."
        },
        {
          type: "p",
          text: "Once the power supervisor detects that the supply voltage has crossed a safe threshold and remains stable, and the oscillator has settled into a steady rhythm, the hardware reset signal is finally released. Only now, with stable power and a reliable clock pulse, can the processor take its first digital step."
        }
      ]
    },
    {
      heading: "3. The Reset Vector",
      content: [
        {
          type: "p",
          text: "When the reset line is released, the CPU's program counter does not start at a random location, nor does it scan the memory looking for code. Instead, the hardware is wired to look at a single, hardcoded address in the memory map: the Reset Vector."
        },
        {
          type: "p",
          text: "This fixed startup address is a contract between the silicon designer and the systems architect. On 8-bit AVR microcontrollers, the reset vector is typically address 0x0000, where a jump instruction to the startup routine is placed. On 32-bit ARM Cortex-M processors, the CPU looks at address 0x00000000 to read the initial Stack Pointer, and then loads the address of the Reset Handler from 0x00000004 into the program counter."
        },
        {
          type: "p",
          text: "Regardless of the specific architecture, the mechanism remains conceptual: the hardware reset release forces the CPU to load its very first instruction address from a dedicated slot. The reset vector is the gateway; it points the processor directly to the code that will build the software runtime."
        },
        {
          type: "image",
          src: "Images/reset_vector_flow.png",
          alt: "Reset Vector Flow",
          caption: "The deterministic path from physical reset release to loading the Reset Handler address from the vector table."
        }
      ]
    },
    {
      heading: "4. The Vector Table",
      content: [
        {
          type: "p",
          text: "Before a processor can execute complex software, it must know how to handle exceptions, faults, and interrupts. This mapping is defined by the Vector Table—the system's primary layout of execution targets."
        },
        {
          type: "p",
          text: "The vector table is a sequential array of memory addresses located at the base of the executable address space (or relocated via a vector table offset register). Its entries do not contain instructions; they contain pointers to functions. The first few slots are reserved for critical system conditions: the initial Stack Pointer (so the CPU has a memory context for registers), the Reset Handler (where initialization code lives), the Non-Maskable Interrupt (NMI), and the HardFault handler."
        },
        {
          type: "p",
          text: "Without this table, the CPU is blind to its own failures. If a memory access fault or illegal instruction occurs during early startup, the processor must instantly jump to a fault handler to prevent runaway execution. The vector table provides this safety net before any user code can run."
        },
        {
          type: "image",
          src: "Images/cortex_m_vector_table.png",
          alt: "Cortex-M Vector Table",
          caption: "The layout of the vector table, mapping system exceptions and hardware faults to their handler addresses."
        }
      ]
    },
    {
      heading: "5. The Startup Code",
      content: [
        {
          type: "p",
          text: "Having loaded the address of the Reset Handler, the CPU begins executing the startup code—typically written in assembly or highly optimized bare-metal C. The primary objective of this phase is memory migration, bridging the gap between persistent storage and volatile workspace."
        },
        {
          type: "p",
          text: "As explored in 'The Hidden Geography of Firmware', global and static variables are split into different sections. At boot, RAM contains nothing but volatile electrical noise. However, global variables in the '.data' section must start with their defined, non-zero values. Since RAM cannot hold this state across power cycles, these initial values are stored in Flash."
        },
        {
          type: "p",
          text: "The startup code performs a literal copy loop: it reads the initialization values from Flash and writes them to their corresponding RAM addresses. Next, it zeros out the '.bss' section in RAM, ensuring all uninitialized global variables are clean. Only when this migration is complete is the system's memory model aligned with the developer's expectations."
        },
        {
          type: "image",
          src: "Images/startup_memory_initialization.png",
          alt: "Startup Memory Initialization",
          caption: "The startup copy routine migrating initialized data from persistent Flash to volatile RAM and zeroing out the BSS segment."
        }
      ]
    },
    {
      heading: "6. The Clock Awakens",
      content: [
        {
          type: "p",
          text: "At boot, the microcontroller operates on a slow, low-power internal RC oscillator. This default clock source requires no external components and starts up instantly, but it lacks the precision and speed needed for high-performance computation or high-speed communication."
        },
        {
          type: "p",
          text: "Once memory is initialized, the system must establish its operational rhythm. The startup code configures the clock tree: it enables the external crystal oscillator (which takes several milliseconds to stabilize), waits for it to lock, and then engages the Phase-Locked Loop (PLL) circuits to multiply the base frequency up to the system's target operating speed."
        },
        {
          type: "p",
          text: "This transition requires care. The flash memory access latency (wait states) must be adjusted to match the new speed; otherwise, the CPU would fetch instructions faster than the Flash could supply them, causing a system crash. Once the clock tree is stable, the system switches its core clock source to the PLL output, and the processor begins running at full speed."
        },
        {
          type: "quote",
          text: "A processor without a clock is a mind without rhythm."
        },
        {
          type: "image",
          src: "Images/clock_startup_chain.png",
          alt: "Clock Startup Chain",
          caption: "The clock propagation path from the base oscillator through frequency multiplication to core system clock distribution."
        }
      ]
    },
    {
      heading: "7. Bootloaders: The Gatekeepers",
      content: [
        {
          type: "p",
          text: "In simple microcontrollers, the reset vector points directly to the startup code of the main application. But in modern, production-grade systems, execution rarely jumps straight to user code. Instead, the CPU passes through one or more bootloaders."
        },
        {
          type: "p",
          text: "A ROM bootloader—sometimes called a primary bootloader—is burned into the processor's silicon during manufacturing. It is immutable. At boot, it executes first, checking GPIO pins or memory flags to decide if it should enter a firmware update mode (pulling new code over UART, USB, or CAN) or hand off control to a secondary bootloader."
        },
        {
          type: "p",
          text: "The secondary bootloader lives in flash memory and provides custom system logic. It might manage dual-image bank switching for safe OTA updates, initialize external RAM, or verify the integrity of the application firmware before jumping to its entry point."
        },
        {
          type: "image",
          src: "Images/bootloader_hierarchy.png",
          alt: "Bootloader Hierarchy",
          caption: "The execution flow passing through ROM and custom bootloader stages before reaching application firmware."
        },
        {
          type: "p",
          text: "By separating the boot process into layers, the system gains robustness. If the main application becomes corrupted during a flash write, the bootloader remains intact, providing a recovery path that prevents the device from becoming permanently unresponsive."
        }
      ]
    },
    {
      heading: "8. Secure Boot and Trust",
      content: [
        {
          type: "p",
          text: "In an interconnected world, the boot process is not just about functionality; it is about security. Secure Boot establishes a chain of trust that guarantees only authentic, unmodified code can run on the hardware."
        },
        {
          type: "p",
          text: "This chain begins with a Root of Trust—typically a public key hashed into read-only memory or one-time programmable (OTP) fuses inside the CPU during manufacturing. The immutable ROM bootloader uses this key to cryptographically verify the signature of the next boot stage. If the signature matches and the code is verified, the ROM bootloader executes it."
        },
        {
          type: "p",
          text: "This verified stage then repeats the process for the next layer, validating the application firmware binary before handing over control. If any link in this chain fails—due to a corrupted download, a tampering attempt, or an unauthorized firmware image—the boot process halts immediately."
        },
        {
          type: "quote",
          text: "Modern systems no longer ask only whether firmware exists. They ask whether it deserves to execute."
        },
        {
          type: "image",
          src: "Images/secure_boot_chain_of_trust.png",
          alt: "Secure Boot Chain of Trust",
          caption: "The sequential validation of signatures from the hardware Root of Trust down to the application layer."
        }
      ]
    },
    {
      heading: "9. The Handoff",
      content: [
        {
          type: "p",
          text: "After passing through electrical stabilization, vector loading, memory relocation, clock configuration, bootloader checks, and cryptographic verification, the system is finally ready. The runtime environment is fully realized."
        },
        {
          type: "p",
          text: "The processor is running at its full frequency. Volatile memory is partitioned and initialized. The stack is clean, the heap is ready, and the interrupt system is armed. The startup routine performs the final handoff: it loads the address of the main() function into the program counter register."
        },
        {
          type: "p",
          text: "At this exact moment, control shifts. The invisible machinery that brought the machine from inert silicon to an executing system recedes into the background. The first line of your main() function executes."
        },
        {
          type: "image",
          src: "Images/complete_boot_process_overview.png",
          alt: "Complete Boot Process Overview",
          caption: "The entire architectural sequence from physical power-on to main() execution."
        }
      ]
    }
  ],
  closing: {
    heading: "The Invisible Journey",
    paragraphs: [
      "Every firmware project hides an invisible journey. Before a single application instruction executes, an entire chain of hardware, memory, startup logic, and trust decisions has already occurred.",
      "The developer sees main(). The system experiences a much longer story."
    ],
    quote: "The first instruction is rarely the one written by the developer. It is the one that teaches the machine how to become itself."
  },
  footer: "Exploring the hidden journeys of firmware systems - PrajnaEdge.dev"
},
{
  id: "why-embedded-systems-speak-in-protocols",
  category: "Interaction",
  series: "System Explorations",
  title: "Why Embedded Systems Speak in Protocols",
  subtitle: "Why simple electrical signals evolved into structured conversations.",
  date: "12th June, 2026",
  tags: ["Protocols", "Communication", "SPI", "I2C", "UART", "Embedded Systems"],
  sections: [
    {
      heading: "1. The Limit of Direct Connection",
      content: [
        {
          type: "p",
          text: "In the early stages of computing design, the challenge is simply getting a CPU to change a physical state. We write a value to a register, voltage appears on a copper pin, and an LED illuminates. This General Purpose Input/Output (GPIO) is the simplest boundary crossing between logic and physical consequence."
        },
        {
          type: "p",
          text: "But systems do not exist in isolation. A microcontroller must talk to sensors, memory modules, display controllers, and other processors. If we try to scale GPIO to handle this, we quickly run into a physical wall."
        },
        {
          type: "p",
          text: "To send a single 8-bit integer, we could use eight separate GPIO pins connected by eight physical wires. This parallel approach works, but it consumes valuable pins and turns the PCB routing layout into a dense maze of copper. If we instead use a single wire to send those 8 bits sequentially, we face a new problem: timing. How does the receiver know when to sample the wire? How does it distinguish a string of consecutive '1' bits from a single long '1' bit?"
        },
        {
          type: "quote",
          text: "Without a shared definition of structure, raw electrical signals are indistinguishable from noise."
        }
      ]
    },
    {
      heading: "2. Communication as Shared Agreement",
      content: [
        {
          type: "p",
          text: "Communication requires more than simply pushing electrons down a copper lead. It requires a shared agreement—a protocol. A protocol transitions communication from raw physics to structured grammar."
        },
        {
          type: "p",
          text: "Every communication protocol establishes three critical boundaries:"
        },
        {
          type: "p",
          text: "1. The Physical Layer: Agreeing on voltage levels. What voltage represents a digital '1' and what represents a '0'? Are we using single-ended voltages or differential signals?\n\n2. The Timing: Agreeing on speed. How long does a single bit of information last?\n\n3. The Framing: Agreeing on structure. How does a transmitter signal that a new message is starting? How does the receiver know when the message has ended, and how does it detect if data was corrupted?"
        },
        {
          type: "p",
          text: "By establishing these rules, we can pack dense information onto a minimal number of physical lines."
        }
      ]
    },
    {
      heading: "3. Serial vs. Parallel: The Routing Dilemma",
      content: [
        {
          type: "p",
          text: "Intuitively, parallel communication seems superior because it transmits multiple bits at the same instant. Early computers relied heavily on parallel buses for printers (LPT ports), hard drives (IDE cables), and internal bus architectures."
        },
        {
          type: "p",
          text: "However, as timing speeds increased, parallel communication encountered fundamental physical limits:"
        },
        {
          type: "p",
          text: "Skew: Because copper traces on a PCB have slightly different physical lengths and capacitive characteristics, bits traveling in parallel arrive at the destination at slightly different times. At high frequencies, this skew corrupts the data.\n\nCrosstalk: Parallel lines running close to each other generate electromagnetic fields that induce noise on neighboring lines.\n\nPCB Complexity: Routing dozens of high-speed parallel traces requires multi-layer boards and tight spacing constraints, increasing manufacturing costs."
        },
        {
          type: "p",
          text: "Serial communication solves this by sending bits sequentially over a minimal physical path (often just one or two lines). By focusing on timing alignment on a single line, modern systems can achieve transfer rates orders of magnitude faster than historical parallel buses, using far less physical space."
        },
        {
          type: "image",
          src: "Images/protocols_vs_gpio_schematic.png",
          alt: "GPIO Direct vs Protocol Structured Signaling",
          caption: "The transition from direct, unstructured GPIO toggling to a structured protocol frame containing synchronization and data payload boundaries."
        }
      ]
    },
    {
      heading: "4. Direction of Flow: Simplex to Full Duplex",
      content: [
        {
          type: "p",
          text: "Once we move to serial lines, we must decide how devices share the channel to transmit and receive data. This flow is categorized into three modes:"
        },
        {
          type: "p",
          text: "Simplex: One-way communication. A transmitter sends data continuously, and a receiver only listens. There is no feedback loop. This is typical in simple broadcast sensors or debug logs.\n\nHalf Duplex: Two-way communication, but only one device can transmit at any given instant. Devices must share the physical line, requiring addressing or turn-taking logic to avoid collisions. I2C and RS-485 are classic examples.\n\nFull Duplex: Simultaneous, bidirectional communication. This is typically achieved by running separate physical lines for transmit (TX) and receive (RX), allowing both devices to speak and listen at the same time without interference. UART and SPI operate in this mode."
        }
      ]
    },
    {
      heading: "5. The Synchronization Boundary",
      content: [
        {
          type: "p",
          text: "The most critical task of any protocol is synchronization—ensuring the receiver samples the wire at the exact moment a bit is stable. This divides serial protocols into two main philosophies:"
        },
        {
          type: "p",
          text: "Synchronous Communication: The transmitter provides a physical clock signal along a dedicated line (e.g., SPI and I2C). The receiver monitors this clock line and samples the data line on the rising or falling clock edge. This is highly reliable and supports variable speeds, but requires an extra physical line."
        },
        {
          type: "p",
          text: "Asynchronous Communication: No clock signal is transmitted (e.g., UART). Instead, both transmitter and receiver must be configured to use the exact same bit speed (baud rate) beforehand. The receiver detects the start of a transmission by watching for a specific voltage change (the Start Bit) and then uses its local clock to count out intervals and sample the subsequent bits."
        },
        {
          type: "quote",
          text: "Synchronous protocols share a clock line to guarantee timing. Asynchronous protocols agree on timing beforehand to save a wire."
        }
      ]
    },
    {
      heading: "6. From Signals to Conversations",
      content: [
        {
          type: "p",
          text: "Communication protocols are the grammar of systems. They move us past raw physical toggling into organized logical networks where processors, sensors, and displays negotiate control, exchange status, and build coordinated behavior."
        },
        {
          type: "p",
          text: "As we explore the interaction layer of the systems tree, we will trace the evolution of these agreements:"
        },
        {
          type: "p",
          text: "UART: The simple, asynchronous point-to-point interface.\n\nSPI: The high-speed, synchronous, register-to-register bus.\n\nI2C: The multi-drop, addressed, two-wire shared conversation.\n\nCAN: The robust, differential, priority-arbitrated network designed for extreme noise environments."
        },
        {
          type: "p",
          text: "Every protocol is a distinct set of engineering compromises, balancing speed, pin count, distance, and reliability to solve a specific coordination challenge."
        }
      ]
    }
  ],
  closing: {
    heading: "The Language of Silicon",
    paragraphs: [
      "A processor speaking in isolation is only executing calculations. When it learns to follow structured protocols, it joins a larger network of interaction.",
      "The choice of protocol defines the parameters of that conversation."
    ],
    quote: "Protocols are not just communication mechanisms; they are the architectural agreements that make distributed systems possible."
  },
  footer: "Reflections on systems communication - PrajnaEdge.dev"
},
{
  id: "uart-structured-asynchronous-communication",
  category: "Interaction",
  series: "System Explorations",
  title: "UART: Structured Asynchronous Communication",
  subtitle: "How two independent systems learned to agree on time.",
  date: "13th June, 2026",
  tags: ["UART", "Serial Protocols", "Asynchronous", "Baud Rate", "Embedded Systems"],
  sections: [
    {
      heading: "1. From Raw Voltage to Structured Language",
      content: [
        {
          type: "p",
          text: "At its absolute physical foundation, a General Purpose Input/Output (GPIO) line is a simple copper trace holding a voltage. It can be pulled high, or it can be driven low. In isolation, a voltage transition is a binary event—a simple statement that something has changed. But if two independent processors are to exchange thoughts, a raw voltage transition is not enough. Without structure, a change in state is indistinguishable from electrical noise, and there is no way to represent a sequence of letters, numbers, or commands."
        },
        {
          type: "p",
          text: "Universal Asynchronous Receiver-Transmitter (UART) is the architectural answer to this limitation. It is the bridge that transforms a simple, volatile voltage line into a channel for structured information. It does this not by adding more wires or introducing a complex shared clock, but by establishing a strict contract: an agreement on how time and voltage translate into a digital language."
        },
        {
          type: "p",
          text: "By eliminating the physical clock line, UART minimizes physical pin count to a bare minimum: Transmit (TX), Receive (RX), and a shared Ground reference. But this simplicity at the physical layer moves the engineering burden entirely into the domain of timing agreements. The devices must agree on a set of rules—a communication contract—that allows them to reconstruct structured data from the transient rise and fall of voltages."
        }
      ]
    },
    {
      heading: "2. Anatomy of the UART Frame",
      content: [
        {
          type: "p",
          text: "To transmit structured data asynchronous to any clock, UART packages bits into small, predictable containers called Frames. Each frame is a sequential series of voltage levels representing synchronization markers, the payload, and validation data. Understanding the frame is to understand the engineering motivation behind each transition:"
        },
        {
          type: "p",
          text: "• Idle State: When no data is being sent, the line remains at a constant High voltage level (logical 1). Keeping the line high serves two purposes: it makes the link noise-resistant during quiet periods, and it ensures that a transition to Low is instantly detectable as a deliberate communication event rather than passive interference."
        },
        {
          type: "p",
          text: "• Start Bit: The transmission starts with a sharp, forced transition from High to Low (logical 0) for exactly one bit period. This falling edge is the receiver's alarm clock. The moment it occurs, the receiver's hardware wakes up, resets its internal timing counters, and aligns its sampling logic to the start of the payload."
        },
        {
          type: "p",
          text: "• Data Bits: Following the start bit, the payload—typically 8 bits—is serialized and driven onto the line, Least Significant Bit (LSB) first. Sending LSB first simplifies the design of shift registers in silicon, as the lowest bit corresponds directly to the first shift out."
        },
        {
          type: "p",
          text: "• Parity Bit: An optional mathematical helper used for error detection. The transmitter counts the number of logical 1s in the data and sets the parity bit to ensure the total count is either Even or Odd. If a stray electromagnetic spike flips a voltage on the wire, the receiver's computed parity will not match the received parity bit, signaling a transmission failure."
        },
        {
          type: "p",
          text: "• Stop Bit(s): To conclude the frame, the transmitter drives the line back to a High state (logical 1) for one or two bit periods. This stop bit ensures the line is held at High, creating a clean boundary and guaranteeing that the next frame can start with a visible High-to-Low transition."
        },
        {
          type: "p",
          text: "The diagram below represents the exact structure of a single UART frame as it progresses over the physical line from left to right:"
        },
        {
          type: "img",
          src: "Images/uart_frame_schematic.png",
          alt: "UART Frame Schematic Layout"
        }
      ]
    },
    {
      heading: "3. The Synchronous Expectation",
      content: [
        {
          type: "p",
          text: "Asynchronous communication is fundamentally a contract of expectations. Since the receiver has no shared clock line to coordinate when to sample, it must rely entirely on its local oscillator. The receiver listens for the falling edge of the Start Bit, waits for 1.5 bit-times to sample the first data bit at its exact physical center, and then samples every subsequent bit at 1-bit intervals."
        },
        {
          type: "p",
          text: "This mechanism is highly sensitive to clock differences. If the transmitter sends data at 9600 bps (104.16 µs per bit) but the receiver's clock runs slightly slower, the receiver's sampling points will accumulate an error. By the time it reaches the 8th data bit or the stop bit, the phase drift can be so large that it samples a transition edge or an adjacent bit. This is why UART frames are kept short—by resetting the timing alignment on every single frame's Start Bit, the accumulated phase error is reset to zero before it can corrupt the data."
        },
        {
          type: "p",
          text: "UART does not synchronize processors. It synchronizes expectations. A microcontroller running at 120 MHz can speak perfectly to a server running at 2 GHz, because they have agreed to slice time and voltage in the exact same way."
        }
      ]
    },
    {
      heading: "4. Interactive: Build a UART Conversation",
      content: [
        {
          type: "p",
          text: "Use the interactive conversation builder below to explore how letters are encoded into ASCII, packed into serial UART frames, and transmitted as electrical voltages. Toggle the advanced mode to simulate mismatched configurations and observe how timing errors corrupt the signal."
        },
        {
          type: "edgecase",
          id: "uart-conversation-builder"
        }
      ]
    }
  ],
  closing: {
    heading: "The Baseline Contract",
    paragraphs: [
      "In the physical layer, there is only voltage over time. It is the shared protocol agreement that turns this electricity into human language.",
      "UART remains the ultimate baseline interface because it demonstrates that system coordination is not a matter of speed, but of agreement."
    ],
    quote: "Time is the invisible wire in asynchronous communication. When we agree on time, we only need a single wire for the conversation."
  },
  footer: "Reflections on asynchronous serialization - PrajnaEdge.dev"
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

  // URL State Syncing
  if (!isRouting) {
    const newUrl = page === 'home' 
      ? window.location.pathname 
      : `${window.location.pathname}?page=${page}`;
    window.history.pushState({ page }, '', newUrl);
  }
}

// ─── SCROLL TO SYSTEMS TREE ──────────────────────────────────────────────────
function scrollToSystemsTree() {
  showPage('home');
  const treeContainer = document.querySelector('.tree-branch');
  if (treeContainer) {
    setTimeout(() => {
      treeContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 50);
  }
}

// ─── RENDER HOME TREE ────────────────────────────────────────────────────────
function renderHomeTree() {
  const treeContainer = document.querySelector('.tree-branch');
  if (!treeContainer) return;
  
  const nodesKeys = ["Matter", "Computation", "Interaction", "Coordination", "Intelligence"];
  let html = '';
  
  nodesKeys.forEach((key, idx) => {
    const node = systemsTreeNodes[key];
    const activeCount = node.explorations.filter(e => e.id !== null).length;
    const progressText = `(${activeCount})`;
    
    html += `
      <div class="tree-node" onclick="openNodeModal('${key}')">
        <div class="tree-node-title">${escHtml(node.title)}</div>
        <div class="tree-node-progress">${escHtml(progressText)}</div>
      </div>
    `;
    
    if (idx < nodesKeys.length - 1) {
      html += `<div class="tree-arrow"></div>`;
    }
  });
  
  treeContainer.innerHTML = html;
}

// ─── MODAL CONTROLLERS ───────────────────────────────────────────────────────
function openNodeModal(nodeKey) {
  const node = systemsTreeNodes[nodeKey];
  if (!node) return;
  
  const wrapper = document.getElementById('modal-content-wrapper');
  
  wrapper.innerHTML = `
    <h2 class="modal-title">${escHtml(node.title)}</h2>
    <p class="modal-desc" style="margin-bottom: 2.25rem;">${escHtml(node.description)}</p>
    <button class="btn-primary" style="width:100%; justify-content:center; padding:0.85rem; font-size:0.85rem;" onclick="exploreNode('${nodeKey}')">
      Explore ${escHtml(node.title)}
    </button>
  `;
  
  document.getElementById('nodeModal').classList.add('active');
}

function exploreNode(nodeKey) {
  closeModal(null);
  filterNodeRoute(nodeKey);
}

function openDirectExplorations() {
  selectedCategoryFilter = null;
  currentSortOrder = 'newest';
  const sortSelect = document.getElementById('blogSortOrderSelect');
  if (sortSelect) sortSelect.value = 'newest';
  
  document.getElementById('blogsBackToTreeBtn').style.display = 'none';
  document.getElementById('blogsPageTitle').innerText = 'Articles & Write-ups';
  document.getElementById('blogsPageSubtitle').innerText = 'Exploring how systems evolve from hardware to intelligence.';
  renderBlogs(1);
  showPage('blogs');
}

function filterNodeRoute(category) {
  selectedCategoryFilter = category;
  currentSortOrder = 'oldest';
  const sortSelect = document.getElementById('blogSortOrderSelect');
  if (sortSelect) sortSelect.value = 'oldest';

  document.getElementById('blogsBackToTreeBtn').style.display = 'block';
  document.getElementById('blogsPageTitle').innerText = category;
  document.getElementById('blogsPageSubtitle').innerText = systemsTreeNodes[category].description;
  renderBlogs(1);

  // URL State Syncing for filtered category
  if (!isRouting) {
    const newUrl = `${window.location.pathname}?page=blogs&category=${category}`;
    window.history.pushState({ page: 'blogs', category }, '', newUrl);
  }

  isRouting = true;
  showPage('blogs');
  isRouting = false;
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
  const clearBtn = document.getElementById('clearFilterBtn');
  if (clearBtn) clearBtn.style.display = 'none';
  const backBtn = document.getElementById('blogsBackToTreeBtn');
  if (backBtn) backBtn.style.display = 'none';
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

function clearBlogFilterAndGoHome() {
  clearBlogFilter();
  scrollToSystemsTree();
}
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

  let finalItems = [];

  if (selectedCategoryFilter) {
    // Guided Mode: Filtered by Node
    const node = systemsTreeNodes[selectedCategoryFilter];
    if (!node) return;

    // Build the list of items from systemsTreeNodes sequence
    let items = node.explorations.map(exp => {
      if (exp.id !== null) {
        const post = blogPosts.find(p => p.id === exp.id);
        return {
          id: exp.id,
          title: post ? post.title : exp.title,
          subtitle: post ? post.subtitle : '',
          date: post ? post.date : '',
          tags: post ? post.tags : [],
          isPublished: true
        };
      } else {
        return {
          id: null,
          title: exp.title,
          subtitle: '',
          date: '',
          tags: [],
          isPublished: false
        };
      }
    });

    const publishedItems = items.filter(i => i.isPublished);
    const comingSoonItems = items.filter(i => !i.isPublished);

    if (currentSortOrder === "newest") {
      publishedItems.reverse();
    }

    finalItems = [...publishedItems, ...comingSoonItems];
  } else {
    // Discovery Mode: Direct/Unfiltered
    let processed = blogPosts.map(post => ({
      id: post.id,
      title: post.title,
      subtitle: post.subtitle,
      date: post.date,
      tags: post.tags,
      isPublished: true
    }));

    if (currentSortOrder === "newest") {
      processed.reverse();
    }
    finalItems = processed;
  }

  if (finalItems.length === 0) {
    container.innerHTML = `<div style="text-align:center; color:var(--muted); font-family:var(--mono); padding:3rem 0;">// No write-ups found under this category</div>`;
    renderPagination(0, 'blogs');
    return;
  }

  const totalPages = Math.ceil(finalItems.length / BLOGS_PER_PAGE);
  const slice = finalItems.slice((page - 1) * BLOGS_PER_PAGE, page * BLOGS_PER_PAGE);

  container.innerHTML = slice.map(item => {
    if (item.isPublished) {
      return `
        <div class="blog-card" onclick="openItem('${item.id}', 'blogs')">
          <div class="blog-title" style="margin-bottom: 0.5rem;">${escHtml(item.title)}</div>
          <div class="blog-subtitle" style="margin-bottom: 0.85rem;">${escHtml(item.subtitle)}</div>
          <div class="blog-meta" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
            <span>${escHtml(item.date)}</span>
            <div class="tags">${item.tags.map(t => `<span class="tag">${escHtml(t)}</span>`).join('')}</div>
          </div>
        </div>
      `;
    } else {
      return `
        <div class="blog-card locked" style="opacity:0.55; cursor:default; border-style:dashed;">
          <div class="blog-title" style="color:var(--muted); margin-bottom: 0.5rem;">${escHtml(item.title)}</div>
          <div class="blog-meta">
            <span class="tag" style="color:var(--blue); border-color:var(--blue); background:var(--blue-glow); text-transform:uppercase; font-size:0.6rem; letter-spacing:0.05em;">Coming Soon</span>
          </div>
        </div>
      `;
    }
  }).join('');

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
    if (selectedCategoryFilter) {
      backBtn.innerText = `← Back to ${item.category}`;
      backBtn.setAttribute('onclick', `filterNodeRoute('${item.category}')`);
    } else {
      backBtn.innerText = "← Back to Exploration";
      backBtn.setAttribute('onclick', "openDirectExplorations()");
    }
  } else {
    backBtn.innerText = "← Back to Demonstration";
    backBtn.setAttribute('onclick', "showPage('demos')");
  }

  // URL State Syncing
  if (!isRouting) {
    const paramName = type === 'blogs' ? 'exploration' : 'demonstration';
    const newUrl = `${window.location.pathname}?${paramName}=${id}`;
    window.history.pushState({ id, type }, '', newUrl);
  }

  let label = item.category;
  let sectionsHtml = item.sections.map(sec => {
    let blocks = sec.content.map(b => {
      if (b.type === 'p') return `<p style="color:#CBD5E1;line-height:1.85;font-size:0.975rem;margin-bottom:1rem;white-space:pre-line">${escHtml(b.text)}</p>`;
      if (b.type === 'quote') return `<div class="blog-quote">${escHtml(b.text)}</div>`;
      if (b.type === 'code') return `<div class="blog-code" style="color:#A5F3FC;">${escHtml(b.text)}</div>`;
      if (b.type === 'image') return `<div class="blog-img-wrap"><img src="${escHtml(b.src)}" alt="${escHtml(b.alt)}">${b.caption ? `<div class="blog-img-caption">${escHtml(b.caption)}</div>` : ''}</div>`;
      if (b.type === 'edgecase') return `<div id="${escHtml(b.id)}" class="edgecase-container"></div>`;
      return '';
    }).join('');
    return `<div style="margin-bottom:2.5rem"><h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.15rem;color:#fff;margin-bottom:1rem">${escHtml(sec.heading)}</h2>${blocks}</div>`;
  }).join('');

  let navHtml = '';
  if (type === 'blogs') {
    const nodeKey = item.category;
    const node = systemsTreeNodes[nodeKey];
    if (node) {
      const currentIndex = node.explorations.findIndex(e => e.id === item.id);
      if (currentIndex !== -1) {
        const prevExp = currentIndex > 0 ? node.explorations[currentIndex - 1] : null;
        const nextExp = currentIndex < node.explorations.length - 1 ? node.explorations[currentIndex + 1] : null;

        let prevHtml = '';
        if (prevExp && prevExp.id) {
          prevHtml = `
            <span class="nav-dir-label">← Previous</span>
            <a class="nav-link active" onclick="openItem('${prevExp.id}', 'blogs')">${escHtml(prevExp.title)}</a>
          `;
        } else {
          prevHtml = `
            <span class="nav-dir-label">← Previous</span>
            <span class="nav-link locked">None</span>
          `;
        }

        let nextHtml = '';
        if (nextExp && nextExp.id) {
          nextHtml = `
            <span class="nav-dir-label">Next →</span>
            <a class="nav-link active" onclick="openItem('${nextExp.id}', 'blogs')">${escHtml(nextExp.title)}</a>
          `;
        } else {
          nextHtml = `
            <span class="nav-dir-label">Next →</span>
            <span class="nav-link locked">None</span>
          `;
        }

        navHtml = `
          <div class="exploration-nav-block">
            <div class="exploration-nav-grid">
              <div class="nav-prev">${prevHtml}</div>
              <div class="nav-next">${nextHtml}</div>
            </div>
          </div>
        `;
      }
    }
  }

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
    ${navHtml}
  `;
  showPage('blog-post');
  document.querySelectorAll('.edgecase-container').forEach(container => {
    initEdgeCase(container.id);
  });
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

function initEdgeCase(containerId) {
  if (containerId === 'uart-conversation-builder') {
    renderUartConversationBuilder();
  }
}

function renderUartConversationBuilder() {
  const container = document.getElementById('uart-conversation-builder');
  if (!container) return;

  container.className = 'edgecase-wrapper';
  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: Build a UART Conversation</div>
    <div class="edgecase-subheader">Watch a message transform from human-readable text into electrical pulses and back again.</div>

    <!-- PANEL 1: Message Input & Conversion -->
    <div class="ec-panel">
      <div class="ec-panel-title">Panel 1: Message Input &amp; Serialization</div>
      <div class="edgecase-control-group" style="margin-bottom:1rem;">
        <label for="ec-text">Text to Transmit</label>
        <div style="display:flex; gap:0.75rem; align-items:center;">
          <input type="text" id="ec-text" class="edgecase-input" value="Hello" maxlength="12" style="max-width:300px;">
          <button id="ec-tx-btn" class="edgecase-button" style="margin:0;">Transmit &amp; Decode</button>
        </div>
      </div>
      <div>
        <label style="font-family:var(--mono); font-size:0.65rem; color:var(--muted); text-transform:uppercase; display:block; margin-bottom:0.4rem;">Character to Bitstream Mapping</label>
        <div id="ec-serialization-table-container"></div>
      </div>
    </div>

    <!-- PANEL 2: UART Frame Builder -->
    <div class="ec-panel">
      <div class="ec-panel-title">Panel 2: UART Frame Builder (TX Contract)</div>
      
      <div class="edgecase-controls">
        <div class="edgecase-control-group">
          <label for="ec-tx-baud">Baud Rate</label>
          <select id="ec-tx-baud" class="edgecase-select">
            <option value="9600" selected>9600 bps</option>
            <option value="19200">19200 bps</option>
            <option value="115200">115200 bps</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-tx-databits">Data Bits</label>
          <select id="ec-tx-databits" class="edgecase-select">
            <option value="5">5 Bits</option>
            <option value="6">6 Bits</option>
            <option value="7">7 Bits</option>
            <option value="8" selected>8 Bits</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-tx-parity">Parity</label>
          <select id="ec-tx-parity" class="edgecase-select">
            <option value="none" selected>None</option>
            <option value="even">Even</option>
            <option value="odd">Odd</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-tx-stopbits">Stop Bits</label>
          <select id="ec-tx-stopbits" class="edgecase-select">
            <option value="1" selected>1 Bit</option>
            <option value="2">2 Bits</option>
          </select>
        </div>
      </div>

      <div style="margin-top:1rem;">
        <label style="font-family:var(--mono); font-size:0.65rem; color:var(--muted); text-transform:uppercase; display:block; margin-bottom:0.4rem;">Constructed UART Frame (First Character)</label>
        <div id="ec-frame-layout" class="ec-frame-bits-container"></div>
      </div>
    </div>

    <!-- PANEL 3: Transmission Waveform -->
    <div class="ec-panel">
      <div class="ec-panel-title">Panel 3: Electrical Waveform (Physical Wire)</div>
      <div class="ec-transmission-wire">
        <div class="ec-wire-signal"></div>
        <div id="ec-wire-pulse" class="ec-wire-pulse"></div>
      </div>
      <div class="edgecase-visual" id="ec-waveform-container" style="margin-top:1rem; margin-bottom:0;"></div>
    </div>

    <!-- PANEL 4: Receiver & Reconstruction -->
    <div class="ec-panel">
      <div class="ec-panel-title">Panel 4: Receiver &amp; Reconstruction</div>
      <div class="edgecase-output-panel" style="background:#0F172A; border-color:var(--border);">
        <div class="edgecase-output-grid">
          <div class="edgecase-output-box">
            <div class="edgecase-output-label">Receiver Status</div>
            <div class="edgecase-output-val" id="ec-rx-status" style="font-size:0.8rem;">-</div>
          </div>
          <div class="edgecase-output-box">
            <div class="edgecase-output-label">Recovered Message</div>
            <div class="edgecase-output-val" id="ec-rx-recovered" style="font-size:1.1rem; font-weight:600; color:#10B981;">-</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ADVANCED MODE toggle -->
    <div class="ec-advanced-toggle-container">
      <input type="checkbox" id="ec-adv-toggle" class="ec-checkbox">
      <label for="ec-adv-toggle" class="ec-checkbox-label">Advanced Mode: Unlock Receiver Mismatch Experiment</label>
    </div>

    <!-- ADVANCED PANEL -->
    <div id="ec-advanced-panel" class="ec-panel" style="display:none; margin-top:1.25rem; border-color:rgba(239,68,68,0.3);">
      <div class="ec-panel-title" style="color:#EF6868; font-size:0.8rem;">Advanced: Mismatched Receiver Settings (RX Contract)</div>
      <div class="edgecase-controls">
        <div class="edgecase-control-group">
          <label for="ec-rx-baud">RX Baud Rate</label>
          <select id="ec-rx-baud" class="edgecase-select">
            <option value="4800">4800 bps</option>
            <option value="9600" selected>9600 bps</option>
            <option value="14400">14400 bps</option>
            <option value="19200">19200 bps</option>
            <option value="115200">115200 bps</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-rx-databits">RX Data Bits</label>
          <select id="ec-rx-databits" class="edgecase-select">
            <option value="5">5 Bits</option>
            <option value="6">6 Bits</option>
            <option value="7">7 Bits</option>
            <option value="8" selected>8 Bits</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-rx-parity">RX Parity</label>
          <select id="ec-rx-parity" class="edgecase-select">
            <option value="none" selected>None</option>
            <option value="even">Even</option>
            <option value="odd">Odd</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-rx-stopbits">RX Stop Bits</label>
          <select id="ec-rx-stopbits" class="edgecase-select">
            <option value="1" selected>1 Bit</option>
            <option value="2">2 Bits</option>
          </select>
        </div>
      </div>
    </div>
  `;

  // Get DOM elements
  const textInput = document.getElementById('ec-text');
  const txBtn = document.getElementById('ec-tx-btn');
  const tableContainer = document.getElementById('ec-serialization-table-container');
  const frameLayout = document.getElementById('ec-frame-layout');
  const waveformContainer = document.getElementById('ec-waveform-container');
  const rxStatusEl = document.getElementById('ec-rx-status');
  const rxRecoveredEl = document.getElementById('ec-rx-recovered');
  const advToggle = document.getElementById('ec-adv-toggle');
  const advPanel = document.getElementById('ec-advanced-panel');
  const pulseEl = document.getElementById('ec-wire-pulse');

  // TX elements
  const txBaudSel = document.getElementById('ec-tx-baud');
  const txDataBitsSel = document.getElementById('ec-tx-databits');
  const txParitySel = document.getElementById('ec-tx-parity');
  const txStopBitsSel = document.getElementById('ec-tx-stopbits');

  // RX elements
  const rxBaudSel = document.getElementById('ec-rx-baud');
  const rxDataBitsSel = document.getElementById('ec-rx-databits');
  const rxParitySel = document.getElementById('ec-rx-parity');
  const rxStopBitsSel = document.getElementById('ec-rx-stopbits');

  // Add event listeners
  advToggle.addEventListener('change', () => {
    if (advToggle.checked) {
      advPanel.style.display = 'block';
    } else {
      advPanel.style.display = 'none';
      // Reset RX values to match TX
      rxBaudSel.value = txBaudSel.value;
      rxDataBitsSel.value = txDataBitsSel.value;
      rxParitySel.value = txParitySel.value;
      rxStopBitsSel.value = txStopBitsSel.value;
    }
    runSimulation();
  });

  const allControls = [
    textInput, txBaudSel, txDataBitsSel, txParitySel, txStopBitsSel,
    rxBaudSel, rxDataBitsSel, rxParitySel, rxStopBitsSel
  ];
  allControls.forEach(ctrl => {
    ctrl.addEventListener('change', runSimulation);
  });
  textInput.addEventListener('input', runSimulation);

  txBtn.addEventListener('click', () => {
    // Re-trigger pulse animation by removing and adding class
    pulseEl.style.animation = 'none';
    pulseEl.offsetHeight; // trigger reflow
    pulseEl.style.animation = 'travelWire 1.5s infinite linear';
    runSimulation();
  });

  // Run initial simulation
  runSimulation();

  function runSimulation() {
    const text = textInput.value || " ";
    const txBaud = parseInt(txBaudSel.value);
    const txDataBits = parseInt(txDataBitsSel.value);
    const txParity = txParitySel.value;
    const txStopBits = parseInt(txStopBitsSel.value);

    // If advanced mode is disabled, sync RX to TX
    if (!advToggle.checked) {
      rxBaudSel.value = txBaudSel.value;
      rxDataBitsSel.value = txDataBitsSel.value;
      rxParitySel.value = txParitySel.value;
      rxStopBitsSel.value = txStopBitsSel.value;
    }

    const rxBaud = parseInt(rxBaudSel.value);
    const rxDataBits = parseInt(rxDataBitsSel.value);
    const rxParity = rxParitySel.value;
    const rxStopBits = parseInt(rxStopBitsSel.value);

    // Panel 1: ASCII & Binary mapping table
    let tableHtml = `<table class="ec-conversion-table">
      <thead>
        <tr>
          <th>Character</th>
          <th>ASCII Decimal</th>
          <th>Binary Byte (MSB -> LSB)</th>
          <th>Serialization Order (LSB First)</th>
        </tr>
      </thead>
      <tbody>`;
    
    // Show conversion for up to 5 characters for visual clean layout
    const charsToShow = text.slice(0, 5);
    for (let i = 0; i < charsToShow.length; i++) {
      const char = charsToShow[i];
      const code = char.charCodeAt(0);
      let binaryStr = code.toString(2).padStart(8, '0');
      
      // Represent LSB first
      let lsbFirstArr = [];
      for (let b = 0; b < 8; b++) {
        lsbFirstArr.push((code >> b) & 1);
      }
      tableHtml += `<tr>
        <td style="font-weight:bold; color:var(--blue);">${escHtml(char)}</td>
        <td>${code}</td>
        <td>${binaryStr}</td>
        <td>${lsbFirstArr.join(' → ')}</td>
      </tr>`;
    }
    if (text.length > 5) {
      tableHtml += `<tr><td colspan="4" style="text-align:center; color:var(--muted);">... and ${text.length - 5} more characters</td></tr>`;
    }
    tableHtml += `</tbody></table>`;
    tableContainer.innerHTML = tableHtml;

    // Panel 2: Frame layout diagram for the first character
    const firstCode = text.charCodeAt(0) || 32;
    let frameBits = [];
    
    // Idle prefix
    frameBits.push({ type: 'idle', label: 'Idle', val: 1 });
    // Start bit
    frameBits.push({ type: 'start', label: 'Start', val: 0 });
    
    // Data bits
    let charBits = [];
    for (let b = 0; b < txDataBits; b++) {
      const bitVal = (firstCode >> b) & 1;
      charBits.push(bitVal);
      frameBits.push({ type: 'data', label: `D${b}`, val: bitVal });
    }

    // Parity
    let txParityBit = null;
    if (txParity !== 'none') {
      const bitSum = charBits.reduce((a, b) => a + b, 0);
      txParityBit = txParity === 'even' ? (bitSum % 2) : (bitSum % 2 === 0 ? 1 : 0);
      frameBits.push({ type: 'parity', label: 'Parity', val: txParityBit });
    }

    // Stop bits
    for (let s = 0; s < txStopBits; s++) {
      frameBits.push({ type: 'stop', label: `Stop${txStopBits > 1 ? s+1 : ''}`, val: 1 });
    }

    // Idle suffix
    frameBits.push({ type: 'idle', label: 'Idle', val: 1 });

    // Render frame layout box elements
    let boxesHtml = '';
    frameBits.forEach(b => {
      let cssClass = '';
      if (b.type === 'start') cssClass = 'bit-start';
      else if (b.type === 'stop') cssClass = 'bit-stop';
      else if (b.type === 'parity') cssClass = 'bit-parity';
      
      boxesHtml += `
        <div class="ec-bit-box ${cssClass}">
          <div class="bit-label">${b.label}</div>
          <div class="bit-value" style="color: ${b.val === 0 ? '#EF6868' : '#10B981'};">${b.val}</div>
        </div>
      `;
    });
    frameLayout.innerHTML = boxesHtml;

    // Panel 3 & 4: Waveform Rendering & Receiver Emulation
    const T_tx = 1.0;
    const T_rx = txBaud / rxBaud; // Bit width in TX time units

    // We build the TX timeline array
    // Let's model the TX waveform for the first character
    // TX waveform sequence of states:
    let txStates = [];
    txStates.push(1); // Idle
    txStates.push(0); // Start
    txStates.push(...charBits); // Data
    if (txParityBit !== null) {
      txStates.push(txParityBit);
    }
    for (let s = 0; s < txStopBits; s++) {
      txStates.push(1);
    }
    txStates.push(1); // Idle trailing

    // Receiver sampling points
    // RX samples starting from falling edge of start bit at (0.5, 1.5, 2.5, ...) * T_rx
    let rxSamples = [];
    const expectedRxCount = 1 + rxDataBits + (rxParity !== 'none' ? 1 : 0) + rxStopBits;
    
    for (let i = 0; i < expectedRxCount; i++) {
      const rxSampleTime = (0.5 + i) * T_rx; // physically relative to Start falling edge (which occurs at physical time = 1.0 bit-units because of the Idle prefix)
      // Since Start is at index 1, physical offset on TX timeline is:
      const txPhysicalTime = 1.0 + rxSampleTime;
      const txBitIdx = Math.floor(txPhysicalTime);
      let sampledVal = 1;
      if (txBitIdx >= 0 && txBitIdx < txStates.length) {
        sampledVal = txStates[txBitIdx];
      }
      rxSamples.push({
        idx: i,
        sampleTime: rxSampleTime,
        txPhysicalTime: txPhysicalTime,
        val: sampledVal,
        bitLabel: i === 0 ? 'Start' : (i <= rxDataBits ? `D${i-1}` : (i === rxDataBits + 1 && rxParity !== 'none' ? 'Par' : 'Stop'))
      });
    }

    // Render SVG
    const svgWidth = 800;
    const svgHeight = 160;
    const paddingLeft = 60;
    const paddingRight = 40;
    const paddingTop = 30;
    const paddingBottom = 30;
    const chartWidth = svgWidth - paddingLeft - paddingRight;
    const chartHeight = svgHeight - paddingTop - paddingBottom;
    const bitWidth = chartWidth / txStates.length;

    // Draw TX voltage waveform path
    let pathD = `M 0,${paddingTop + 10} L ${paddingLeft},${paddingTop + 10}`;
    for (let i = 0; i < txStates.length; i++) {
      const val = txStates[i];
      const y = val === 1 ? paddingTop + 10 : paddingTop + chartHeight - 10;
      const xStart = paddingLeft + i * bitWidth;
      const xEnd = paddingLeft + (i + 1) * bitWidth;
      pathD += ` L ${xStart},${y} L ${xEnd},${y}`;
    }
    pathD += ` L ${svgWidth},${paddingTop + 10}`;

    // Draw sampling marks
    let sampleMarksHtml = '';
    rxSamples.forEach(s => {
      const x = paddingLeft + s.txPhysicalTime * bitWidth;
      if (x > svgWidth) return;

      // Color coding of sampling points
      // Check if it matches TX state at the sample time
      const txBitIdx = Math.floor(s.txPhysicalTime);
      const expectedVal = (txBitIdx >= 0 && txBitIdx < txStates.length) ? txStates[txBitIdx] : 1;
      const isCorrect = s.val === expectedVal;
      const strokeColor = isCorrect ? '#3B82F6' : '#EF6868';
      const dashStyle = isCorrect ? '3,3' : '1,1';

      sampleMarksHtml += `
        <line x1="${x}" y1="${paddingTop}" x2="${x}" y2="${paddingTop + chartHeight}" stroke="${strokeColor}" stroke-dasharray="${dashStyle}" stroke-width="1.5" />
        <circle cx="${x}" cy="${paddingTop + chartHeight / 2}" r="4.5" fill="${strokeColor}" />
        <text x="${x}" y="${paddingTop + chartHeight + 15}" fill="${strokeColor}" font-family="var(--mono)" font-size="8" text-anchor="middle">S${s.idx}</text>
      `;
    });

    // Draw grid lines separating TX bit slots
    let gridLinesHtml = '';
    for (let i = 0; i <= txStates.length; i++) {
      const x = paddingLeft + i * bitWidth;
      let label = '';
      if (i < txStates.length) {
        if (i === 0) label = 'IDLE';
        else if (i === 1) label = 'START';
        else if (i - 1 <= txDataBits) label = `D${i-2}`;
        else if (i - 1 === txDataBits + 1 && txParity !== 'none') label = 'PAR';
        else if (i < txStates.length - 1) label = 'STOP';
        else label = 'IDLE';
      }
      gridLinesHtml += `
        <line x1="${x}" y1="${paddingTop}" x2="${x}" y2="${paddingTop + chartHeight}" stroke="rgba(148, 163, 184, 0.1)" stroke-width="1" />
        ${label ? `<text x="${x + bitWidth/2}" y="${paddingTop - 8}" fill="var(--muted)" font-family="var(--mono)" font-size="8" text-anchor="middle">${label}</text>` : ''}
      `;
    }

    const svgHtml = `
      <svg viewBox="0 0 ${svgWidth} ${svgHeight}" width="100%">
        ${gridLinesHtml}
        <text x="${paddingLeft - 8}" y="${paddingTop + 14}" fill="var(--muted)" font-family="var(--mono)" font-size="9" text-anchor="end">HIGH (1)</text>
        <text x="${paddingLeft - 8}" y="${paddingTop + chartHeight - 6}" fill="var(--muted)" font-family="var(--mono)" font-size="9" text-anchor="end">LOW (0)</text>
        <path d="${pathD}" fill="none" stroke="#FFF" stroke-width="2" />
        ${sampleMarksHtml}
      </svg>
    `;
    waveformContainer.innerHTML = svgHtml;

    // Decode all characters of the input string under current configurations
    let decodedMessage = '';
    let hasFramingError = false;
    let hasParityError = false;

    for (let cIdx = 0; cIdx < text.length; cIdx++) {
      const charVal = text.charCodeAt(cIdx);
      
      // Serialize character according to TX parameters
      let txCharBits = [];
      for (let b = 0; b < txDataBits; b++) {
        txCharBits.push((charVal >> b) & 1);
      }
      let txParBit = null;
      if (txParity !== 'none') {
        const sum = txCharBits.reduce((a, b) => a + b, 0);
        txParBit = txParity === 'even' ? (sum % 2) : (sum % 2 === 0 ? 1 : 0);
      }

      // Build TX frame array for this specific char
      let txFrame = [0]; // Start bit
      txFrame.push(...txCharBits);
      if (txParBit !== null) txFrame.push(txParBit);
      for (let s = 0; s < txStopBits; s++) txFrame.push(1);

      // Emulate RX sampling
      let sampledBits = [];
      for (let i = 0; i < expectedRxCount; i++) {
        const rxTime = (0.5 + i) * T_rx;
        const txIdx = Math.floor(rxTime);
        let val = 1; // Idle if sampled out of bounds
        if (txIdx >= 0 && txIdx < txFrame.length) {
          val = txFrame[txIdx];
        }
        sampledBits.push(val);
      }

      // Parse sampled bits according to RX parameters
      // Start is at sampledBits[0]
      const rxStartVal = sampledBits[0];
      const rxData = sampledBits.slice(1, 1 + rxDataBits);
      const rxPar = rxParity !== 'none' ? sampledBits[1 + rxDataBits] : null;
      
      let rxStopStartIdx = 1 + rxDataBits + (rxParity !== 'none' ? 1 : 0);
      const rxStop = sampledBits.slice(rxStopStartIdx, rxStopStartIdx + rxStopBits);

      // Check errors
      let framingErr = false;
      if (rxStartVal !== 0) framingErr = true;
      rxStop.forEach(sb => {
        if (sb !== 1) framingErr = true;
      });

      let parityErr = false;
      if (rxParity !== 'none' && rxPar !== null) {
        const rxSum = rxData.reduce((a, b) => a + b, 0);
        const expectedPar = rxParity === 'even' ? (rxSum % 2) : (rxSum % 2 === 0 ? 1 : 0);
        if (rxPar !== expectedPar) parityErr = true;
      }

      if (framingErr) hasFramingError = true;
      if (parityErr) hasParityError = true;

      // Reconstruct ASCII character value
      let recCharVal = 0;
      for (let b = 0; b < rxDataBits; b++) {
        if (rxData[b] === 1) {
          recCharVal |= (1 << b);
        }
      }

      // Format character output
      let charStr = '';
      if (recCharVal >= 32 && recCharVal <= 126) {
        charStr = String.fromCharCode(recCharVal);
      } else {
        charStr = ''; // replacement character
      }

      if (framingErr || parityErr) {
        decodedMessage += `<span class="text-corrupted" title="Error">${escHtml(charStr)}</span>`;
      } else {
        decodedMessage += escHtml(charStr);
      }
    }

    // Set receiver diagnostic status
    let statusText = '';
    if (!hasFramingError && !hasParityError) {
      statusText = `<span class="edgecase-status-badge edgecase-status-ok">Locked &amp; Decoded</span><br>
                    <span style="font-size:0.68rem; color:var(--muted); margin-top:0.4rem; display:block;">TX and RX contracts are compatible. Character timings line up perfectly within phase margins.</span>`;
    } else {
      let errLabels = [];
      if (hasFramingError) errLabels.push('Framing Error');
      if (hasParityError) errLabels.push('Parity Error');
      statusText = `<span class="edgecase-status-badge edgecase-status-error">${errLabels.join(' / ')}</span><br>
                    <span style="font-size:0.68rem; color:#EF6868; margin-top:0.4rem; display:block;">Expectations mismatched. The receiver sampled outside of the expected frame boundaries or detected bad parity.</span>`;
    }

    rxStatusEl.innerHTML = statusText;
    rxRecoveredEl.innerHTML = decodedMessage;
  }
}

// ─── INIT ─────────────────────────────────────────────────────────────────────
let isRouting = false;

function handleUrlRouting() {
  isRouting = true;
  const params = new URLSearchParams(window.location.search);
  const page = params.get('page');
  const blogId = params.get('exploration');
  const demoId = params.get('demonstration');
  
  if (blogId) {
    openItem(blogId, 'blogs');
  } else if (demoId) {
    openItem(demoId, 'demos');
  } else if (page) {
    const category = params.get('category');
    if (page === 'blogs') {
      if (category && systemsTreeNodes[category]) {
        filterNodeRoute(category);
      } else {
        openDirectExplorations();
      }
    } else if (page === 'journey' || page === 'systems-map') {
      showPage('journey');
    } else if (page === 'demos' || page === 'demonstrations') {
      showPage('demos');
    } else if (page === 'about') {
      showPage('about');
    } else if (page === 'contact') {
      showPage('contact');
    } else {
      showPage('home');
    }
  } else {
    showPage('home');
  }
  isRouting = false;
}

renderBlogs(1);
renderDemos(1);
renderHomeTree();
handleUrlRouting();

window.addEventListener('popstate', () => {
  handleUrlRouting();
});

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
