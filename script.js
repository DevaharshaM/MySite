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
      { id: null, title: "The First Instruction", status: "Coming Soon" },
      { id: null, title: "Coming Soon" }
    ]
  },
  Interaction: {
    title: "Interaction",
    description: "The moment software crossed into physical consequence.",
    explorations: [
      { id: "why-systems-need-interfaces", title: "Why Systems Need Interfaces" },
      { id: "the-physical-edge-of-software", title: "The Physical Edge of Software" },
      { id: null, title: "Why Embedded Systems Speak in Protocols", status: "Coming Soon" },
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
    const progressText = activeCount > 0 ? `${activeCount} Exploration${activeCount > 1 ? 's' : ''}` : "Coming Soon";
    const isClickable = activeCount > 0;
    
    html += `
      <div class="tree-node${!isClickable ? ' disabled' : ''}" 
           ${isClickable ? `onclick="openNodeModal('${key}')"` : 'style="cursor:default; opacity:0.6;"'}>
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
  
  const explorationsHtml = node.explorations.map((exp, index) => {
    const isPublished = exp.id !== null;
    const num = String(index + 1).padStart(2, '0');
    if (isPublished) {
      return `
        <div class="progression-item active" onclick="openNodeExploration('${exp.id}')">
          <span class="progression-num">${num}</span>
          <span class="progression-title">${escHtml(exp.title)}</span>
        </div>
      `;
    } else {
      const isComingSoon = exp.status === "Coming Soon" || exp.title !== "Coming Soon";
      const badgeHtml = isComingSoon ? `<span class="progression-badge">Coming Soon</span>` : '';
      return `
        <div class="progression-item locked">
          <span class="progression-num">${num}</span>
          <span class="progression-title">${escHtml(exp.title)}</span>
          ${badgeHtml}
        </div>
      `;
    }
  }).join('');
  
  wrapper.innerHTML = `
    <h2 class="modal-title">${escHtml(node.title)}</h2>
    <p class="modal-desc">${escHtml(node.description)}</p>
    <div class="modal-explores-label">Systems Map Progression:</div>
    <div class="exploration-progression">
      ${explorationsHtml}
    </div>
  `;
  
  document.getElementById('nodeModal').classList.add('active');
}

function openNodeExploration(blogId) {
  closeModal(null);
  openItem(blogId, 'blogs');
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
      if (b.type === 'image') return `<div class="blog-img-wrap"><img src="${escHtml(b.src)}" alt="${escHtml(b.alt)}">${b.caption ? `<div class="blog-img-caption">${escHtml(b.caption)}</div>` : ''}</div>`;
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
        if (prevExp) {
          if (prevExp.id) {
            prevHtml = `
              <span class="nav-dir-label">← Previous</span>
              <a class="nav-link active" onclick="openItem('${prevExp.id}', 'blogs')">${escHtml(prevExp.title)}</a>
            `;
          } else {
            prevHtml = `
              <span class="nav-dir-label">← Previous</span>
              <span class="nav-link locked">Coming Soon</span>
            `;
          }
        } else {
          prevHtml = `
            <span class="nav-dir-label">← Previous</span>
            <span class="nav-link locked">None</span>
          `;
        }

        let nextHtml = '';
        if (nextExp) {
          if (nextExp.id) {
            nextHtml = `
              <span class="nav-dir-label">Next →</span>
              <a class="nav-link active" onclick="openItem('${nextExp.id}', 'blogs')">${escHtml(nextExp.title)}</a>
            `;
          } else {
            nextHtml = `
              <span class="nav-dir-label">Next →</span>
              <span class="nav-link locked">${escHtml(nextExp.title || "Coming Soon")}</span>
            `;
          }
        } else {
          nextHtml = `
            <span class="nav-dir-label">Next →</span>
            <span class="nav-link locked">Coming Soon</span>
          `;
        }

        navHtml = `
          <div class="exploration-nav-block">
            <div class="exploration-nav-header">
              <span class="nav-node-label">System Tree Node</span>
              <span class="nav-node-name">${escHtml(node.title)}</span>
            </div>
            <div class="exploration-nav-grid">
              <div class="nav-prev">${prevHtml}</div>
              <div class="nav-current">
                <span class="nav-dir-label">Current Exploration</span>
                <span class="nav-title-current">${escHtml(item.title)}</span>
              </div>
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
renderHomeTree();

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
