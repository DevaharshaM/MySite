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
      { id: "spi-shared-rhythm-of-machines", title: "SPI: The Shared Rhythm of Machines" },
      { id: "i2c-the-shared-conversation", title: "I2C: The Shared Conversation" },
      { id: "can-the-language-of-many-voices", title: "CAN: The Language of Many Voices" },
      { id: "the-roads-not-often-travelled", title: "The Roads Not Often Travelled" },
      { id: null, title: "Coming Soon" }
    ]
  },
  Coordination: {
    title: "Coordination",
    description: "Why isolated computation evolved into synchronized systems.",
    explorations: [
      { id: "the-architecture-of-time", title: "The Architecture of Time" },
      { id: "when-machines-learned-to-observe", title: "When Machines Learned to Observe" },
      { id: "when-machines-learned-to-speak-back", title: "When Machines Learned to Speak Back" },
      { id: "the-tyranny-of-waiting", title: "The Tyranny of Waiting" },
      { id: "when-hardware-learned-to-interrupt", title: "When Hardware Learned to Interrupt" },
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
          type: "image",
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
},
{
  id: "spi-shared-rhythm-of-machines",
  category: "Interaction",
  series: "System Explorations",
  title: "SPI: The Shared Rhythm of Machines",
  subtitle: "Why timing agreement wasn't enough, and why engineers chose to share a clock.",
  date: "16th June, 2026",
  tags: ["SPI", "Serial Protocols", "Synchronous", "Clock Phase", "Shift Register", "Embedded Systems"],
  sections: [
    {
      heading: "1. The Limits of Asynchronous Agreement",
      content: [
        {
          type: "p",
          text: "In the exploration of UART, we observed how two independent microprocessors, each operating in their own private temporal domain, can exchange data using a single wire and a shared agreement. By setting a predetermined baud rate, the receiver can reconstruct bit boundaries simply by counting local oscillator cycles relative to the falling edge of the Start Bit. It is an elegant, minimal approach to interaction—yet it is built upon a delicate physical compromise."
        },
        {
          type: "p",
          text: "This compromise becomes a bottleneck as system throughput requirements escalate. Because the asynchronous receiver relies entirely on its local clock, any physical discrepancy between the transmitter's oscillator and the receiver's oscillator accumulates over the frame. At 9600 baud, a 2% timing mismatch is inconsequential; the sample point drifts only slightly away from the bit's center. But if we attempt to scale the transfer rate to 10 Mbps or 20 Mbps, a fraction of a microsecond of phase drift translates into multiple bit periods of misalignment, causing catastrophic corruption."
        },
        {
          type: "p",
          text: "To combat this drift, asynchronous frames must remain short—typically restricted to 8 payload bits. Consequently, a substantial portion of the bandwidth is consumed by non-data overhead: start bits, stop bits, and idle gaps. For every byte sent, at least two framing bits must be transmitted, yielding an automatic 20% protocol tax. When a system needs to transfer megabytes of image data to a display, or pull raw high-frequency sensor readings, this framing overhead and timing sensitivity make the asynchronous model physically untenable."
        }
      ]
    },
    {
      heading: "2. Shifting the Burden: The Shared Clock",
      content: [
        {
          type: "p",
          text: "To break past the speed limits of asynchronous protocols, embedded engineers had to rethink the nature of time itself. Instead of requiring the receiver to reconstruct time, why not transmit time directly along with the data?"
        },
        {
          type: "p",
          text: "This shift in thinking is the core of Synchronous communication, and it is the foundation of the Serial Peripheral Interface (SPI). By adding a dedicated physical line—the Serial Clock (SCLK)—the transmitter takes on the responsibility of orchestrating the timing of the entire bus. The receiver no longer needs to guess where a bit begins or ends, nor does it need to count local clock ticks. It simply watches the SCLK wire: when the clock line transitions, the receiver samples the data line. When the clock line is idle, the system waits."
        },
        {
          type: "p",
          text: "This physical synchrony immediately eliminates the threat of oscillator drift. Because the clock line dictates the timing of the data transitions, the bus speed can scale from zero to tens of megahertz without phase misalignment. If the master processor pauses mid-transmission to handle an interrupt, the clock simply stops, the state of the bus freezes in place, and the transfer resumes later without a single bit of corrupted data. Time becomes a physical signal, not an expectation."
        }
      ]
    },
    {
      heading: "3. The Four Wires of the Bus",
      content: [
        {
          type: "p",
          text: "To achieve this high-speed, synchronous coordination, SPI establishes a strict Master-Slave hierarchy. Unlike UART's symmetric point-to-point architecture, an SPI bus always operates under the absolute control of a single Master device. The master generates the clock signal and drives the conversation. The Slave devices are passive, reacting only to the clock and signal boundaries initiated by the master."
        },
        {
          type: "p",
          text: "The physical interface consists of four dedicated lines, each serving a distinct architectural role:"
        },
        {
          type: "p",
          text: "• SCLK (Serial Clock): Driven exclusively by the master, this line carries the pulse train that synchronizes data shifts and samples across all connected devices."
        },
        {
          type: "p",
          text: "• MOSI (Master Out Slave In): The data line driven by the master to transmit payload bits to the slave."
        },
        {
          type: "p",
          text: "• MISO (Master In Slave Out): The data line driven by the slave to transmit payload bits back to the master."
        },
        {
          type: "p",
          text: "• CS / SS (Chip Select / Slave Select): An active-low control line used by the master to address and enable individual slaves. Holding the CS line low selects the target slave and wakes its interface logic; pulling it high disconnects the slave's MISO driver into a high-impedance (tri-state) mode, isolating it from the shared bus."
        },
        {
          type: "p",
          text: "The schematic below illustrates how these four lines form the baseline interface between a master and a single slave device:"
        },
        {
          type: "image",
          src: "Images/spi_bus_topology.png",
          alt: "SPI Master-Slave Bus Interface Topology"
        }
      ]
    },
    {
      heading: "4. The Shift Register Loop: Continuous Exchange",
      content: [
        {
          type: "p",
          text: "In many protocols, write operations and read operations are separate events, separated by direction changes and state handshakes. SPI, however, approaches data exchange with a unique hardware-level elegance. At its silicon core, an SPI transaction is not a separate write and read; it is a simultaneous circular swap."
        },
        {
          type: "p",
          text: "Both the master and slave contain an internal shift register—typically 8 bits wide. When the master initiates a transaction, these two registers are physically connected in a closed circular loop via the MOSI and MISO lines. As SCLK toggles, the master shifts its most significant bit (MSB) out of its register onto the MOSI line, where it is shifted into the least significant bit (LSB) of the slave's register. Simultaneously, the slave shifts its MSB out onto the MISO line, where it enters the master's LSB."
        },
        {
          type: "p",
          text: "After exactly 8 clock pulses, the two bytes have completely swapped places. What was in the master is now in the slave, and what was in the slave is now in the master. Every SPI write is also a read, and every SPI read requires a write. If the master only wants to read a byte from an external flash memory, it must shift out a dummy byte to generate the clock cycles required to pull the slave's data in."
        },
        {
          type: "p",
          text: "This circular data loop is illustrated below, showcasing the hardware shift register interaction during a transfer:"
        },
        {
          type: "image",
          src: "Images/spi_shift_registers.png",
          alt: "SPI Full-Duplex Shift Register Loop"
        }
      ]
    },
    {
      heading: "5. CPOL and CPHA: The Choreography of Sampling",
      content: [
        {
          type: "p",
          text: "Because SPI is a raw hardware-level interface without a predefined standard, different slave devices require different timing alignments. Some chips expect data to change when the clock rises and be sampled when the clock falls. Others require the exact opposite. To accommodate these differences, SPI defines two configurable parameters that dictate the clock's timing behavior: Clock Polarity (CPOL) and Clock Phase (CPHA)."
        },
        {
          type: "p",
          text: "CPOL defines the idle state of the clock line when no communication is active:"
        },
        {
          type: "p",
          text: "• CPOL = 0: SCLK idles at Low (0V). The active phase of the clock consists of rising edges, and the trailing phase consists of falling edges."
        },
        {
          type: "p",
          text: "• CPOL = 1: SCLK idles at High (3.3V/VCC). The active phase of the clock consists of falling edges, and the trailing phase consists of rising edges."
        },
        {
          type: "p",
          text: "CPHA defines which clock transition is used to shift data vs. which edge is used to sample it:"
        },
        {
          type: "p",
          text: "• CPHA = 0: Data is sampled on the first (leading) edge of SCLK, and shifted out onto the line on the second (trailing) edge. This mode requires that the transmitter places the first data bit on the line the moment CS is pulled low, before the first clock edge even occurs."
        },
        {
          type: "p",
          text: "• CPHA = 1: Data is shifted onto the line on the first (leading) edge of SCLK, and sampled on the second (trailing) edge."
        },
        {
          type: "p",
          text: "By combining these two parameters, engineers can configure the interface in one of four distinct SPI Modes (0, 1, 2, or 3). The timing diagram below demonstrates how these configurations adjust the relationship between SCLK transitions and the MOSI/MISO data windows:"
        },
        {
          type: "image",
          src: "Images/spi_clock_modes.png",
          alt: "SPI Timing Diagram illustrating CPOL and CPHA configuration modes"
        },
        {
          type: "edgecase",
          id: "spi-shared-rhythm"
        }
      ]
    },
    {
      heading: "6. Bus Expansion and the Chip Select Problem",
      content: [
        {
          type: "p",
          text: "Unlike network protocols that use digital addresses embedded inside data packets, SPI addresses devices physically. If a master wishes to communicate with multiple slave devices on a shared bus, it can do so in one of two configurations: independent slave routing or daisy-chaining."
        },
        {
          type: "p",
          text: "In the independent configuration, the master shares the SCLK, MOSI, and MISO lines across all slaves, but routes a dedicated, individual Chip Select (CS) line to each chip. To speak to Slave A, the master pulls CS_A low while keeping CS_B high. This isolates Slave B's MISO pin, preventing it from driving the shared trace and causing bus contention. While this configuration is incredibly fast and simple to route, it suffers from severe pin inflation: adding a fourth slave requires adding a fourth IO pin to the master."
        },
        {
          type: "p",
          text: "In the daisy-chain configuration, the master routes a single CS and SCLK to all slaves, but loops the MISO of one slave into the MOSI of the next, forming one giant, multi-byte shift register loop. While this saves IO pins, it introduces timing delays, as the master must shift data through every single slave in the chain to update a single register, and requires that all slaves support daisy-chain formatting in their silicon."
        },
        {
          type: "p",
          text: "Physical addressing introduces silent bugs. If a glitch or transient voltage spike pulls a CS line low when it should remain high, multiple slaves will attempt to drive the MISO trace simultaneously. This results in bus contention, creating excessive current draw, heating, and corrupted data—a silent failure state that cannot be detected by the protocol itself since SPI lacks any built-in error detection or flow control."
        },
        {
          type: "edgecase",
          id: "spi-silent-conversation"
        }
      ]
    },
    {
      heading: "7. The Trade-Offs of Raw Speed",
      content: [
        {
          type: "p",
          text: "SPI's dominance in high-speed, low-level embedded interfaces stems from its simplicity. Because it is synchronous, it has no start or stop bits, yielding 100% data throughput efficiency. Because it has dedicated TX and RX pins, it supports true full-duplex communication. There is no addressing overhead, no arbitration delays, and no complex state machines in silicon, allowing SPI peripherals to be incredibly small, cheap, and fast."
        },
        {
          type: "p",
          text: "However, this simplicity comes at a cost:"
        },
        {
          type: "p",
          text: "• Pin Inflation: Every additional slave requires a dedicated CS pin in independent mode. A bus with six sensors quickly consumes nine microcontroller pins, cluttering the PCB layout and exhausting register space."
        },
        {
          type: "p",
          text: "• No Flow Control: SPI is a 'blind' protocol. The master drives SCLK regardless of whether the slave is ready, busy, or has crashed. If the slave cannot process incoming bits fast enough, data is silently overwritten in its shift register."
        },
        {
          type: "p",
          text: "• No Error Checking: Unlike UART, which supports optional parity bits, or CAN, which uses CRC checksums, SPI contains no built-in mechanism to verify data integrity. If electrical noise distorts a bit on the wire, the receiver registers the wrong value without warning."
        }
      ]
    },
    {
      heading: "8. The Coexistence of Two Worlds",
      content: [
        {
          type: "p",
          text: "Despite these limitations, SPI remains the undisputed standard for high-bandwidth embedded peripherals. When a microcontroller needs to write thousands of pixels to a color LCD, pull megabytes of firmware from a Serial Flash memory chip, or stream high-fidelity audio samples, SPI's raw speed—often exceeding 50 MHz—is essential."
        },
        {
          type: "p",
          text: "UART taught us that two independent nodes can communicate through a mutual agreement on time. SPI showed us that by sharing a clock physically, we can discard the timing contract and unlock speeds orders of magnitude higher. But as embedded systems grew more complex, containing dozens of small sensors, displays, and controllers on a single board, the pin inflation of SPI's multi-wire bus became an intolerable physical constraint."
        },
        {
          type: "p",
          text: "Engineers were faced with a new design challenge: How do we retain the speed benefits of a shared clock, but route the entire system using only two wires, regardless of how many devices are connected? This design tension would eventually drive the creation of I2C—a protocol that trade-offs raw speed to achieve absolute pin efficiency."
        }
      ]
    }
  ],
  closing: {
    heading: "The Synchronization Rhythm",
    paragraphs: [
      "In the design of digital interfaces, speed is a function of synchrony. When we share a clock, we share a pulse, allowing data to flow at the speed of silicon state transitions.",
      "SPI survives because it is the ultimate expression of raw hardware-level communication: fast, simple, and unburdened by protocol overhead."
    ],
    quote: "A shared clock is a shared heartbeat. When systems beat to the same rhythm, they no longer need to discuss when to speak."
  },
  footer: "Reflections on synchronous SPI communication - PrajnaEdge.dev"
},
{
  id: "i2c-the-shared-conversation",
  category: "Interaction",
  series: "System Explorations",
  part: 3,
  title: "I2C: The Shared Conversation",
  subtitle: "How open-drain logic and addressing solved the pin inflation crisis of SPI.",
  date: "20th June, 2026",
  tags: ["I2C", "Serial Protocols", "Open Drain", "Arbitration", "Embedded Systems"],
  sections: [
    {
      heading: "1. The SPI Pin Crisis",
      content: [
        {
          type: "p",
          text: "SPI unlocked extreme communication speeds by sharing a clock, but it introduced a severe hardware bottleneck: pin inflation. Because SPI has no addressing system, the master must use a dedicated Chip Select (CS) pin for every single peripheral on the bus. If you connect five sensors, you need five separate CS pins. If you scale to ten devices, your microcontroller's GPIO lines are consumed entirely by chip selection.\n\nThis physical routing nightmare forced engineers to re-evaluate the bus architecture. They needed a protocol that preserved the benefits of a synchronous clock but allowed dozens of devices to share the exact same physical wires without a forest of chip select lines. The solution was the Inter-Integrated Circuit (I2C) protocol."
        }
      ]
    },
    {
      heading: "2. Shared Wires: The Two-Line Compromise",
      content: [
        {
          type: "p",
          text: "I2C makes a radical design trade-off. It discards the four-wire, point-to-point architecture of SPI in favor of a strictly shared, two-wire bus: SDA (Serial Data) and SCL (Serial Clock). Every device on the bus connects to these same two traces.\n\nBy shrinking the bus to two wires, I2C eliminates the physical pin bottleneck. A master can communicate with over a hundred devices using the exact same two pins. However, this simplicity introduces a complex electrical challenge: if multiple devices share the same data and clock lines, how do we prevent them from colliding and burning out their output drivers when one tries to transmit a 1 while another transmits a 0?"
        },
        {
          type: "image",
          src: "Images/i2c_bus_topology.png",
          alt: "I2C Shared Bus Topology showing Pull-up resistors and multiple slaves"
        }
      ]
    },
    {
      heading: "3. The Physics of Open-Drain Buses",
      content: [
        {
          type: "p",
          text: "In standard push-pull output stages (used in UART and SPI), a device actively drives the line HIGH (connecting it to VCC) or actively drives it LOW (connecting it to GND). If Device A drives HIGH while Device B drives LOW on a shared wire, a low-resistance path is created directly from VCC to GND. This causes a short circuit, excessive current draw, heating, and physical damage to the silicon.\n\nTo prevent this, I2C uses open-drain (or open-collector) output buffers combined with physical pull-up resistors on both SCL and SDA. In an open-drain buffer, a device can only actively pull the line LOW (turning on an internal NMOS transistor connected to GND). It cannot actively drive the line HIGH; instead, to send a 1, it simply turns off the transistor and lets the line float. The external pull-up resistor then pulls the line HIGH.\n\nThis creates a 'wired-AND' logic bus. If any single device pulls the line LOW, the entire line goes LOW. The line only returns HIGH when every single device releases it. Electrical collisions are resolved safely: if two devices write conflicting states, the line simply resolves to LOW, drawing only a safe, limited current through the pull-up resistor."
        },
        {
          type: "image",
          src: "Images/i2c_open_drain.png",
          alt: "I2C Open-Drain Transistor Circuit Schematic"
        }
      ]
    },
    {
      heading: "4. The Syntax of a Shared Wire",
      content: [
        {
          type: "p",
          text: "Because I2C lacks physical Chip Select lines, the protocol must establish starting boundaries and address routing directly within the two-wire interface. Under normal operation, the SDA line is only allowed to change state when the SCL clock line is LOW. When SCL is HIGH, the data on SDA must remain stable to be sampled.\n\nI2C exploits this stability rule to define START and STOP conditions. A START condition is signaled when SDA transitions from HIGH to LOW while SCL is HIGH. A STOP condition is signaled when SDA transitions from LOW to HIGH while SCL is HIGH. These transitions act as start-of-frame and end-of-frame markers that every peripheral monitors on the bus, resetting their internal receivers to listen for addressing."
        },
        {
          type: "image",
          src: "Images/i2c_start_stop.png",
          alt: "I2C START and STOP Condition Waveforms"
        }
      ]
    },
    {
      heading: "5. Software Addressing and Handshaking",
      content: [
        {
          type: "p",
          text: "Immediately following a START condition, the master transmits a 9-bit address frame. The first 7 bits represent the unique target address of the slave. The 8th bit indicates the transaction direction: Write (0) or Read (1).\n\nThe 9th clock cycle is reserved for a hardware handshake: the Acknowledge (ACK) bit. During the 9th clock tick, the master releases the SDA line (letting it float HIGH). The slave device matching the address must actively pull the SDA line LOW. If the slave pulls SDA LOW, it is an ACK—the transaction continues. If the slave is missing, busy, or has crashed, the line remains HIGH (a Not-Acknowledge, or NACK), signaling the master to stop."
        },
        {
          type: "edgecase",
          id: "i2c-shared-bus"
        }
      ]
    },
    {
      heading: "6. Slowing the Master: Clock Stretching",
      content: [
        {
          type: "p",
          text: "SPI is a 'blind' protocol: the master drives SCLK regardless of whether the slave has processed the data. If the slave lags behind, data is lost. I2C solves this flow-control problem using clock stretching.\n\nAlthough the master normally controls SCL, the open-drain architecture allows a slave to take control. If a slave needs more time to process a byte or fetch sensor readings, it can actively hold the SCL line LOW after the master releases it. The master monitors the SCL line: as long as it senses SCL is LOW, its internal clock generator pauses, freezing the transaction. Only when the slave releases SCL does it float HIGH and the master continues."
        }
      ]
    },
    {
      heading: "7. Polite Arguments: Multi-Master Arbitration",
      content: [
        {
          type: "p",
          text: "In complex systems, multiple master devices may share the same bus. If two masters assert a START condition simultaneously, I2C uses bus arbitration to resolve conflicts without corrupting data or causing electrical shorts.\n\nBecause of the open-drain wired-AND structure, both masters can drive SCL and SDA. As they transmit data bits, each master monitors the actual state of the SDA line. As long as the bus matches the bits they write, they proceed. However, if Master A writes a 1 (releasing SDA) but Master B writes a 0 (pulling SDA LOW), the bus resolves to LOW. Master A, sensing a LOW when it expected a HIGH, realizes another master is active, immediately halts its transmission, releases the bus, and falls back to receiver mode. Master B continues its transaction completely uninterrupted, unaware of the silent victory."
        },
        {
          type: "image",
          src: "Images/i2c_arbitration.png",
          alt: "I2C Multi-Master Arbitration Timing Diagram"
        }
      ]
    },
    {
      heading: "8. The Threshold of Complexity",
      content: [
        {
          type: "p",
          text: "Let's review the journey: UART taught us to align clock phases through a timing contract between two nodes. SPI showed us that sharing a physical clock yields speeds orders of magnitude higher at the cost of dedicated wiring. I2C showed us that by using addressing and open-drain physics, we can share the clock and data wires completely, scaling to dozens of devices using only two pins.\n\nYet I2C has limits. The pull-up resistors create an RC time constant with the parasitic capacitance of the wires: as the bus gets longer or more devices are added, the rising edge of SCL/SDA becomes slow and rounded, limiting speeds (typically 400 kHz to 3.4 MHz) and distances to a few meters. Furthermore, in high-noise environments like automotive engines or industrial floors, common-mode noise can easily flip single-ended logic levels.\n\nWhen we need to scale to longer distances, high noise immunity, and multi-master robustness without master-slave dependencies, we must look beyond single-ended voltage sharing to differential, arbitrated networks—leading us to the design of the Controller Area Network (CAN)."
        },
        {
          type: "edgecase",
          id: "i2c-bus-arbitration"
        }
      ]
    }
  ],
  closing: {
    heading: "The Cooperative Bus",
    paragraphs: [
      "I2C stands as a monument to cooperation in hardware. By shifting the selection burden from dedicated copper wires (SPI's CS) to software protocol syntax and open-drain physics, it enables complex inter-chip ecosystems using minimum resources.",
      "It reminds us that communication is not just about driving voltages, but agreeing on when to listen and when to step aside."
    ],
    quote: "On a shared wire, silence is as critical as speech. It is the pull-up resistor that lifts the bus when all devices learn to let go."
  },
  footer: "Reflections on cooperative I2C communication - PrajnaEdge.dev"
},
{
  id: "can-the-language-of-many-voices",
  category: "Interaction",
  series: "System Explorations",
  part: 4,
  title: "CAN: The Language of Many Voices",
  subtitle: "How differential signaling and destructive-free arbitration solved the noise and coordination challenges of multi-master buses.",
  date: "20th June, 2026",
  tags: ["CAN Bus", "Differential Signaling", "Arbitration", "Message RAM", "Hardware Safety"],
  sections: [
    {
      heading: "1. The Single-Ended Voltage Failure",
      content: [
        {
          type: "p",
          text: "In our earlier explorations, we watched systems learn to speak. UART established a simple contract between two nodes. SPI shared a clock to unlock extreme speeds. I2C shared clock and data lines using open-drain logic and addressing, allowing dozens of chips to coexist on a single two-wire bus.\n\nYet, all three protocols share a fatal vulnerability: they are single-ended. They measure logic states by comparing the voltage of a signal line against a common reference: ground. If a signal line is at 3.3V relative to ground, it is a 1; if it is at 0V, it is a 0.\n\nThis architecture works beautifully on a clean PCB. But transport these wires onto a factory floor, an elevator shaft, or a car engine bay, and the physics changes. High-current electric motors, ignition systems, and magnetic fields induce voltage spikes in nearby wires. If electromagnetic interference (EMI) induces a +1.5V spike on the signal line, a 0V logic level is suddenly misread as 1.5V (which can be interpreted as a logic 1). If ground offsets occur between nodes due to long cables, the common ground reference drifts, and nodes lose the ability to interpret each other's voltages. In a noisy world, single-ended coordination collapses."
        }
      ]
    },
    {
      heading: "2. Differential Signaling: Noise Cancellation through Subtraction",
      content: [
        {
          type: "p",
          text: "In 1983, Bosch engineers designing automotive electronics realized that they could not eliminate electrical noise; they had to learn to ignore it. The result was the Controller Area Network (CAN) bus.\n\nTo defeat noise, CAN discards the single-ended model in favor of differential signaling. Instead of one signal line and a ground reference, CAN uses two dedicated lines twisted together: CAN High (CANH) and CAN Low (CANL).\n\nWhen a noise spike hits the twisted-pair cable, the electromagnetic fields affect both wires equally. If a motor induces a +1.0V spike, it shifts both CANH and CANL up by exactly 1.0V. The receiving node does not measure each wire against ground; instead, it measures the voltage difference between them (Vdiff = V_CANH - V_CANL). Because the noise spike is added to both wires, subtraction cancels it out completely:\n\n(V_CANH + V_noise) - (V_CANL + V_noise) = V_CANH - V_CANL\n\nThis simple mathematical physics makes CAN almost completely immune to common-mode noise, allowing it to communicate reliably over hundreds of meters in the most hostile environments."
        },
        {
          type: "image",
          src: "Images/can_network.png",
          alt: "CAN Network Topology showing CANH and CANL twisted pair with nodes and transceivers"
        }
      ]
    },
    {
      heading: "3. Dominant and Recessive: The Wired-AND Evolution",
      content: [
        {
          type: "p",
          text: "How do we transmit data on this differential bus? CAN takes a page from I2C's open-drain playbook but elevates it to a differential drive.\n\nIn I2C, a node either actively pulls the bus LOW or releases it to float HIGH via pull-up resistors. CAN implements a similar philosophy using dominant and recessive states:\n\n1. Recessive State (Logic 1): The transmitter drivers are turned off. Both CANH and CANL float to a nominal 2.5V, driven by terminating resistors. The differential voltage is Vdiff = 2.5V - 2.5V = 0.0V.\n2. Dominant State (Logic 0): The transmitter actively drives the lines apart. CANH is driven high to 3.5V, and CANL is driven low to 1.5V. The differential voltage is Vdiff = 3.5V - 1.5V = 2.0V.\n\nBecause the dominant state actively drives the lines while the recessive state passively lets them float, a dominant bit (0) will always override a recessive bit (1). If one node attempts to write a recessive 1, but another node writes a dominant 0, the bus resolves to a dominant 0. This dominant/recessive physics forms the basis of CAN's collision-free, multi-master arbitration."
        },
        {
          type: "image",
          src: "Images/can_differential.png",
          alt: "Differential Voltage Levels: Dominant vs Recessive on CANH and CANL"
        }
      ]
    },
    {
      heading: "4. The Physics of the 120 Ohm Terminator",
      content: [
        {
          type: "p",
          text: "Look at any CAN network, and you will find a 120 Ohm resistor at each extreme end of the bus, bridging CANH and CANL. These are not simple pull-up resistors; they are transmission line terminators.\n\nAt high speeds, electrical signals behave like waves in water. When a voltage transition travels down a wire, it carries electrical energy. If it hits the open end of a cable, it encounters a boundary mismatch: the energy has nowhere to go, so it reflects back down the wire in the opposite direction. These reflected waves bounce back and forth, colliding with new incoming bits and corrupting the waveform.\n\nTo prevent signal reflections, we must match the cable's characteristic impedance. A standard twisted-pair cable has a characteristic impedance of 120 Ohms. Placing 120 Ohm resistors at both ends acts as an electrical sink: the incoming wave's energy is completely absorbed and converted to heat, preventing any reflections and maintaining pristine signal integrity."
        },
        {
          type: "image",
          src: "Images/can_termination.png",
          alt: "CAN Bus Termination: Impedance Matching vs Signal Reflections"
        }
      ]
    },
    {
      heading: "5. Bit Arbitration: The Conversation of Dominance",
      content: [
        {
          type: "p",
          text: "In SPI, a master dictates timing and selection. In I2C, a master addresses slaves. But CAN is a peer-to-peer network: there are no masters or slaves, only nodes. Any node can transmit whenever the bus is idle.\n\nWhat happens when three nodes start transmitting at the exact same microsecond? In Ethernet, this causes a collision; the nodes stop, wait a random interval, and try again, wasting bandwidth. CAN solves this using bitwise arbitration.\n\nEvery CAN frame begins with an Identifier (ID), which serves two purposes: it defines the priority of the message and labels the data content. When multiple nodes start transmitting, they write their ID bits onto the bus one bit at a time while simultaneously reading the state of the bus.\n\nIf Node A writes a recessive 1, but Node B writes a dominant 0, the bus becomes dominant. When Node A reads the bus, it notices the mismatch: it wrote a 1, but it sees a 0. Knowing that another node with a higher priority (a lower numerical ID) is transmitting, Node A immediately falls silent, dropping out of arbitration. Node B continues uninterrupted. This arbitration is completely non-destructive: the winning message is delivered without a single bit of corruption."
        },
        {
          type: "edgecase",
          id: "can-conversation-of-dominance"
        }
      ]
    },
    {
      heading: "6. Frame Architectures: CAN 2.0A vs CAN 2.0B",
      content: [
        {
          type: "p",
          text: "As networks grew, the original 11-bit identifier space (CAN 2.0A) proved too small for complex systems. To expand this, engineers introduced the Extended CAN frame (CAN 2.0B).\n\n1. Standard Frame (CAN 2.0A): Uses an 11-bit identifier, allowing up to 2,048 unique message priorities. It is the core format for basic automotive and industrial networks.\n2. Extended Frame (CAN 2.0B): Uses a 29-bit identifier, expanding the space to over 536 million unique priorities. This is achieved by splitting the ID into an 11-bit Base ID and an 18-bit Extension ID, separated by the IDE (Identifier Extension) and SRR (Substitute Remote Request) bits. If a standard and an extended frame with the same base ID compete, the standard frame wins arbitration because its IDE bit is dominant (logic 0), whereas the extended frame's IDE bit is recessive (logic 1)."
        },
        {
          type: "image",
          src: "Images/can_frame_format.png",
          alt: "CAN 2.0A Standard vs CAN 2.0B Extended Frame Layouts"
        }
      ]
    },
    {
      heading: "7. The Safety Layer: Stuffing, CRC, and ACK",
      content: [
        {
          type: "p",
          text: "Because CAN has no shared clock line (like SPI or I2C), nodes must synchronize their clocks using the transitions (edges) of the incoming data bits. If a message contains a long sequence of identical bits—for example, a data payload of 0x00 (all 0s)—the line remains flat, and the nodes' clocks drift out of sync.\n\nTo maintain synchronization, CAN uses bit stuffing. If the controller detects five consecutive bits of the same polarity, it automatically inserts an opposite 'stuff bit' into the stream. The receiving controller detects these stuff bits and strips them out before delivering the data, ensuring the receiver's phase-locked loop (PLL) stays locked to the transmitter.\n\nAdditionally, CAN includes robust integrity checks. The transmitter appends a 15-bit Cyclic Redundancy Check (CRC) checksum. After the CRC comes the Acknowledge (ACK) slot. During the ACK bit, the transmitter writes a recessive 1. Every receiver that successfully validated the frame overrides this slot by writing a dominant 0. If the transmitter reads a 0 in the ACK slot, it knows at least one node received the frame correctly. If it reads a 1, it assumes a transmission error and retransmits the message."
        }
      ]
    },
    {
      heading: "8. Message RAM: The Hidden Geography of Firmware",
      content: [
        {
          type: "p",
          html: true,
          text: "In our earlier journey through <a onclick=\"openItem('the-hidden-geography-of-firmware', 'blogs')\" style=\"color:var(--blue); cursor:pointer; text-decoration:underline;\">The Hidden Geography of Firmware</a>, we saw that SRAM is not a uniform block of memory. It is divided into distinct regions, and modern microcontrollers often allocate specific, hardware-accessible partitions for peripheral data. CAN controllers are a prime example.\n\nIn high-performance microcontrollers (such as the STM32H7 or microcontrollers containing Bosch's M_CAN IP), CAN frames are not handled directly in general-purpose CPU registers. Instead, they are written to and read from a dedicated region of memory called Message RAM.\n\nThis Message RAM contains the configuration for receive and transmit buffers, filters, and FIFO queues. Because the CAN peripheral's hardware controller reads and writes to this RAM region directly via DMA (Direct Memory Access), the firmware developer must carefully define the start address and offsets of these buffers in linker scripts or configuration registers. A misalignment of a single word in the Message RAM boundary causes the CAN hardware to generate a bus fault or corrupt frame routing. To write robust CAN drivers, you must understand the exact physical layout of your microcontroller's memory map."
        },
        {
          type: "edgecase",
          id: "can-journey-of-a-frame"
        }
      ]
    }
  ],
  closing: {
    heading: "The Cooperative Network",
    paragraphs: [
      "CAN represents the pinnacle of cooperative embedded networking. By replacing central master control with distributed, non-destructive bit arbitration and robust differential physics, it creates a system where nodes can converse reliably in the presence of noise that would disable any other protocol.",
      "It reminds us that robust communication does not require silence from others; it requires a physical layer that allows voices to merge and resolve their differences without corruption."
    ],
    quote: "When machines speak in many voices, harmony is not achieved by force, but by a physical agreement on who steps aside."
  },
  footer: "Reflections on differential CAN bus communication - PrajnaEdge.dev"
},
{
  id: "the-roads-not-often-travelled",
  category: "Interaction",
  series: "System Explorations",
  part: 5,
  title: "The Roads Not Often Travelled",
  subtitle: "How constraints, cost, and physical boundaries spawned the specialized cousins of UART, SPI, I2C, and CAN.",
  date: "21st June, 2026",
  tags: ["USART", "QSPI", "SMBus", "LIN", "One-Wire", "Serial Protocols"],
  sections: [
    {
      heading: "1. USART: The Synchronous Bridge",
      content: [
        {
          type: "p",
          text: "In our exploration of UART, we discovered that asynchronous communication is a delicate timing contract. Without a shared clock wire, nodes must rely on internal oscillators, oversampling clocks, and framing bits (Start/Stop) to synchronize. This contract is simple but costly: clock drift limits speeds, and framing adds a 20% protocol overhead on every byte.\n\nBut what if we added a clock line back to UART? That hybrid is the Universal Synchronous Asynchronous Receiver Transmitter (USART).\n\nWhen configured in synchronous mode, USART transmits a dedicated clock signal alongside the data line. Instead of oversampling and searching for start bits, the receiver simply samples the data wire on the clock edges. This eliminates clock drift issues, allowing speeds comparable to SPI while retaining UART's simple frame packaging. Yet, despite being present on almost every modern microcontroller, synchronous USART is rarely used. If an engineer is willing to route a clock line, the simplicity of UART is lost; and if they have a clock line, they almost always prefer the faster shift register architecture of SPI or the multi-slave addressing of I2C. USART remains a bridge not often crossed, operating quietly in asynchronous UART mode on most developer desks."
        },
        {
          type: "image",
          src: "Images/usart_timing.png",
          alt: "USART Timing Diagram showing Synchronous Clock CK and Data TX Alignment vs Asynchronous UART"
        }
      ]
    },
    {
      heading: "2. QSPI: SPI on Steroids",
      content: [
        {
          type: "p",
          text: "SPI achieved extreme throughput by sharing a clock, but it remained limited by its physical architecture: a single MOSI (Master Out Slave In) and MISO (Master In Slave Out) line. As microcontrollers shrank, board designers began moving flash memory outside the MCU package to external chips. This created a critical bottleneck: loading bootloader code and assets over a single MOSI/MISO line was too slow, stalling system startup.\n\nThe solution was Quad SPI (QSPI). Instead of keeping data lines unidirectional, QSPI converts MOSI, MISO, and two additional pins into four bidirectional data channels (IO0 through IO3). In a single clock cycle, the controller reads or writes four bits of data instead of one.\n\nBy leveraging this quad-width bus and Dual Data Rate (DDR) clocking—sampling on both rising and falling edges—QSPI increases throughput up to eightfold. This massive bandwidth allows modern microcontrollers to execute code directly from external flash memory (Execute-in-Place, or XiP), making external memory feel as responsive as internal SRAM."
        },
        {
          type: "image",
          src: "Images/qspi_vs_spi.png",
          alt: "Standard SPI (4 wires) vs Quad SPI (6 wires showing IO0-IO3 bidirectional lines)"
        }
      ]
    },
    {
      heading: "3. SMBus: Stricter Rules for a Shared Conversation",
      content: [
        {
          type: "p",
          text: "I2C gave us a clean, shared bus using open-drain logic and software addressing. But I2C's flexibility was also its weakness. It lacked strict timeouts, standardized voltage thresholds, and error checking. If a slave device crashed or held SCL low (clock stretching) to process data, the entire bus could freeze indefinitely. On a PC motherboard, a single hanging temperature sensor could lock up the system.\n\nTo address this, Intel defined the System Management Bus (SMBus) in 1995. SMBus is electrically compatible with I2C but enforces a strict set of rules:\n\n1. Bus Timeout: If SCL is held low for more than 35ms, all devices must reset their internal interface controllers and release the bus, preventing permanent lockups.\n2. Packet Error Checking (PEC): Appends a Cyclic Redundancy Check (CRC-8) byte to ensure data integrity, critical for battery charging controllers.\n3. SMBALERT# Line: Adds an optional interrupt wire, allowing slave devices to notify the master of events (like battery over-temperature) immediately, avoiding the need for continuous polling.\n\nSMBus turned the cooperative conversation of I2C into a reliable, deterministic diagnostic bus for power management."
        },
        {
          type: "image",
          src: "Images/smbus_topology.png",
          alt: "SMBus Topology showing pull-ups, SCL, SDA, and the SMBALERT# alert line"
        }
      ]
    },
    {
      heading: "4. LIN: The Economical Sub-Bus",
      content: [
        {
          type: "p",
          text: "CAN bus solved the problem of high-noise automotive environments using differential signaling and bitwise arbitration. But this reliability came with a high cost: CAN requires a dedicated controller IP, a transceiver chip, and two twisted copper wires. Putting a CAN node in every car door, side mirror, seat motor, and window lifter would drive up vehicle costs and weight.\n\nThis economic constraint gave birth to the Local Interconnect Network (LIN) bus.\n\nLIN is a single-wire, master-slave sub-bus. It operates at low speeds (up to 20 kbps) using standard, low-cost UART frames. It runs on a single wire pulled up to 12V (battery voltage), eliminating the need for differential transceivers. Instead of complex CAN controllers, LIN runs on cheap 8-bit microcontrollers. In a car, a single CAN-enabled body controller acts as the LIN Master, managing a cluster of LIN slaves (doors, locks, mirrors) and bridging their diagnostic info back to the primary CAN backbone, saving copper, weight, and silicon cost."
        },
        {
          type: "image",
          src: "Images/lin_network.png",
          alt: "LIN single-wire network topology with Master node, slave modules, and 12V pull-up"
        }
      ]
    },
    {
      heading: "5. One-Wire: Minimalism in Copper",
      content: [
        {
          type: "p",
          text: "If LIN reduced the bus to a single wire plus power and ground, Dallas Semiconductor's 1-Wire protocol went even further. It reduced the entire bus—power, clock, and data—to a single copper conductor (DQ) and a ground return.\n\n1-Wire devices use parasitic power. Inside each slave device is a small capacitor. When the master lets the DQ line float HIGH, the slave harvests energy from the wire to charge its capacitor. When the master pulls the line LOW to transmit data, the slave runs off the stored capacitor charge.\n\nWith no clock wire, timing is critical. Communication is divided into precise time slots (e.g. 15µs to 60µs) where master and slave pull the line low for varying durations to represent 0s and 1s. Every 1-Wire device is factory-programmed with a unique, immutable 64-bit registration ID. This allows a master to communicate with dozens of sensors (like the DS18B20 digital thermometer) sharing the same single wire run, with zero manual address configuration. 1-Wire represents the ultimate realization of hardware minimalism."
        },
        {
          type: "image",
          src: "Images/onewire_bus.png",
          alt: "1-Wire bus topology showing master, parasitic power slaves, DQ wire, and pull-up"
        }
      ]
    },
    {
      heading: "6. Summary and Comparison",
      content: [
        {
          type: "p",
          text: "The history of embedded communication was never a straight line. UART, SPI, I²C, and CAN became the major highways of the interaction layer because they solved the most common problems. Yet engineers continually carved smaller paths whenever unique constraints appeared.\n\nSome of these protocols remained specialized niches; others became industry standards. All of them remind us that embedded engineering evolves through physical and economic constraints rather than the pursuit of theoretical perfection."
        },
        {
          type: "p",
          html: true,
          text: '<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:1.0rem;color:#FFF;margin-bottom:0.75rem;">Core Communication Protocols</div>\n<table class="blog-table">\n  <thead>\n    <tr>\n      <th>Protocol</th>\n      <th>Style</th>\n      <th>Typical Speed</th>\n      <th>Topology</th>\n      <th>Strength</th>\n      <th>Common Use</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td><strong>UART</strong></td>\n      <td>Asynchronous, Full-Duplex</td>\n      <td>9.6 - 115.2 kbps</td>\n      <td>Point-to-Point (2 wires)</td>\n      <td>Simple, no clock line needed</td>\n      <td>Debug logs, simple telemetry</td>\n    </tr>\n    <tr>\n      <td><strong>SPI</strong></td>\n      <td>Synchronous, Full-Duplex</td>\n      <td>10 - 50+ Mbps</td>\n      <td>Master-Slave (4+ wires)</td>\n      <td>Extreme throughput, simple hardware</td>\n      <td>SD cards, displays, fast sensors</td>\n    </tr>\n    <tr>\n      <td><strong>I²C</strong></td>\n      <td>Synchronous, Half-Duplex</td>\n      <td>100 - 400 kbps</td>\n      <td>Shared Bus (2 wires)</td>\n      <td>Low pin count, hardware addressing</td>\n      <td>EEPROMs, onboard sensors</td>\n    </tr>\n    <tr>\n      <td><strong>CAN</strong></td>\n      <td>Asynchronous, Half-Duplex</td>\n      <td>125 kbps - 1 Mbps</td>\n      <td>Shared Bus (2 wires)</td>\n      <td>Noise immunity, arbitration</td>\n      <td>Automotive, industrial control</td>\n    </tr>\n  </tbody>\n</table>'
        },
        {
          type: "p",
          html: true,
          text: '<div style="font-family:\'Syne\',sans-serif;font-weight:700;font-size:1.0rem;color:#FFF;margin-bottom:0.75rem;margin-top:1.5rem;">Unexpected Cousins</div>\n<table class="blog-table">\n  <thead>\n    <tr>\n      <th>Protocol</th>\n      <th>Parent Protocol</th>\n      <th>Why It Exists (Constraint)</th>\n      <th>Typical Use</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td><strong>USART</strong></td>\n      <td>UART</td>\n      <td>Adds synchronous clock line to eliminate clock drift at high speed</td>\n      <td>High-speed serial links, synchronous peripherals</td>\n    </tr>\n    <tr>\n      <td><strong>QSPI</strong></td>\n      <td>SPI</td>\n      <td>Repurposes pins into 4 bidirectional channels to increase flash throughput</td>\n      <td>Booting from external flash (Execute-in-Place)</td>\n    </tr>\n    <tr>\n      <td><strong>SMBus</strong></td>\n      <td>I²C</td>\n      <td>Enforces strict timeouts (35ms) and alert line to prevent bus lockups</td>\n      <td>Smart battery packs, PC motherboard system health</td>\n    </tr>\n    <tr>\n      <td><strong>LIN</strong></td>\n      <td>CAN</td>\n      <td>Sub-bus reducing cost using single-wire 12V and basic UART logic</td>\n      <td>Car mirrors, windows, door lock body modules</td>\n    </tr>\n    <tr>\n      <td><strong>One-Wire</strong></td>\n      <td>Custom</td>\n      <td>Ultimate pin reduction, merging data and power on a single wire</td>\n      <td>Temperature sensor networks (DS18B20), electronic keys</td>\n    </tr>\n  </tbody>\n</table>'
        }
      ]
    }
  ],
  closing: {
    heading: "The Evolution of Constraint",
    paragraphs: [
      "Every protocol we study is a snapshot of a compromise made under a specific set of physical, financial, and temporal boundaries.",
      "As systems developers, our task is not to find a single perfect protocol, but to understand which compromise aligns best with the constraints of the world we are building."
    ],
    quote: "Engineering does not look for perfect answers. It builds paths through constraints."
  },
  footer: "Reflections on specialized protocols and constraints - PrajnaEdge.dev"
},
{
  id: "the-architecture-of-time",
  category: "Coordination",
  series: "System Explorations",
  part: 1,
  title: "The Architecture of Time",
  subtitle: "How machines learned to measure cycles, divide frequencies, and keep promises.",
  date: "21st June, 2026",
  tags: ["Timers", "Prescalers", "PWM", "Compare Match", "Input Capture", "Real-Time Systems"],
  sections: [
    {
      heading: "1. The Illusion of Speed",
      content: [
        {
          type: "p",
          text: "In our earlier explorations, we watched systems learn to speak. UART established timing contracts, SPI synchronized clocks, and I2C/CAN introduced bus sharing. Yet, all communication protocols and computational structures share an underlying assumption: they assume the existence of structured, reliable time.\n\nHow does software wait? The most naive approach is a busy-wait delay loop:\n\n`for(volatile int i = 0; i < 100000; i++);`\n\nThis simple loop runs on a test bench, but collapses in a real-world system. First, it is entirely clock-frequency dependent: if the microcontroller switches from an 8 MHz internal RC oscillator to a 168 MHz external crystal, the delay shrinks to a fraction of its intended duration. Second, if you enable compiler optimizations (such as `-O3`), the compiler may strip the empty loop entirely. Third, if an interrupt service routine (ISR) fires during the loop, the CPU suspends execution to handle the event, stretching the delay unpredictably. Software alone cannot keep temporal promises."
        }
      ]
    },
    {
      heading: "2. The Hardware Counter",
      content: [
        {
          type: "p",
          text: "To keep time reliably, the CPU must delegate the task to dedicated hardware: the timer. At its simplest, a timer is an independent hardware block consisting of a clock oscillator feeding a digital register called the Counter (CNT).\n\nOn every tick of the clock, the counter register increments. Because this incrementing happens in hardware, it is completely independent of CPU execution. The CPU can be performing complex arithmetic, waiting for an interrupt, or even resting in a low-power sleep state; the hardware counter increments steadily in the background, counting clock cycles to track elapsed time."
        }
      ]
    },
    {
      heading: "3. Prescalers: Division of Labor",
      content: [
        {
          type: "p",
          text: "Directly clocking the counter register quickly reveals a physical limitation: frequency. Suppose our microcontroller runs at 84 MHz, and we use a 16-bit counter register (which can hold values from 0 to 65,535).\n\nAt 84 million ticks per second, the counter will fill up and wrap back to zero in just 780 microseconds. Measuring a simple 1-second interval would require tracking thousands of wraps in software, consuming CPU cycles and defeating the purpose of hardware timing.\n\nTo solve this, timers use a Prescaler (PSC). The prescaler is a programmable frequency divider. If we set the prescaler to 8399, the incoming 84 MHz clock is divided by 8400 (PSC + 1), feeding the counter a slow, manageable 10 kHz signal. The counter now increments once every 100 microseconds, wrapping in a comfortable 6.5 seconds."
        },
        {
          type: "image",
          src: "Images/timer_prescaler.png",
          alt: "Timer Clock Division: Clock source divided by Prescaler to drive Counter CNT"
        }
      ]
    },
    {
      heading: "4. Overflow: The Heartbeat of wrapping",
      content: [
        {
          type: "p",
          text: "When the counter register counts past its maximum value (or a configured Auto-Reload Register / ARR value), it wraps back to zero. This wraparound is called an Overflow.\n\nThe moment an overflow occurs, the timer hardware asserts an Update Interrupt Flag (UIF) and can trigger a CPU interrupt. By adjusting the ARR value, we dictate the exact period of this wraparound. A 10 kHz counter configured to wrap at 10,000 generates an overflow interrupt exactly once every second, creating a deterministic periodic heartbeat."
        },
        {
          type: "image",
          src: "Images/timer_overflow.png",
          alt: "Timer Overflow Sequence showing Counter wrapping at ARR and generating Update Flag"
        }
      ]
    },
    {
      heading: "5. Compare Match: Keeping Promises",
      content: [
        {
          type: "p",
          text: "Periodic overflows are useful, but what if we need events to happen *during* the count cycle? That is where the Compare Register (CCR) comes in.\n\nThe CPU writes a target value to the CCR. The timer's hardware comparator continuously checks: `Is CNT == CCR?`.\n\nThe moment the counter matches the compare register, the timer asserts a Compare Match flag and can toggle an output pin or trigger an event. This allows the system to schedule precise sub-millisecond events without CPU intervention."
        },
        {
          type: "image",
          src: "Images/timer_compare_match.png",
          alt: "Timer Compare Match Waveform showing Counter intersecting CCR to trigger Match Events"
        }
      ]
    },
    {
      heading: "6. Timer Configurator: The Race Against Time",
      content: [
        {
          type: "p",
          text: "Let's experiment with these core concepts. In the simulator below, configure the clock source, prescaler division, counter size, and compare match values to see how physical frequencies translate into structured temporal events."
        },
        {
          type: "edgecase",
          id: "timer-builder"
        }
      ]
    },
    {
      heading: "7. Pulse Width Modulation: Painting with Time",
      content: [
        {
          type: "p",
          text: "Compare match logic unlocks a powerful technique: Pulse Width Modulation (PWM). If we configure a timer pin to go HIGH on counter reset (0) and go LOW when the counter matches the Compare Value (CCR), we generate a repeating digital pulse train.\n\nBy changing the compare value, we adjust the Duty Cycle—the percentage of the period that the signal is HIGH. By toggling this signal at high frequencies, we can simulate an analog voltage.\n\nA 50% duty cycle on a 3.3V pin outputs 3.3V half the time, averaging to 1.65V. To an LED, this appears as half brightness. To a DC motor, it translates to half speed. Timers allow us to paint analog behaviors onto digital silicon using nothing but time."
        },
        {
          type: "image",
          src: "Images/pwm_waveforms.png",
          alt: "PWM Waveform showing Period, Pulse Width, and Amplitude"
        },
        {
          type: "image",
          src: "Images/pwm_duty_cycle.png",
          alt: "Comparison of 25%, 50%, and 75% Duty Cycles and resulting average voltages"
        }
      ]
    },
    {
      heading: "8. PWM Simulator: Painting with Time",
      content: [
        {
          type: "p",
          text: "Adjust the frequency and duty cycle below to see how pulse widths map directly to average output voltages, controlling LED intensity and motor velocity."
        },
        {
          type: "edgecase",
          id: "pwm-painter"
        }
      ]
    },
    {
      heading: "9. Input Capture: Measuring the World",
      content: [
        {
          type: "p",
          text: "Timers do not just generate waveforms; they can also measure them. This is the role of Input Capture.\n\nInstead of the counter triggering changes on an external pin, external pin transitions (edges) trigger the timer. When a rising edge is detected on an input capture pin, the hardware instantly copies (captures) the current counter value (CNT) into the capture register (CCR). When the falling edge arrives, it captures the value again.\n\nBy subtracting the first captured value from the second, the software can measure the exact pulse width of an external signal down to the nanosecond, enabling precise sensor decoding (such as ultrasonic distance sensors or RPM tachometers) with zero CPU polling overhead."
        },
        {
          type: "image",
          src: "Images/input_capture.png",
          alt: "Timer Input Capture timing showing CCR latching at rising/falling edges to measure width"
        }
      ]
    }
  ],
  closing: {
    heading: "The Foundation of Decision",
    paragraphs: [
      "Communication protocols taught machines how to exchange information. Time taught machines how to coordinate action.",
      "Before a system can observe the world, react to events, or schedule complex work, it must first learn how to measure time itself. With a structured heartbeat established, we can begin exploring how multiple activities are coordinated on a single CPU core."
    ],
    quote: "Time is the canvas upon which coordination is painted. Without a clock, a machine is merely reactive; with one, it becomes purposeful."
  },
  footer: "Reflections on timing architectures and hardware counters - PrajnaEdge.dev"
},
{
  id: "when-machines-learned-to-observe",
  category: "Coordination",
  title: "When Machines Learned to Observe",
  subtitle: "How reality became numbers.",
  date: "21st June, 2026",
  tags: ["ADC", "Sampling", "Quantization", "Resolution", "Hardware Pipeline"],
  sections: [
    {
      heading: "1. The Analog World",
      content: [
        {
          type: "p",
          text: "The physical world is fluid, continuous, and unbroken. If you measure the temperature of a room, it does not jump instantly from 22°C to 23°C; it transitions through an infinite number of intermediate states. The pressure of sound waves hitting a microphone, the changing angle of a steering wheel potentiometer, the terminal voltage of a discharging lithium-ion battery, and the intensity of morning light are all continuous. They exist as physical quantities that can take any value within a range, changing smoothly across time."
        },
        {
          type: "image",
          src: "Images/analog_signals.png",
          alt: "Continuous physical waveforms vs discrete computer states"
        }
      ]
    },
    {
      heading: "2. Why Computers Cannot Directly Understand Analog Signals",
      content: [
        {
          type: "p",
          text: "A digital processor, by contrast, is a machine of absolute division. Inside its silicon core, electricity is gated into binary states: a transistor is either fully conducting or cut off, representing a logical 1 or 0. A processor cannot store 'a slightly warm voltage' or 'a loud sound wave' in its registers. It understands only precise digital numbers. To bridge this gap between continuous physical reality and discrete computation, the system needs an interface that translates raw, infinitely variable analog signals into finite, structured digital words. This interface is the Analog-to-Digital Converter (ADC)."
        }
      ]
    },
    {
      heading: "3. Sampling: Freezing Time",
      content: [
        {
          type: "p",
          text: "The first step of this translation is Sampling. Since a computer cannot observe the world constantly, it must observe it at discrete moments. Sampling is the process of reading the analog voltage of a signal at precise, regular intervals.\n\nThis is where we connect back to the Hardware Timer. A timer serves as the clock heartbeat of the system, asserting trigger events to dictate exactly *when* the ADC should observe. By sampling at a fast enough rate, the machine captures enough snapshots of the signal to represent its behavior across time."
        },
        {
          type: "image",
          src: "Images/sampling_process.png",
          alt: "Sampling timing trace showing periodic capture ticks"
        }
      ]
    },
    {
      heading: "4. Quantization: Slicing the Continuous",
      content: [
        {
          type: "p",
          text: "Freezing time via sampling is only half the battle. At each sampling moment, the voltage level is still a continuous value with infinite decimal possibilities. A computer has a finite number of bits to represent this value, so it must map this infinite voltage to the nearest level on a pre-defined digital staircase. This mapping process is called Quantization.\n\nQuantization discards the infinite sub-millivolt details, rounding the physical voltage to the closest discrete step. The tiny difference between the true analog voltage and the rounded digital level is called Quantization Error."
        },
        {
          type: "image",
          src: "Images/quantization_steps.png",
          alt: "Continuous signal mapped onto discrete binary quantization levels"
        }
      ]
    },
    {
      heading: "5. Resolution: The Fineness of the Mesh",
      content: [
        {
          type: "p",
          text: "How close can our digital staircase approximate reality? That depends on the ADC's Resolution. Resolution refers to the number of binary bits the converter uses to represent the signal, which dictates the number of steps on our measurement staircase.\n\n- A **3-bit ADC** has only $2^3 = 8$ steps. The staircase is coarse, jagged, and introduces substantial quantization noise.\n- An **8-bit ADC** provides $2^8 = 256$ steps, which is sufficient for basic sensing but still relatively coarse.\n- A **12-bit ADC** provides $2^{12} = 4096$ steps, offering a fine mesh that captures small changes with minimal noise.\n- A **16-bit ADC** offers $2^{16} = 65,536$ steps, resolving microvolt fluctuations for high-fidelity audio or medical instrumentation.\n\nBy increasing resolution, we make the grid mesh finer, allowing the machine to capture a closer approximation of the physical wave."
        },
        {
          type: "image",
          src: "Images/resolution_comparison.png",
          alt: "Comparison of grid density for 3-bit vs 8-bit resolutions"
        }
      ]
    },
    {
      heading: "6. Reference Voltage: The Calibration Ruler",
      content: [
        {
          type: "p",
          text: "To assign digital numbers to analog voltages, the ADC needs a ruler. This ruler is the Reference Voltage ($V_{REF}$). The reference voltage defines the maximum physical voltage the ADC can measure, which corresponds to the maximum digital count.\n\nIf we have a 12-bit ADC (0 to 4095) with a $V_{REF}$ of 3.3V:\n- An input of 0.0V resolves to `0`.\n- An input of 3.3V resolves to `4095`.\n- An input of 1.65V resolves to exactly `2048`.\n\nIf the reference voltage fluctuates, our measurements fluctuate too. If $V_{REF}$ drops to 3.0V due to poor power supply regulation, an input of 1.5V will resolve to `2048` instead of `1861`, causing a measurement error. Precise calibration of $V_{REF}$ is the cornerstone of accurate physical observation."
        },
        {
          type: "image",
          src: "Images/reference_voltage.png",
          alt: "Reference voltage acting as a calibrated measuring scale"
        }
      ]
    },
    {
      heading: "7. The Conversion Pipeline: Sample, Hold, Convert, Store",
      content: [
        {
          type: "p",
          text: "How does the physical conversion happen? Most microcontrollers use a Successive Approximation Register (SAR) ADC. The hardware processes each sample through a four-stage pipeline:\n\n1. **Sample**: A physical switch closes briefly, connecting the external pin to an internal capacitor.\n2. **Hold**: The switch opens. The capacitor 'holds' the captured charge steady so the voltage doesn't change during conversion.\n3. **Convert**: A comparator compares the held voltage to a series of voltages generated by an internal DAC. Using a binary search (Successive Approximation), it tests the most significant bit first, deciding whether the signal is above or below half of $V_{REF}$, and repeats for each bit down to the LSB.\n4. **Store**: Once all bits are decided, the binary result is copied to a data register, raising an interrupt or DMA request so the CPU can read it."
        },
        {
          type: "image",
          src: "Images/adc_pipeline.png",
          alt: "SAR ADC hardware blocks: Sample switch, Hold capacitor, Comparator, and SAR register"
        }
      ]
    },
    {
      heading: "8. Accuracy vs Precision",
      content: [
        {
          type: "p",
          text: "In embedded sensing, engineers often confuse two critical terms: Accuracy and Precision. They are not the same.\n\n- **Accuracy** is how close a measurement is to the true physical value. An accurate system has minimal calibration offset.\n- **Precision** is how consistent and repeatable the measurements are when the same input is read multiple times. A precise system has low noise.\n\nA system can be highly precise but inaccurate (giving highly repeatable, low-noise readings that are calibrated incorrectly) or highly accurate but imprecise (averaging to the correct value but showing substantial noise on each individual sample). Below is a visual representation of these states:"
        },
        {
          type: "html",
          html: `<div style="background:#0F172A; padding:1.25rem; border:1px solid var(--border); border-radius:8px; display:flex; justify-content:center; align-items:center; margin:1.5rem 0;">
            <svg width="640" height="170" viewBox="0 0 640 170" style="background:transparent; overflow:visible; width:100%; max-width:640px;">
              <!-- 1. Low Accuracy, Low Precision -->
              <g transform="translate(70, 75)">
                <circle cx="0" cy="0" r="45" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="2"/>
                <circle cx="0" cy="0" r="30" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1.5"/>
                <circle cx="0" cy="0" r="15" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1"/>
                <circle cx="0" cy="0" r="2" fill="var(--blue)"/>
                <circle cx="-25" cy="-20" r="3" fill="#EF6868"/>
                <circle cx="15" cy="-35" r="3" fill="#EF6868"/>
                <circle cx="-10" cy="30" r="3" fill="#EF6868"/>
                <circle cx="35" cy="20" r="3" fill="#EF6868"/>
                <circle cx="-30" cy="15" r="3" fill="#EF6868"/>
                <text x="0" y="65" fill="var(--muted)" font-family="var(--mono)" font-size="0.65rem" text-anchor="middle">Imprecise & Inaccurate</text>
              </g>
              <!-- 2. Low Accuracy, High Precision -->
              <g transform="translate(230, 75)">
                <circle cx="0" cy="0" r="45" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="2"/>
                <circle cx="0" cy="0" r="30" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1.5"/>
                <circle cx="0" cy="0" r="15" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1"/>
                <circle cx="0" cy="0" r="2" fill="var(--blue)"/>
                <circle cx="-25" cy="-25" r="3" fill="#EF6868"/>
                <circle cx="-27" cy="-22" r="3" fill="#EF6868"/>
                <circle cx="-23" cy="-26" r="3" fill="#EF6868"/>
                <circle cx="-26" cy="-28" r="3" fill="#EF6868"/>
                <circle cx="-22" cy="-21" r="3" fill="#EF6868"/>
                <text x="0" y="65" fill="var(--muted)" font-family="var(--mono)" font-size="0.65rem" text-anchor="middle">Precise & Inaccurate</text>
              </g>
              <!-- 3. High Accuracy, Low Precision -->
              <g transform="translate(390, 75)">
                <circle cx="0" cy="0" r="45" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="2"/>
                <circle cx="0" cy="0" r="30" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1.5"/>
                <circle cx="0" cy="0" r="15" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1"/>
                <circle cx="0" cy="0" r="2" fill="var(--blue)"/>
                <circle cx="-12" cy="-10" r="3" fill="#10B981"/>
                <circle cx="10" cy="-8" r="3" fill="#10B981"/>
                <circle cx="-5" cy="12" r="3" fill="#10B981"/>
                <circle cx="14" cy="10" r="3" fill="#10B981"/>
                <circle cx="2" cy="-14" r="3" fill="#10B981"/>
                <text x="0" y="65" fill="var(--muted)" font-family="var(--mono)" font-size="0.65rem" text-anchor="middle">Imprecise & Accurate</text>
              </g>
              <!-- 4. High Accuracy, High Precision -->
              <g transform="translate(550, 75)">
                <circle cx="0" cy="0" r="45" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="2"/>
                <circle cx="0" cy="0" r="30" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1.5"/>
                <circle cx="0" cy="0" r="15" fill="none" stroke="rgba(148,163,184,0.12)" stroke-width="1"/>
                <circle cx="0" cy="0" r="2" fill="var(--blue)"/>
                <circle cx="0" cy="0" r="3" fill="#10B981"/>
                <circle cx="-2" cy="1" r="3" fill="#10B981"/>
                <circle cx="1" cy="-2" r="3" fill="#10B981"/>
                <circle cx="2" cy="2" r="3" fill="#10B981"/>
                <circle cx="-1" cy="-1" r="3" fill="#10B981"/>
                <text x="0" y="65" fill="var(--muted)" font-family="var(--mono)" font-size="0.65rem" text-anchor="middle">Precise & Accurate</text>
              </g>
            </svg>
          </div>`
        }
      ]
    },
    {
      heading: "9. Capturing Reality",
      content: [
        {
          type: "p",
          text: "Let's observe these conversion behaviors. In the interactive panel below, modify signal frequency, resolution, and sampling rate to watch how an analog signal is sliced and rounded into digital numbers."
        },
        {
          type: "edgecase",
          id: "capturing-reality"
        }
      ]
    },
    {
      heading: "10. The Cost of Observation",
      content: [
        {
          type: "p",
          text: "What happens when our observation parameters are configured incorrectly? In the simulator below, adjust the reference voltage, resolution, and sample rate to induce signal clipping, aliasing (undersampling), or high quantization stepping."
        },
        {
          type: "edgecase",
          id: "cost-of-observation"
        }
      ]
    },
    {
      heading: "11. Real Embedded Applications",
      content: [
        {
          type: "p",
          text: "ADCs are the sensory organs of embedded silicon. They monitor the health of battery cells in electric vehicles, translate analog temperature sensors (like thermistors or RTDs) into precise degrees, decode phase currents for brushless DC motor control, digitize microphone voice data in smart assistants, and capture cardiac electrical potentials in medical ECG monitors. Without the ADC, a processor is deaf, blind, and isolated from physical reality."
        }
      ]
    }
  ],
  closing: {
    heading: "The Sensory Handshake",
    paragraphs: [
      "Timers taught machines when to pay attention. ADCs taught machines how to translate reality into something computation could understand.",
      "Yet observing reality is only half the story. Once a machine has observed its environment and decided on a course of action, it must eventually speak back—driving physical outputs and painting analog actions onto the physical world."
    ],
    quote: "A processor without an ADC is a brain without senses—trapped in a silent chamber of its own logical abstractions."
  },
  footer: "Reflections on analog interfaces and ADC conversions - PrajnaEdge.dev"
},
{
  id: "when-machines-learned-to-speak-back",
  category: "Coordination",
  series: "The Architecture of Time",
  title: "When Machines Learned to Speak Back",
  subtitle: "How numbers became reality.",
  date: "21st June, 2026",
  tags: ["DAC", "R-2R Ladder", "PWM", "Reconstruction Filter", "Waveform Generation"],
  sections: [
    {
      heading: "1. The Need to Influence Reality",
      content: [
        {
          type: "p",
          text: "Sensing the world is a passive act. A microcontroller can read an ADC, clocking timing intervals and translating physical temperatures, light levels, or voltages into neat digital variables. But observation alone does not change the physical state of a system. A machine that can only observe is a brain trapped in a jar—fully aware of its environment but powerless to act.\n\nTo become purposeful, a machine must eventually influence its surroundings. It needs to drive a speaker cone to vibrate air and generate sound, adjust the speed of a high-torque motor in an industrial conveyor, produce a specific reference voltage to calibrate another sensor, or generate a precise high-frequency carrier wave for radio transmission. Every active control system, from a simple thermostat to a multi-axis surgical robot, requires the ability to write actions back into physical space. Observation must give way to influence."
        }
      ]
    },
    {
      heading: "2. The Reverse Journey",
      content: [
        {
          type: "p",
          text: "This requirement defines a symmetrical engineering challenge. In our earlier explorations, we watched the Analog-to-Digital Converter (ADC) carve physical reality into discrete digital states. The ADC took a continuous voltage, sampled it at discrete intervals in time, and rounded it to the nearest binary code on a grid. It was a journey from continuous physics to discrete numbers.\n\nTo speak back, the machine must take the reverse journey. It must start with a discrete binary code—a neat integer stored in a CPU register—and translate it back into a continuous physical voltage. This is the domain of the Digital-to-Analog Converter (DAC). Below is a conceptual representation of this symmetry:"
        },
        {
          type: "image",
          src: "Images/dac_reverse_journey.svg",
          alt: "The Symmetry of ADC and DAC pathways",
          caption: "Figure 1: While the ADC slices continuous signals into discrete digital numbers, the DAC maps numbers back into physical voltages."
        }
      ]
    },
    {
      heading: "3. How a DAC Works: The Resistor Divider Intuition",
      content: [
        {
          type: "p",
          text: "How does a chip translate an abstract binary number into a real physical voltage? At its heart, a DAC is a network of resistors and switches that divide a stable Reference Voltage ($V_{REF}$) down to a specific fraction.\n\nConsider a simple resistor divider ladder. A binary code represents a set of instructions for a switch matrix. For instance, in a classic R-2R ladder architecture, each bit of the digital input code controls a corresponding physical switch. If a bit is 1, its switch connects a node in the resistor ladder to the Reference Voltage ($V_{REF}$). If a bit is 0, the switch connects that node to ground. The current splits symmetrically at each R-2R junction. By summing these scaled currents, the DAC generates an output current directly proportional to the digital code, which is then buffered by an operational amplifier to output a clean, stable voltage. The hardware block diagram below illustrates this pipeline:"
        },
        {
          type: "image",
          src: "Images/dac_block_diagram.svg",
          alt: "DAC Pipeline Block Diagram",
          caption: "Figure 2: The internal elements of a DAC: input register, switch matrix, resistor scaling network, and output buffer."
        }
      ]
    },
    {
      heading: "4. Resolution: Slicing the Staircase",
      content: [
        {
          type: "p",
          text: "Just as with ADCs, a DAC's precision is governed by its Resolution. Resolution defines the number of discrete steps the DAC can use to construct its output voltage.\n\n- An **8-bit DAC** yields $2^8 = 256$ discrete voltage steps.\n- A **10-bit DAC** provides $2^{10} = 1024$ steps.\n- A **12-bit DAC** provides $2^{12} = 4096$ steps, which is standard for high-quality microcontroller peripherals.\n- A **16-bit DAC** provides $2^{16} = 65,536$ steps, used in high-fidelity audio equipment where stepped jaggedness would introduce audible distortion.\n\nThe smallest voltage change the DAC can output is called the Least Significant Bit (LSB) size. As resolution increases, the step size shrinks, transforming a coarse, jagged staircase into a smooth line. Below is a comparison of output granularity across resolutions:"
        },
        {
          type: "image",
          src: "Images/dac_resolution_comparison.svg",
          alt: "DAC Resolution Step Comparison",
          caption: "Figure 3: High resolution minimizes the quantization step size, allowing the DAC to reconstruct curves with minimal distortion."
        }
      ]
    },
    {
      heading: "5. Reference Voltage: The Boundary Ruler",
      content: [
        {
          type: "p",
          text: "A DAC cannot output a voltage larger than the Reference Voltage ($V_{REF}$) supplied to its core. $V_{REF}$ acts as the physical ruler that calibrates the digital steps. The relationship between the output voltage ($V_{OUT}$), the digital code, the resolution ($N$), and $V_{REF}$ is defined as:\n\n$V_{OUT} = V_{REF} \\times \\frac{\\text{Digital Code}}{2^N - 1}$\n\nIf $V_{REF}$ is 3.3V, a 12-bit code of `4095` outputs exactly 3.3V, while `2048` outputs 1.65V. If $V_{REF}$ drifts or contains high-frequency electrical noise, that noise couples directly into $V_{OUT}$—if the ruler expands and contracts, the measurements scale with it. Therefore, a clean, stable, and decoupled reference voltage is vital for analog precision. Below is an illustration of how $V_{REF}$ defines the output scaling boundaries:"
        },
        {
          type: "image",
          src: "Images/dac_reference_voltage.svg",
          alt: "Reference Voltage Scaling",
          caption: "Figure 4: Reference voltage dictates both the maximum output range and the individual step size (LSB) of the converter."
        }
      ]
    },
    {
      heading: "6. Waveform Generation: Building Curves from Steps",
      content: [
        {
          type: "p",
          text: "To generate a dynamic waveform—such as a smooth audio tone, a linear motor ramp, or a calibration pulse—the CPU writes a continuous stream of digital values to the DAC register in a periodic loop driven by timer interrupts.\n\nFor example, to generate a Sine Wave, engineers compute a table of sine values beforehand and load them into memory. Every time a timer overflows, a DMA (Direct Memory Access) channel automatically copies the next value from the table directly into the DAC data register without CPU intervention. By updating the DAC at a high, constant frequency, the discrete steps approximate a continuous curve. The illustrations below depict how different waveforms are constructed by sequencing discrete values:"
        },
        {
          type: "image",
          src: "Images/dac_waveform_generation.svg",
          alt: "Waveform Generation",
          caption: "Figure 5: Building Sine, Triangle, Sawtooth, and Square waveforms by outputting timed sequences of digital codes."
        }
      ]
    },
    {
      heading: "7. The Illusion of Continuity: Filtering the Steps",
      content: [
        {
          type: "p",
          text: "If you look closely at a raw DAC output on an oscilloscope, you will see a stair-step pattern. If this raw voltage is fed directly to a high-frequency speaker, the sharp corners of the steps (which represent high-frequency harmonic distortion) will cause an audible hiss or crackle. How do we turn these steps into a truly smooth curve?\n\nThe solution is a Reconstruction Filter. This is a low-pass analog filter placed immediately after the DAC output pin. A simple resistor-capacitor (RC) filter removes the high-frequency transitions (the sharp corners of the steps), leaving only the fundamental low-frequency analog wave. Furthermore, many physical loads (like speaker diaphragms or heavy motor coils) possess natural mechanical or inductive inertia, meaning they cannot react instantly to the steps anyway. They act as natural low-pass filters, integrating the steps into smooth physical movements. Below is a diagram of low-pass reconstruction filtering:"
        },
        {
          type: "image",
          src: "Images/dac_illusion_continuity.svg",
          alt: "Low-Pass Reconstruction Filter",
          caption: "Figure 6: A low-pass filter integrates the sharp steps of the raw DAC output, smoothing it into a continuous analog waveform."
        }
      ]
    },
    {
      heading: "8. PWM: The Impostor DAC",
      content: [
        {
          type: "p",
          text: "In many embedded systems, dedicated DAC hardware is absent because it requires substantial PCB silicon and pin counts. Instead, engineers often use a timer to generate Pulse-Width Modulation (PWM) signals, mimicking an analog output.\n\nBy toggling a digital pin rapidly between 0V and 3.3V at a high frequency (often tens of kilohertz) and adjusting the Duty Cycle (the ratio of HIGH time to the total period), we can represent different voltages. If we pass this PWM stream through a low-pass RC filter, the filter integrates the square pulses, smoothing the high-frequency switching into a steady DC voltage directly proportional to the duty cycle. The diagram below illustrates this integration:"
        },
        {
          type: "image",
          src: "Images/pwm_impostor_dac.svg",
          alt: "PWM Impostor DAC",
          caption: "Figure 7: Using high-frequency PWM duty-cycle pulses combined with a low-pass filter to generate an average analog voltage."
        },
        {
          type: "p",
          text: "While PWM is cheap, simple, and highly efficient for power applications (like driving LEDs or brushless motors), it is an imperfect 'impostor' DAC. It suffers from slow response times (due to filter charging delays) and contains switching ripple noise that is difficult to filter out completely. A true DAC provides a steady, immediate voltage level without switching noise. The comparison below contrasts the two methods:"
        },
        {
          type: "image",
          src: "Images/pwm_vs_dac_comparison.svg",
          alt: "PWM vs True DAC Comparison",
          caption: "Figure 8: A true DAC provides clean, instantaneous voltage steps, whereas a filtered PWM introduces exponential rise delays and ripple noise."
        }
      ]
    },
    {
      heading: "9. Painting with Voltage",
      content: [
        {
          type: "p",
          text: "Let's observe these conversion behaviors. In the interactive panel below, modify reference voltage, DAC resolution, and digital input codes to watch how digital values translate into analog voltages on a meter."
        },
        {
          type: "edgecase",
          id: "painting-with-voltage"
        }
      ]
    },
    {
      heading: "10. The Illusion of Smoothness",
      content: [
        {
          type: "p",
          text: "How does sequence timing and low-pass filtering shape the output waveform? In the simulator below, adjust the waveform type, update rate, resolution, and low-pass reconstruction filter cutoff to see how a continuous curve is painted."
        },
        {
          type: "edgecase",
          id: "illusion-of-smoothness"
        }
      ]
    },
    {
      heading: "11. Real Embedded Applications",
      content: [
        {
          type: "p",
          text: "DACs are the expressive voice of microcontrollers. They drive audio amplifiers in smart speakers, generate control voltages in industrial loops (like proportional valves), produce high-frequency diagnostic test signals in lab instruments, calibrate medical pacemakers, and execute motor speed profiling in robotics. By giving digital systems a path to write back to the physical world, the DAC completes the handshake between computational logic and physical reality."
        }
      ]
    }
  ],
  closing: {
    heading: "The Expressive Handshake",
    paragraphs: [
      "Timers taught machines when to pay attention. ADCs taught machines how to translate reality into digital coordinates. DACs taught machines how to write numbers back into physical reality.",
      "For the first time, a machine could not only understand its environment, but actively influence it. Yet as these sensory and output capabilities expanded, a new system challenge emerged. Managing high-speed sampling, responding, keeping time, and communicating all at once required synchronized scheduling. The next engineering frontier was no longer sensing or speaking—it was scheduling what deserved the processor's attention next."
    ],
    quote: "A processor without a DAC is a mind without a voice—fully capable of thought, but unable to sing."
  },
  footer: "Reflections on digital-to-analog conversions - PrajnaEdge.dev"
},
{
  id: "the-tyranny-of-waiting",
  category: "Coordination",
  series: "The Architecture of Time",
  title: "The Tyranny of Waiting",
  subtitle: "The simplest way to control a machine eventually becomes its greatest limitation.",
  date: "21st June, 2026",
  tags: ["Polling", "Bare-Metal", "Latency", "Real-Time Constraints", "CPU Overhead"],
  sections: [
    {
      heading: "1. The Infinite Loop",
      content: [
        {
          type: "p",
          text: "At the root of almost every bare-metal embedded system is a simple, inescapable fact: a processor must never stop executing instructions. Unlike desktop software that can run, finish its task, and cleanly return to an operating system, a microcontroller is the operating system. It has nowhere to go. If the CPU is allowed to reach the end of the program counter, it falls off a digital cliff, entering an undefined state where it may execute random garbage RAM contents. To maintain absolute control, the core must loop forever.\n\nThis is why embedded firmware fundamentally revolves around an endless loop:\n\n```c\nint main(void) {\n    // Initialize peripherals\n    SystemInit();\n    \n    while(1) {\n        // The engine of the system\n    }\n}\n```\n\nThis simple `while(1)` structure is the structural spine of bare-metal computing. It keeps the CPU active, heartbeat regular, and program execution contained. In a quiet, simple machine, this loop is the perfect foundation. But it is also an empty arena, waiting for responsibilities."
        },
        {
          type: "img",
          src: "Images/polling_infinite_loop.svg",
          alt: "The circular flow of the infinite while(1) loop."
        }
      ]
    },
    {
      heading: "2. The Birth of Polling",
      content: [
        {
          type: "p",
          text: "Suppose we want our microcontroller to react when a user presses a button. How does the software know the button was pressed? The simplest and most intuitive way is to write code that actively, repeatedly checks the state of the pin connected to that button. We place a check function inside our loop:\n\n```c\nwhile(1) {\n    if (ReadPin(BUTTON_PIN) == PIN_LOW) {\n        ToggleLED();\n    }\n}\n```\n\nThis is the birth of Polling. The central processing unit (CPU) is placed in a perpetual state of interrogation. It reads the input port register, compares the bit with its target state, and takes action if necessary. It asks: *'Has anything happened?'* Then, nanoseconds later, it asks again: *'Has anything happened?'*\n\nThis direct checking pattern is incredibly elegant because it is deterministic and easy to reason about. There are no background threads, no complex scheduler structures, and no preemption. The CPU does one thing: it waits, inspects, and reacts."
        }
      ]
    },
    {
      heading: "3. The Cost of Curiosity",
      content: [
        {
          type: "p",
          text: "But this curiosity is not free. When a processor polls, it consumes energy at its maximum operating rate. Even if the button is pressed once an hour, the processor does not rest. It spends millions of CPU cycles every second checking the same pin, reading the same registry value, and getting the exact same answer: *'No. Nothing has changed.'*\n\nIn a battery-powered device, this is a disaster. Polling wastes massive amounts of power. The core is 100% active, running at full speed and drawing full current, simply to confirm that the world is quiet. The processor is trapped in a loop of wasted effort, spinning its wheels at top speed while waiting for something to happen."
        },
        {
          type: "img",
          src: "Images/polling_wasted_effort.svg",
          alt: "Wasted CPU cycles: 99.9% of checks return no change, keeping core load at 100%."
        },
        {
          type: "curious",
          text: "Curious? Many early embedded systems, from microwave ovens to simple industrial controllers, relied entirely on polling. Because power consumption and complex coordination were secondary concerns, the simplicity of a polling loop was an easy engineering tradeoff."
        }
      ]
    },
    {
      heading: "4. The Growing System",
      content: [
        {
          type: "p",
          text: "The limitations of polling become severe when we add more responsibilities. Let's design a real-world system. It needs to read a UART command interface, sample an ADC temperature sensor, monitor a CAN bus network for safety alerts, and toggle an indicator LED. If we stick to our polling strategy, our loop grows to handle all of them:\n\n```c\nwhile(1) {\n    CheckButton();\n    CheckUART();\n    CheckADC();\n    CheckCAN();\n    UpdateLEDs();\n}\n```\n\nNow, the central processing unit is no longer just checking the button. It must perform a sequence of duties. Each check requires time. If `CheckUART()` has to read a packet, it executes instructions. If `CheckADC()` must wait for a conversion, it spins. As we add more peripherals, the total execution time of a single pass through the loop—the loop cycle time—stretches."
        },
        {
          type: "img",
          src: "Images/polling_growing_system.svg",
          alt: "The expanding loop: as more peripherals are added, loop cycle time grows significantly."
        },
        {
          type: "curious",
          text: "Curious? As systems grow larger, waiting becomes increasingly expensive. When one slow driver function blocks the loop, every other peripheral in the system is forced to wait for its turn, degrading the responsiveness of the entire machine."
        }
      ]
    },
    {
      heading: "5. Latency: The Unnoticed Gap",
      content: [
        {
          type: "p",
          text: "This brings us to the critical bottleneck of polling: Latency. In embedded engineering, latency is the delay between the occurrence of a physical event and the processor's response to it.\n\nImagine a UART message packet arriving at the exact millisecond `CheckUART()` finishes. The CPU moves to `CheckADC()`, then `CheckCAN()`, then `UpdateLEDs()`, and finally loops back to `CheckButton()`. Only when the execution path returns to `CheckUART()` does the CPU finally detect the packet. The worst-case response latency is directly proportional to the total loop cycle time:\n\n$$\\text{Max Latency} = \\sum_{i=1}^{N} \\text{Time}(\\text{Check}_i)$$\n\nIf the loop cycle time exceeds the arrival rate of new data, we encounter a catastrophic failure mode: missed events. If a second UART character arrives before the loop finishes its round to read the first, the hardware's internal buffer overflows, and data is permanently lost."
        },
        {
          type: "img",
          src: "Images/polling_latency_timeline.svg",
          alt: "Timing timeline: showing the latency delay between an event's occurrence and its detection by the polling CPU."
        }
      ]
    },
    {
      heading: "6. Real Embedded Examples",
      content: [
        {
          type: "p",
          text: "Despite these limits, polling is still widely used in modern systems. In simple, low-cost microcontrollers running household appliances—like a toaster, a digital clock, or a basic toy—polling is perfectly sufficient. The event rates are low, power saving is achieved by sleeping the entire system when inactive, and latency is human-scale (a 50ms delay in a button press is imperceptible to a human user).\n\nHowever, in high-speed and complex applications—such as CAN communication in automotive ECUs, high-rate sensor acquisition in flight stabilizers, or audio stream buffers—polling fails. High-speed systems cannot afford to wait for a loop to spin; they require immediate, microsecond-accurate responses."
        }
      ]
    },
    {
      heading: "7. The Fundamental Limitation",
      content: [
        {
          type: "p",
          text: "The core design flaw of polling is structural: it ties coordination to the execution path of the software. The CPU spends almost all its time and power asking if something has happened, only to receive 'no' as an answer. It is a system built on active waiting, where the processor is both a bottleneck and a victim of its own loop structure."
        }
      ]
    }
  ],
  closing: {
    heading: "The Tyranny of the Loop",
    paragraphs: [
      "Polling works because the processor is simple, tireless, and constantly asks whether something has happened. It is the easiest way to control a machine, but as complexity grows, it becomes a structural straightjacket.",
      "But what if the processor could stop asking? What if the hardware could announce events instead? What if the machine only reacted when something actually changed, leaving the processor free to sleep or run other tasks in the meantime?",
      "That question would fundamentally change embedded software design. And it would lead directly to interrupts."
    ],
    quote: "To free the processor from the tyranny of waiting, we must stop asking the hardware if it is ready, and teach the hardware to speak up when it is."
  },
  footer: "Reflections on bare-metal polling loops and latency constraints - PrajnaEdge.dev"
},
{
  id: "when-hardware-learned-to-interrupt",
  category: "Coordination",
  series: "The Architecture of Time",
  title: "When Hardware Learned to Interrupt",
  subtitle: "The moment machines stopped waiting.",
  date: "21st June, 2026",
  tags: ["Interrupts", "NVIC", "Preemption", "Latency", "Vector Table"],
  sections: [
    {
      heading: "1. A World of Waiting",
      content: [
        {
          type: "p",
          text: "In our previous exploration, we watched a simple bare-metal embedded loop scale from a single button check to a complex array of duties. The microcontroller had to check the UART console, query an ADC sensor, inspect a CAN bus register, and toggle diagnostic LEDs. The result was a monolithic loop:\n\n```c\nwhile(1) {\n    CheckButton();\n    CheckUART();\n    CheckADC();\n    CheckCAN();\n}\n```\n\nThis is polling. Its primary flaw is structural: it ties coordination entirely to the execution path of the software. The CPU spends almost all its time and power asking if something has happened, only to receive 'no' as an answer. It keeps the core running at 100% load, consuming maximum power simply to check idle pins. It is a system built on active waiting, where responsiveness degrades as more peripherals stretch the loop cycle time."
        }
      ]
    },
    {
      heading: "2. The Reversal",
      content: [
        {
          type: "p",
          text: "What if we could reverse this relationship? Instead of the central processor constantly interrogating passive hardware components, what if the hardware could announce events instead?\n\nThis is the core philosophy of **Interrupts**. Rather than the CPU spinning in a loop asking *'Has anything happened?'*, the hardware peripherals are given a dedicated channel to signal the CPU: *'Something happened. Act now.'*\n\nThis simple reversal represents the most fundamental shift in embedded system architecture. It decouples event detection from the sequential flow of execution, freeing the CPU to execute background calculations or enter deep low-power sleep modes until the physical world demands its attention."
        }
      ]
    },
    {
      heading: "3. The Doorbell Analogy",
      content: [
        {
          type: "p",
          text: "To appreciate this shift, imagine waiting for a package delivery. Under a polling strategy, you must walk to the front door every ten seconds, open it, check the porch, close the door, and walk back. You can do nothing else; you are entirely consumed by the active wait.\n\nAn interrupt-driven approach equips the door with a bell. You sit down, read a book, or fall asleep. The visitor arrives and presses the button. The bell rings, interrupting your activity. You bookmark your page, answer the door, sign for the package, and return to exactly where you left off. The active checking is gone, replaced by a reactive trigger."
        }
      ]
    },
    {
      heading: "4. The Anatomy of an Interrupt",
      content: [
        {
          type: "p",
          text: "How does this handoff occur in raw silicon? When an external event occurs—such as a button pin falling low or a byte arriving in a UART buffer—the peripheral asserts a physical interrupt request (IRQ) line connected to the processor core. The hardware handoff then unfolds automatically:\n\n1. **Assertion**: The peripheral drives its IRQ line to its active state (high or low).\n2. **Synchronization**: The core detects the active line and waits to finish its currently executing machine instruction (typically 1 to 5 clock cycles).\n3. **Context Saving**: The CPU automatically halts normal execution and pushes its current register states (such as the Program Counter, Link Register, Stack Pointer, and Status Register) onto the stack. This preserves the exact state of the background program.\n4. **Vector Fetch**: The processor reads the vector table to fetch the memory address of the handler function associated with the triggering IRQ.\n5. **Execution**: The Program Counter jumps to that address, and the CPU begins executing the **Interrupt Service Routine (ISR)**.\n6. **Return**: Once the handler finishes, it executes a special return instruction. The CPU pops the saved registers back off the stack, restoring the CPU state, and resumes the background program exactly where it was paused."
        },
        {
          type: "img",
          src: "Images/interrupt_flow.svg",
          alt: "The step-by-step lifecycle of an interrupt request handoff."
        }
      ]
    },
    {
      heading: "5. Interrupt Latency",
      content: [
        {
          type: "p",
          text: "While interrupts resolve the polling delay bottleneck, they do not respond instantly. In embedded systems engineering, **Interrupt Latency** is the exact delay between the assertion of the hardware IRQ line and the execution of the first instruction in the ISR.\n\nLatency is a hardware tax composed of several parts: completing the current instruction, pushing CPU registers onto the stack (stacking), syncing clocks between the peripheral bus and core, and executing entry handler routines. In modern ARM Cortex-M processors, this hardware stacking and lookup process is heavily optimized, taking as few as 12 to 24 clock cycles. But in real-time systems, every cycle counts. If another interrupt is already running or interrupts are temporarily disabled by the driver, this latency can stretch, potentially causing missed deadlines."
        },
        {
          type: "img",
          src: "Images/interrupt_latency.svg",
          alt: "The timing breakdown of hardware stacking and vector fetch latencies."
        }
      ]
    },
    {
      heading: "6. Priority and Preemption",
      content: [
        {
          type: "p",
          text: "A real embedded system has multiple interrupt sources. What happens if a button press occurs at the exact same millisecond a critical CAN network alarm frame arrives? How does the hardware choose?\n\nThis is solved by **Interrupt Priority**. Every interrupt source is assigned a priority value. When multiple IRQ lines are asserted simultaneously, the core's hardware interrupt controller (such as the Nested Vectored Interrupt Controller, or NVIC, in ARM architectures) compares their values and runs the highest-priority handler first. If a lower-priority handler is already running when a higher-priority event arrives, the hardware executes **Preemption**—instantly pausing the lower-priority ISR, pushing its registers to the stack, and running the higher-priority ISR. Only when the high-priority handler completes does the lower-priority handler resume."
        },
        {
          type: "img",
          src: "Images/interrupt_priority.svg",
          alt: "A multi-lane timing diagram visualizing preemption and context nesting."
        }
      ]
    },
    {
      heading: "7. Nested Interrupts",
      content: [
        {
          type: "p",
          text: "This ability to preempt running handlers is called **Nesting**. Without nesting, a slow, low-priority handler (like a periodic temperature readout) would block a high-speed critical line (like a motor safety trip signal) for milliseconds, defeating the real-time guarantees of the system.\n\nPrioritization and nesting ensure that critical routines remain deterministic, regardless of other activities. However, nesting also introduces a system risk: stack depth. Each nested layer pushes more registers onto the RAM stack. If too many interrupts nest, the stack can overrun into application variables, leading to silent memory corruption."
        },
        {
          type: "curious",
          text: "Curious? Most timer compare events can be configured to generate interrupts. This allows firmware to schedule high-precision periodic events without polluting the main loop."
        }
      ]
    },
    {
      heading: "8. The Vector Table",
      content: [
        {
          type: "p",
          text: "How does the hardware translate a physical IRQ number into a software function address? It reads the **Vector Table**.\n\nThe Vector Table is an array of function pointers placed at a fixed location in memory (typically at the very bottom of the Flash partition, `0x0000_0000` or `0x0800_0000`). Each index corresponds to a specific hardware line: index 0 is the initial stack pointer, index 1 is the Reset Vector, index 2 is the Non-Maskable Interrupt (NMI), and subsequent indices map to internal faults, timers, and external peripherals.\n\nWhen a peripheral triggers, the processor uses the IRQ index to offset into this table, reads the 32-bit address stored there, and jumps directly to that address. You may recognize the first entries from *The First Instruction*: the Reset Vector is simply the very first interrupt address fetched by the silicon when power is applied."
        },
        {
          type: "img",
          src: "Images/interrupt_vector_table.svg",
          alt: "The mapping between hardware address indexes and handler code in flash."
        },
        {
          type: "curious",
          text: "Curious? ADC conversions often notify software through interrupts. When a conversion completes, the ADC asserts its IRQ line, allowing the CPU to read the register exactly when the conversion finishes."
        }
      ]
    },
    {
      heading: "9. Real Embedded Examples",
      content: [
        {
          type: "p",
          text: "Interrupts are the invisible coordination layer of modern electronics. In a UART interface, an interrupt triggers each time a character lands in the receive register, ensuring the CPU extracts it before it is overwritten. In a motor control loop, timer compare interrupts trigger microsecond-aligned PWM adjustments. In safety systems, CAN controllers trigger emergency handlers the moment an error frame is detected.\n\nBy replacing active waiting with reactive notifications, interrupts allow microcontrollers to sleep when inactive and respond with microsecond precision when needed. They represent the moment hardware became coordinate-aware."
        },
        {
          type: "curious",
          text: "Curious? Some high-speed communication systems generate so many interrupts that a new bottleneck emerges. If interrupts trigger faster than the CPU can push and pop the stack, the processor gets stuck in a state of continuous interrupt thrashing, leaving no time for background application tasks."
        }
      ]
    }
  ],
  closing: {
    heading: "The Limits of Response",
    paragraphs: [
      "Polling wasted CPU time by constantly asking if anything happened. Interrupts solved this by reversing the relationship, allowing the hardware to announce its readiness directly to the core.",
      "But as system speeds continued to climb, a new engineering limit emerged. Imagine a high-speed network transceiver receiving thousands of bytes every millisecond, or an ADC sampling at megahertz rates. If the CPU must pause, save registers, jump to an ISR, extract a byte, restore registers, and return for every single byte, the processor is quickly overwhelmed.",
      "The CPU now spends less time waiting, but it spends all of its time responding. Handling the data has become more expensive than detecting it.",
      "To break this bottleneck, data needed to be moved directly from hardware to memory without involving the CPU at all. That need would lead directly to Direct Memory Access."
    ],
    quote: "Interrupts freed the processor from active waiting, but as speed scaled, the core became a victim of its own responsiveness."
  },
  footer: "Reflections on hardware interrupt requests and vector table architectures - PrajnaEdge.dev"
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
      if (b.type === 'p') {
        let textContent = b.html ? b.text : escHtml(b.text);
        return `<p style="color:#CBD5E1;line-height:1.85;font-size:0.975rem;margin-bottom:1rem;white-space:pre-line">${parseTextFormatting(textContent)}</p>`;
      }
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
      ${item.closing.paragraphs.map(p => {
        let textContent = escHtml(p);
        return `<p style="color:#CBD5E1;line-height:1.85;font-size:0.975rem;margin-bottom:1rem">${parseTextFormatting(textContent)}</p>`;
      }).join('')}
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

function parseTextFormatting(text) {
  // 1. Bold notation: **text** -> <strong>text</strong>
  let parsed = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  
  // 2. Math LaTeX-like notation: $...$ -> custom HTML formatting
  parsed = parsed.replace(/\$(.*?)\$/g, (match, mathExpr) => {
    // Replace 2^x or 2^{x}
    if (/^2\^\{?(\d+)\}?$/.test(mathExpr)) {
      return mathExpr.replace(/^2\^\{?(\d+)\}?$/, '2<sup>$1</sup>');
    }
    // Replace V_{REF} or V_REF
    if (/^V_\{?REF\}?$/.test(mathExpr)) {
      return '<i>V</i><sub>REF</sub>';
    }
    // Fallback: wrap in italic tag for variables
    return `<i>${mathExpr}</i>`;
  });
  
  return parsed;
}

function initEdgeCase(containerId) {
  if (containerId === 'uart-conversation-builder') {
    renderUartConversationBuilder();
  } else if (containerId === 'spi-shared-rhythm') {
    renderSpiSharedRhythm();
  } else if (containerId === 'spi-silent-conversation') {
    renderSpiSilentConversation();
  } else if (containerId === 'i2c-shared-bus') {
    renderI2cSharedBus();
  } else if (containerId === 'i2c-bus-arbitration') {
    renderI2cBusArbitration();
  } else if (containerId === 'can-conversation-of-dominance') {
    renderCanConversationOfDominance();
  } else if (containerId === 'can-journey-of-a-frame') {
    renderCanJourneyOfAFrame();
  } else if (containerId === 'timer-builder') {
    renderTimerBuilder();
  } else if (containerId === 'pwm-painter') {
    renderPwmPainter();
  } else if (containerId === 'capturing-reality') {
    renderCapturingReality();
  } else if (containerId === 'cost-of-observation') {
    renderCostOfObservation();
  } else if (containerId === 'painting-with-voltage') {
    renderPaintingWithVoltage();
  } else if (containerId === 'illusion-of-smoothness') {
    renderIllusionOfSmoothness();
  }
}

function renderUartConversationBuilder() {
  const container = document.getElementById('uart-conversation-builder');
  if (!container) return;

  container.className = 'edgecase-wrapper';
  
  // HTML layout
  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Journey of a Byte</div>
    <div class="edgecase-subheader">What really happens when you send "Hello"?</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Walk through the hidden layers of registers, serial frames, electrical signals, and sampling points.
    </div>

    <!-- CONFIGURATION SETTINGS (TX & RX ALWAYS VISIBLE SIDE-BY-SIDE WITH AGREEMENT) -->
    <div class="pipeline-step">System Configurations</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1.5rem;">
        <!-- TX Column -->
        <div>
          <div class="panel-title" style="color:var(--blue); font-size:0.85rem; margin-bottom:0.75rem;">Transmitter (TX Contract)</div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-tx-baud" style="font-size:0.7rem;">TX Baud Rate</label>
            <select id="ec-tx-baud" class="edgecase-select">
              <option value="9600" selected>9600 bps</option>
              <option value="19200">19200 bps</option>
              <option value="115200">115200 bps</option>
            </select>
          </div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-tx-databits" style="font-size:0.7rem;">TX Data Bits</label>
            <select id="ec-tx-databits" class="edgecase-select">
              <option value="5">5 Bits</option>
              <option value="6">6 Bits</option>
              <option value="7">7 Bits</option>
              <option value="8" selected>8 Bits</option>
            </select>
          </div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-tx-parity" style="font-size:0.7rem;">TX Parity</label>
            <select id="ec-tx-parity" class="edgecase-select">
              <option value="None" selected>None</option>
              <option value="Even">Even</option>
              <option value="Odd">Odd</option>
            </select>
          </div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-tx-stopbits" style="font-size:0.7rem;">TX Stop Bits</label>
            <select id="ec-tx-stopbits" class="edgecase-select">
              <option value="1" selected>1 Bit</option>
              <option value="2">2 Bits</option>
            </select>
          </div>
        </div>

        <!-- RX Column -->
        <div>
          <div class="panel-title" style="color:#E2E8F0; font-size:0.85rem; margin-bottom:0.75rem;">Receiver (RX Contract)</div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-rx-baud" style="font-size:0.7rem;">RX Baud Rate</label>
            <select id="ec-rx-baud" class="edgecase-select">
              <option value="4800">4800 bps</option>
              <option value="9600" selected>9600 bps</option>
              <option value="14400">14400 bps</option>
              <option value="19200">19200 bps</option>
              <option value="115200">115200 bps</option>
            </select>
          </div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-rx-databits" style="font-size:0.7rem;">RX Data Bits</label>
            <select id="ec-rx-databits" class="edgecase-select">
              <option value="5">5 Bits</option>
              <option value="6">6 Bits</option>
              <option value="7">7 Bits</option>
              <option value="8" selected>8 Bits</option>
            </select>
          </div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-rx-parity" style="font-size:0.7rem;">RX Parity</label>
            <select id="ec-rx-parity" class="edgecase-select">
              <option value="None" selected>None</option>
              <option value="Even">Even</option>
              <option value="Odd">Odd</option>
            </select>
          </div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-rx-stopbits" style="font-size:0.7rem;">RX Stop Bits</label>
            <select id="ec-rx-stopbits" class="edgecase-select">
              <option value="1" selected>1 Bit</option>
              <option value="2">2 Bits</option>
            </select>
          </div>
        </div>

        <!-- Agreement Column -->
        <div>
          <div class="panel-title" style="color:#10B981; font-size:0.85rem; margin-bottom:0.75rem;">Agreement Verification</div>
          <div id="ec-agreement-container"></div>
        </div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="pipeline-step">System Controls</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: 2fr 1fr 1fr; gap:1rem; align-items:end;">
        <div class="edgecase-control-group" style="margin:0;">
          <label for="ec-text" style="font-size:0.7rem;">Enter Message (Press SEND to Transmit)</label>
          <input type="text" id="ec-text" class="edgecase-input" value="Hello" maxlength="12" style="width:100%;">
        </div>
        <div class="edgecase-control-group" style="margin:0;">
          <label for="ec-char-select" style="font-size:0.7rem;">Inspect Byte Details</label>
          <select id="ec-char-select" class="edgecase-select" style="width:100%;"></select>
        </div>
        <button id="ec-send-btn" class="edgecase-button" style="margin:0; width:100%; height:38px;">SEND MESSAGE</button>
      </div>
    </div>

    <!-- PIPELINE CONTAINERS -->
    <div id="ec-pipeline-container"></div>
  `;

  // Get DOM elements
  const txBaudSel = document.getElementById('ec-tx-baud');
  const txDataBitsSel = document.getElementById('ec-tx-databits');
  const txParitySel = document.getElementById('ec-tx-parity');
  const txStopBitsSel = document.getElementById('ec-tx-stopbits');

  const rxBaudSel = document.getElementById('ec-rx-baud');
  const rxDataBitsSel = document.getElementById('ec-rx-databits');
  const rxParitySel = document.getElementById('ec-rx-parity');
  const rxStopBitsSel = document.getElementById('ec-rx-stopbits');

  const textInput = document.getElementById('ec-text');
  const charSelect = document.getElementById('ec-char-select');
  const sendBtn = document.getElementById('ec-send-btn');
  const agreementContainer = document.getElementById('ec-agreement-container');
  const pipelineContainer = document.getElementById('ec-pipeline-container');

  // Simulation State
  let message = "Hello";
  let tempMessage = "Hello";
  let selectedIdx = 0;
  let animating = false;
  let currentStage = 10; // 10 = static completed state

  // Initialize character selector options
  function updateCharSelectOptions() {
    charSelect.innerHTML = "";
    for (let i = 0; i < message.length; i++) {
      const option = document.createElement('option');
      option.value = i;
      option.textContent = `Index ${i}: '${message[i]}'`;
      charSelect.appendChild(option);
    }
    // Restore or clamp index
    if (selectedIdx >= message.length) {
      selectedIdx = 0;
    }
    charSelect.value = selectedIdx;
  }

  // Event Listeners
  textInput.addEventListener('input', () => {
    tempMessage = textInput.value;
  });

  textInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendBtn.click();
    }
  });

  sendBtn.addEventListener('click', async () => {
    if (animating) return;
    
    message = tempMessage || " ";
    selectedIdx = 0;
    updateCharSelectOptions();
    
    // Start animation
    animating = true;
    currentStage = 1;
    
    runSimulation();
    
    // Animation loop using async sleep
    for (let stage = 1; stage <= 10; stage++) {
      currentStage = stage;
      runSimulation();
      await new Promise(resolve => setTimeout(resolve, 600));
    }
    
    animating = false;
    currentStage = 10;
    runSimulation();
  });

  charSelect.addEventListener('change', () => {
    selectedIdx = parseInt(charSelect.value) || 0;
    runSimulation();
  });

  const configSelectors = [
    txBaudSel, txDataBitsSel, txParitySel, txStopBitsSel,
    rxBaudSel, rxDataBitsSel, rxParitySel, rxStopBitsSel
  ];
  configSelectors.forEach(sel => {
    sel.addEventListener('change', () => {
      runSimulation();
    });
  });

  // Init
  updateCharSelectOptions();
  runSimulation();

  function runSimulation() {
    // Read current settings
    const txBaud = parseInt(txBaudSel.value);
    const txDataBits = parseInt(txDataBitsSel.value);
    const txParity = txParitySel.value;
    const txStopBits = parseInt(txStopBitsSel.value);

    const rxBaud = parseInt(rxBaudSel.value);
    const rxDataBits = parseInt(rxDataBitsSel.value);
    const rxParity = rxParitySel.value;
    const rxStopBits = parseInt(rxStopBitsSel.value);

    // 1. Agreement Verification Panel
    const baudOk = (txBaud === rxBaud);
    const bitsOk = (txDataBits === rxDataBits);
    const parityOk = (txParity === rxParity);
    const stopsOk = (txStopBits === rxStopBits);

    const verifyItems = [
      ["Baud Rate", baudOk, `${txBaud} vs ${rxBaud} bps`],
      ["Data Bits", bitsOk, `${txDataBits} vs ${rxDataBits} bits`],
      ["Parity Check", parityOk, `${txParity} vs ${rxParity}`],
      ["Stop Bits", stopsOk, `${txStopBits} vs ${rxStopBits}`]
    ];

    let agreementHtml = "";
    verifyItems.forEach(([name, ok, desc]) => {
      const icon = ok ? "✓" : "✗";
      const cls = ok ? "agreement-ok" : "agreement-fail";
      agreementHtml += `<div class="agreement-item ${cls}">${icon} ${name}: ${desc}</div>`;
    });
    agreementContainer.innerHTML = agreementHtml;

    // Get current inspected byte details
    const selectedChar = message[selectedIdx] || " ";
    const selectedCharCode = selectedChar.charCodeAt(0);
    const selectedCharBin = selectedCharCode.toString(2).padStart(8, '0');

    // Helper to get stage style
    function getStageStyle(stageNum) {
      if (animating) {
        if (stageNum < currentStage) {
          return { label: "", style: "" };
        } else if (stageNum === currentStage) {
          return {
            label: '<span style="color:#3B82F6; font-family:var(--mono); font-size:0.7rem; font-weight:bold; margin-left:1rem; border:1px solid #3B82F6; padding:0.15rem 0.4rem; border-radius:4px; background:rgba(59,130,246,0.1); letter-spacing:0.05em;">PROCESSING...</span>',
            style: "border-color: #3B82F6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.35); background: rgba(59, 130, 246, 0.02);"
          };
        } else {
          return {
            label: '<span style="color:var(--muted); font-family:var(--mono); font-size:0.7rem; margin-left:1rem;">(WAITING)</span>',
            style: "opacity: 0.15; filter: grayscale(100%); pointer-events: none;"
          };
        }
      } else {
        return { label: "", style: "" };
      }
    }

    // Pipeline generation
    let pipelineHtml = "";

    // Stage 1: Application (Software Variable)
    const st1 = getStageStyle(1);
    const prefix = message.slice(0, selectedIdx);
    const hlChar = `<span class="code-highlight">${escHtml(selectedChar)}</span>`;
    const suffix = message.slice(selectedIdx + 1);
    pipelineHtml += `
      <div class="pipeline-step">Stage 1: Application (Software variable) ${st1.label}</div>
      <div class="panel-box" style="${st1.style}">
        <div class="code-display">uart_write("${escHtml(prefix)}${hlChar}${escHtml(suffix)}");</div>
        <div style="font-size:0.7rem; color:var(--muted); margin-top:0.4rem;">The user application requests data transmission. The highlighted character is currently selected for inspection.</div>
      </div>
      <div class="arrow-divider">↓</div>
    `;

    // Stage 2: UART Driver (Handoff)
    const st2 = getStageStyle(2);
    pipelineHtml += `
      <div class="pipeline-step">Stage 2: UART Driver (Handoff) ${st2.label}</div>
      <div class="panel-box" style="${st2.style}">
        <div style="font-family:var(--mono); font-size:0.8rem; background:#0f172a; padding:0.6rem 1rem; border-radius:6px; border:1px solid var(--border);">
          <span style="color:var(--muted);">DRIVER STATE:</span> Pushing byte <span style="color:var(--blue); font-weight:bold;">0x${selectedCharCode.toString(16).toUpperCase().padStart(2, '0')}</span> to hardware register
        </div>
        <div style="font-size:0.7rem; color:var(--muted); margin-top:0.4rem;">The device driver intercepts the call, verifies if the peripheral is ready, and copies the data byte into the hardware transmitter port.</div>
      </div>
      <div class="arrow-divider">↓</div>
    `;

    // Stage 3: TX FIFO (Queue buffer)
    const st3 = getStageStyle(3);
    let txFifoHtml = "";
    for (let idx = 0; idx < message.length; idx++) {
      const cls = idx === selectedIdx ? "fifo-block fifo-active" : "fifo-block";
      txFifoHtml += `<div class="${cls}">${escHtml(message[idx])}</div>`;
    }
    pipelineHtml += `
      <div class="pipeline-step">Stage 3: TX FIFO (Queue buffer) ${st3.label}</div>
      <div class="panel-box" style="${st3.style}">
        <div style="font-family:var(--mono); font-size:0.7rem; color:var(--muted); text-transform:uppercase;">Hardware FIFO Buffer:</div>
        <div class="fifo-container">${txFifoHtml}</div>
        <div style="font-size:0.7rem; color:var(--muted); margin-top:0.4rem;">A hardware memory queue (FIFO) buffers bytes to prevent timing gaps if the CPU is busy with other tasks.</div>
      </div>
      <div class="arrow-divider">↓</div>
    `;

    // Stage 4: Serialization (ASCII & Binary Mapping)
    const st4 = getStageStyle(4);
    let lsbFirstArr = [];
    for (let b = 0; b < 8; b++) {
      lsbFirstArr.push((selectedCharCode >> b) & 1);
    }
    pipelineHtml += `
      <div class="pipeline-step">Stage 4: Serialization (ASCII & Binary Mapping) ${st4.label}</div>
      <div class="panel-box" style="${st4.style}">
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:1rem; font-family:var(--mono);">
          <div style="background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid var(--border);">
            <span style="color:var(--muted); font-size:0.7rem; display:block;">CHARACTER</span>
            <span style="color:#FFF; font-weight:bold; font-size:1.1rem;">'${escHtml(selectedChar)}'</span>
          </div>
          <div style="background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid var(--border);">
            <span style="color:var(--muted); font-size:0.7rem; display:block;">ASCII DECIMAL</span>
            <span style="color:var(--blue); font-weight:bold; font-size:1.1rem;">${selectedCharCode}</span>
          </div>
          <div style="background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid var(--border);">
            <span style="color:var(--muted); font-size:0.7rem; display:block;">BINARY BYTE</span>
            <span style="color:#10B981; font-weight:bold; font-size:1.1rem;">${selectedCharBin}</span>
          </div>
          <div style="background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid var(--border);">
            <span style="color:var(--muted); font-size:0.7rem; display:block;">LSB FIRST ORDER</span>
            <span style="color:var(--blue); font-weight:bold; font-size:1.1rem;">${lsbFirstArr.join(' → ')}</span>
          </div>
        </div>
        <div style="font-size:0.7rem; color:var(--muted); margin-top:0.4rem;">Software concepts translate into discrete physical values (0s and 1s) ordered LSB-first.</div>
      </div>
      <div class="arrow-divider">↓</div>
    `;

    // Stage 5: Shift Register (Parallel-In Serial-Out)
    const st5 = getStageStyle(5);
    let pisoCellsHtml = "";
    for (let b = 0; b < txDataBits; b++) {
      const bitVal = (selectedCharCode >> b) & 1;
      pisoCellsHtml += `
        <div class="register-cell">
          <div class="register-label">D${b}</div>
          <div class="register-val">${bitVal}</div>
        </div>
      `;
    }
    pipelineHtml += `
      <div class="pipeline-step">Stage 5: Shift Register (Parallel-In Serial-Out) ${st5.label}</div>
      <div class="panel-box" style="${st5.style}">
        <div style="font-family:var(--mono); font-size:0.7rem; color:var(--muted); text-transform:uppercase;">Transmitter Shift Register (PISO):</div>
        <div class="register-container">
          ${pisoCellsHtml}
          <div style="display:flex; align-items:center; margin-left:0.5rem; color:var(--blue); font-weight:bold; font-family:var(--mono); font-size:0.8rem;">➔ serial out</div>
        </div>
        <div style="font-size:0.7rem; color:var(--muted); margin-top:0.4rem;">Data is loaded in parallel from the buffer, then shifted out bit-by-bit onto the electrical trace.</div>
      </div>
      <div class="arrow-divider">↓</div>
    `;

    // Stages 6 & 7: Frame & Waveform (SVG)
    let label6 = "";
    let label7 = "";
    let combStyle = "";
    let highlightFrame = false;
    let highlightWaveform = false;

    if (animating) {
      if (currentStage < 6) {
        label6 = '<span style="color:var(--muted); font-family:var(--mono); font-size:0.7rem; margin-left:1rem;">(WAITING)</span>';
        label7 = '<span style="color:var(--muted); font-family:var(--mono); font-size:0.7rem; margin-left:1rem;">(WAITING)</span>';
        combStyle = "opacity: 0.15; filter: grayscale(100%); pointer-events: none;";
      } else if (currentStage === 6) {
        label6 = '<span style="color:#3B82F6; font-family:var(--mono); font-size:0.7rem; font-weight:bold; margin-left:1rem; border:1px solid #3B82F6; padding:0.15rem 0.4rem; border-radius:4px; background:rgba(59,130,246,0.1); letter-spacing:0.05em;">PROCESSING...</span>';
        label7 = '<span style="color:var(--muted); font-family:var(--mono); font-size:0.7rem; margin-left:1rem;">(WAITING)</span>';
        combStyle = "border-color: #3B82F6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.35); background: rgba(59, 130, 246, 0.02);";
        highlightFrame = true;
      } else if (currentStage === 7) {
        label7 = '<span style="color:#3B82F6; font-family:var(--mono); font-size:0.7rem; font-weight:bold; margin-left:1rem; border:1px solid #3B82F6; padding:0.15rem 0.4rem; border-radius:4px; background:rgba(59,130,246,0.1); letter-spacing:0.05em;">PROCESSING...</span>';
        combStyle = "border-color: #3B82F6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.35); background: rgba(59, 130, 246, 0.02);";
        highlightWaveform = true;
      }
    }

    // Build SVG components
    let txCharBits = [];
    for (let b = 0; b < txDataBits; b++) {
      txCharBits.push((selectedCharCode >> b) & 1);
    }
    let txParityBit = null;
    if (txParity !== "None") {
      const bitSum = txCharBits.reduce((a,b)=>a+b, 0);
      txParityBit = txParity === "Even" ? (bitSum % 2) : (bitSum % 2 === 0 ? 1 : 0);
    }

    let txFrameBits = [];
    txFrameBits.push({ type: "idle", label: "IDLE", val: 1, desc: "Line free" });
    txFrameBits.push({ type: "start", label: "START", val: 0, desc: "Frame Alert" });
    for (let b = 0; b < txDataBits; b++) {
      txFrameBits.push({ type: "data", label: `D${b}`, val: txCharBits[b], desc: b===0 ? "Payload LSB" : (b===txDataBits-1 ? "Payload MSB" : "Payload bit") });
    }
    if (txParityBit !== null) {
      txFrameBits.push({ type: "parity", label: "PARITY", val: txParityBit, desc: "Error Check" });
    }
    for (let s = 0; s < txStopBits; s++) {
      txFrameBits.push({ type: "stop", label: "STOP", val: 1, desc: "Frame End" });
    }
    txFrameBits.push({ type: "idle", label: "IDLE", val: 1, desc: "Line free" });

    const txStates = txFrameBits.map(b => b.val);

    const T_tx = 1.0;
    const T_rx = txBaud / rxBaud;
    const rxSampleCount = 1 + rxDataBits + (rxParity !== "None" ? 1 : 0) + rxStopBits;
    let rxSamplesInfo = [];

    for (let i = 0; i < rxSampleCount; i++) {
      const rxTime = (0.5 + i) * T_rx;
      const txTime = 1.0 + rxTime;
      const txIdx = Math.floor(txTime);
      let sampledVal = 1;
      if (txIdx >= 0 && txIdx < txStates.length) {
        sampledVal = txStates[txIdx];
      }

      let correct = true;
      if (txIdx >= txStates.length) {
        correct = false;
      } else {
        if (i === 0 && sampledVal !== 0) {
          correct = false;
        } else if (i >= 1 && i <= rxDataBits) {
          const txBitPos = i - 1;
          const expected = txBitPos < txDataBits ? txCharBits[txBitPos] : 1;
          if (sampledVal !== expected) correct = false;
        } else if (i >= 1 + rxDataBits + (rxParity !== "None" ? 1 : 0)) {
          if (sampledVal !== 1) correct = false;
        }
      }

      rxSamplesInfo.push({
        idx: i,
        txTime: txTime,
        val: sampledVal,
        correct: correct
      });
    }

    const svgW = 900;
    const svgH = 320;
    const padLeft = 70;
    const padRight = 30;
    const dispW = svgW - padLeft - padRight;
    const nSlots = txStates.length;
    const dx = dispW / nSlots;

    const colors = {
      idle: "#475569",
      start: "#EF4444",
      data: "#3B82F6",
      parity: "#F59E0B",
      stop: "#10B981"
    };

    let svgBlocks = [];
    const blocksOpacity = highlightWaveform ? "0.3" : "1.0";
    const waveformOpacity = highlightFrame ? "0.3" : "1.0";
    const waveformStrokeWidth = highlightWaveform ? "4" : "2";
    const waveformStrokeColor = highlightWaveform ? "#3B82F6" : "#FFFFFF";

    // 1. Draw Frame Blocks
    for (let i = 0; i < txFrameBits.length; i++) {
      const b = txFrameBits[i];
      const x = padLeft + i * dx;
      const c = colors[b.type];
      const strokeW = (highlightFrame && b.type !== "idle") ? "2.5" : "1.5";
      const fillOpacity = highlightFrame ? "0.15" : "0.08";
      svgBlocks.push(`
        <!-- Block ${b.label} -->
        <rect x="${x + 2}" y="15" width="${dx - 4}" height="70" rx="4" fill="none" stroke="${c}" stroke-width="${strokeW}" opacity="${blocksOpacity}" />
        <rect x="${x + 2}" y="15" width="${dx - 4}" height="70" rx="4" fill="${c}" opacity="${blocksOpacity === "1.0" ? fillOpacity : "0.02"}" />
        <text x="${x + dx/2}" y="32" fill="#94A3B8" font-family="monospace" font-size="8" text-anchor="middle" font-weight="bold" opacity="${blocksOpacity}">${b.label}</text>
        <text x="${x + dx/2}" y="56" fill="${b.val === 0 ? '#EF6868' : '#10B981'}" font-family="monospace" font-size="18" text-anchor="middle" font-weight="bold" opacity="${blocksOpacity}">${b.val}</text>
        <text x="${x + dx/2}" y="76" fill="#64748B" font-family="monospace" font-size="6.5" text-anchor="middle" opacity="${blocksOpacity}">${b.desc}</text>
      `);
    }

    // 2. Draw Waveform Step Line
    let pathD = `M 0,135 L ${padLeft},135`;
    for (let i = 0; i < nSlots; i++) {
      const val = txStates[i];
      const prevVal = i > 0 ? txStates[i-1] : 1;
      const y = val === 1 ? 135 : 175;
      const xStart = padLeft + i * dx;
      const xEnd = padLeft + (i + 1) * dx;
      if (val !== prevVal) {
        const yPrev = prevVal === 1 ? 135 : 175;
        pathD += ` L ${xStart},${yPrev} L ${xStart},${y}`;
      }
      pathD += ` L ${xEnd},${y}`;
    }
    pathD += ` L ${svgW},135`;

    svgBlocks.push(`
      <!-- Waveform Signal -->
      <path d="${pathD}" fill="none" stroke="${waveformStrokeColor}" stroke-width="${waveformStrokeWidth}" opacity="${waveformOpacity}" />
      <text x="${padLeft - 8}" y="139" fill="#64748B" font-family="monospace" font-size="8" text-anchor="end" opacity="${waveformOpacity}">HIGH (3.3V)</text>
      <text x="${padLeft - 8}" y="179" fill="#64748B" font-family="monospace" font-size="8" text-anchor="end" opacity="${waveformOpacity}">LOW (0V)</text>
    `);

    // Draw grid lines
    for (let i = 0; i <= nSlots; i++) {
      const x = padLeft + i * dx;
      svgBlocks.push(`<line x1="${x}" y1="15" x2="${x}" y2="195" stroke="#334155" stroke-dasharray="1,4" stroke-width="0.75" />`);
    }

    // 3. Draw RX Sampling Timeline (hidden during initial TX stages)
    const rxVisible = !(animating && currentStage < 8);
    if (rxVisible) {
      svgBlocks.push(`
        <!-- RX Axis line -->
        <line x1="${padLeft}" y1="235" x2="${svgW - padRight}" y2="235" stroke="#475569" stroke-width="1" />
        <text x="${padLeft - 8}" y="238" fill="#64748B" font-family="monospace" font-size="8" text-anchor="end">RX SAMPLES</text>
      `);

      rxSamplesInfo.forEach(s => {
        const xSample = padLeft + s.txTime * dx;
        if (xSample > (svgW - padRight)) return;

        const yWave = s.val === 1 ? 135 : 175;
        const color = s.correct ? "#3B82F6" : "#EF6868";
        const dash = s.correct ? "2,3" : "1,1";

        svgBlocks.push(`
          <!-- Sample S${s.idx} -->
          <line x1="${xSample}" y1="120" x2="${xSample}" y2="235" stroke="${color}" stroke-dasharray="${dash}" stroke-width="1" />
          <circle cx="${xSample}" cy="${yWave}" r="4" fill="${color}" stroke="#0F172A" stroke-width="1" />
          <circle cx="${xSample}" cy="235" r="3" fill="${color}" />
          <text x="${xSample}" y="252" fill="${color}" font-family="monospace" font-size="9" text-anchor="middle" font-weight="bold">S${s.idx}</text>
          <text x="${xSample}" y="266" fill="#FFF" font-family="monospace" font-size="9" text-anchor="middle" font-weight="bold">(${s.val})</text>
        `);
      });
    }

    const svgHtml = `
      <svg viewBox="0 0 ${svgW} ${svgH}" width="100%">
        ${svgBlocks.join('')}
      </svg>
    `;

    pipelineHtml += `
      <div class="pipeline-step">Stage 6: UART Frame Builder (TX Pin state) ${label6}</div>
      <div class="pipeline-step">Stage 7: Physical Wire (Waveform) ${label7}</div>
      <div class="panel-box" style="${combStyle}">
        <div style="background:#0F172A; padding:0; overflow-x:auto;">${svgHtml}</div>
        <div style="font-size:0.7rem; color:var(--muted); margin-top:0.4rem;">Voltage values on the physical trace directly echo the UART frame contract. Dashed lines illustrate receiver sampling offsets.</div>
      </div>
      <div class="arrow-divider">↓</div>
    `;

    // Stage 8: RX Pin & Receiver (Sampling & Demodulation)
    const st8 = getStageStyle(8);
    const rxStartVal = rxSamplesInfo[0].val;
    let flowSteps = [];

    if (rxStartVal === 0) {
      flowSteps.push('<span class="flow-step" style="color:#10B981;">✓ Waiting: Idle line HIGH</span>');
      flowSteps.push('<span class="flow-step" style="color:#10B981;">✓ Start Bit Detected (LOW)</span>');
    } else {
      flowSteps.push('<span class="flow-step" style="color:#EF6868;">✗ Waiting: Idle Mismatch</span>');
      flowSteps.push('<span class="flow-step" style="color:#EF6868;">✗ Start Bit Error (HIGH)</span>');
    }

    const rxDataBitsVals = rxSamplesInfo.slice(1, 1 + rxDataBits).map(s => s.val);
    flowSteps.push(`<span class="flow-step" style="color:#3B82F6;">➔ Sampling ${rxDataBits} Payload Bits: [${rxDataBitsVals.join(',')}]</span>`);

    if (rxParity !== "None") {
      const rxParIdx = 1 + rxDataBits;
      const rxParityVal = rxParIdx < rxSamplesInfo.length ? rxSamplesInfo[rxParIdx].val : 1;
      const rxSum = rxDataBitsVals.reduce((a,b)=>a+b, 0);
      const expectedPar = rxParity === "Even" ? (rxSum % 2) : (rxSum % 2 === 0 ? 1 : 0);
      if (rxParityVal === expectedPar) {
        flowSteps.push(`<span class="flow-step" style="color:#10B981;">✓ Parity Matched (${rxParity} = ${rxParityVal})</span>`);
      } else {
        flowSteps.push(`<span class="flow-step" style="color:#EF6868;">✗ Parity Error (Sampled ${rxParityVal}, expected ${expectedPar})</span>`);
      }
    }

    const rxStopStartIdx = 1 + rxDataBits + (rxParity !== "None" ? 1 : 0);
    const rxStopVals = rxSamplesInfo.slice(rxStopStartIdx, rxStopStartIdx + rxStopBits).map(s => s.val);
    const stopsValid = rxStopVals.every(v => v === 1);
    if (stopsValid) {
      flowSteps.push('<span class="flow-step" style="color:#10B981;">✓ Stop Bit(s) Verified (HIGH)</span>');
    } else {
      flowSteps.push('<span class="flow-step" style="color:#EF6868;">✗ Framing Error (Stop bit LOW)</span>');
    }

    let reconstructedCode = 0;
    for (let b = 0; b < rxDataBits; b++) {
      if (b < rxDataBitsVals.length && rxDataBitsVals[b] === 1) {
        reconstructedCode |= (1 << b);
      }
    }

    const byteValid = (rxStartVal === 0) && stopsValid && (rxParity === "None" || (txParity === rxParity));
    const recoveredChar = (byteValid && reconstructedCode >= 32 && reconstructedCode <= 126) ? String.fromCharCode(reconstructedCode) : "?";

    if (byteValid) {
      flowSteps.push(`<span class="flow-step" style="background:#10B981; color:#0F172A; font-weight:bold;">➔ Character Recovered: '${escHtml(recoveredChar)}'</span>`);
    } else {
      flowSteps.push('<span class="flow-step" style="background:#EF6868; color:#FFF; font-weight:bold;">➔ Character Corrupted: \'?\'</span>');
    }

    pipelineHtml += `
      <div class="pipeline-step">Stage 8: RX Pin & Receiver (Sampling & Demodulation) ${st8.label}</div>
      <div class="panel-box" style="${st8.style}">
        <div class="panel-title">Receiver Processing Flow (First Frame Byte)</div>
        <div style="margin-top:0.5rem; margin-bottom:0.5rem;">${flowSteps.join(' ')}</div>
        <div style="font-size:0.7rem; color:var(--muted);">The receiver checks timing offsets, decodes the voltage transitions, and validates the parity/stop framing.</div>
      </div>
      <div class="arrow-divider">↓</div>
    `;

    // Stage 9: RX FIFO (Hardware Input buffer)
    const st9 = getStageStyle(9);
    let recoveredChars = [];
    
    // Process all characters for full string recovery
    for (let char of message) {
      const val = char.charCodeAt(0);
      let tBits = [];
      for (let b = 0; b < txDataBits; b++) {
        tBits.push((val >> b) & 1);
      }
      let tPar = null;
      if (txParity !== "None") {
        const sum = tBits.reduce((a,b)=>a+b, 0);
        tPar = txParity === "Even" ? (sum % 2) : (sum % 2 === 0 ? 1 : 0);
      }

      let tFrame = [0].concat(tBits);
      if (tPar !== null) tFrame.push(tPar);
      for (let s = 0; s < txStopBits; s++) tFrame.push(1);
      let tFull = [1].concat(tFrame).concat([1]);

      let rSampled = [];
      for (let i = 0; i < rxSampleCount; i++) {
        const rTime = (0.5 + i) * T_rx;
        const txIdx = Math.floor(1.0 + rTime);
        let sVal = 1;
        if (txIdx >= 0 && txIdx < tFull.length) {
          sVal = tFull[txIdx];
        }
        rSampled.push(sVal);
      }

      const rStart = rSampled[0];
      const rData = rSampled.slice(1, 1 + rxDataBits);
      const rParVal = rxParity !== "None" ? rSampled[1 + rxDataBits] : null;
      const rStopStart = 1 + rxDataBits + (rxParity !== "None" ? 1 : 0);
      const rStops = rSampled.slice(rStopStart, rStopStart + rxStopBits);

      const fErr = (rStart !== 0) || rStops.some(v => v !== 1);
      let pErr = false;
      if (rxParity !== "None" && rParVal !== null) {
        const rxSum = rData.reduce((a,b)=>a+b, 0);
        const expectedP = rxParity === "Even" ? (rxSum % 2) : (rxSum % 2 === 0 ? 1 : 0);
        if (rParVal !== expectedP) pErr = true;
      }

      if (fErr || pErr) {
        recoveredChars.push("?");
      } else {
        let recVal = 0;
        for (let b = 0; b < rxDataBits; b++) {
          if (b < rData.length && rData[b] === 1) {
            recVal |= (1 << b);
          }
        }
        recoveredChars.push((recVal >= 32 && recVal <= 126) ? String.fromCharCode(recVal) : "?");
      }
    }

    let rxFifoBlocks = "";
    for (let idx = 0; idx < recoveredChars.length; idx++) {
      const char = recoveredChars[idx];
      const cls = idx === selectedIdx ? "fifo-block fifo-active-rx" : "fifo-block";
      if (char === "?") {
        rxFifoBlocks += `<div class="${cls}" style="border-color:#EF6868; color:#EF6868; background:rgba(239,68,68,0.08);">?</div>`;
      } else {
        rxFifoBlocks += `<div class="${cls}">${escHtml(char)}</div>`;
      }
    }

    pipelineHtml += `
      <div class="pipeline-step">Stage 9: RX FIFO (Hardware Input buffer) ${st9.label}</div>
      <div class="panel-box" style="${st9.style}">
        <div style="font-family:var(--mono); font-size:0.7rem; color:var(--muted); text-transform:uppercase;">Receiver FIFO Queue buffer:</div>
        <div class="fifo-container">${rxFifoBlocks}</div>
        <div style="font-size:0.7rem; color:var(--muted); margin-top:0.4rem;">Decoded bytes are queued into the receiver FIFO buffer, waiting to be read by the system's driver.</div>
      </div>
      <div class="arrow-divider">↓</div>
    `;

    // Stage 10: Application (Reconstructed Output)
    const st10 = getStageStyle(10);
    let recoveredMsgHtml = "";
    recoveredChars.forEach(c => {
      if (c === "?") {
        recoveredMsgHtml += `<span class="text-corrupted">?</span>`;
      } else {
        recoveredMsgHtml += escHtml(c);
      }
    });

    pipelineHtml += `
      <div class="pipeline-step">Stage 10: Application (Reconstructed Output) ${st10.label}</div>
      <div class="panel-box" style="${st10.style}">
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:1.25rem; font-family:var(--mono);">
          <div style="background:#0F172A; padding:0.6rem; border-radius:6px; border:1px solid rgba(148,163,184,0.1);">
            <span style="color:var(--muted); font-size:0.75rem; display:block;">TRANSMITTED MESSAGE</span>
            <span style="color:#FFF; font-weight:bold; font-size:1.4rem;">${escHtml(message)}</span>
          </div>
          <div style="background:#0F172A; padding:0.6rem; border-radius:6px; border:1px solid rgba(148,163,184,0.1);">
            <span style="color:var(--muted); font-size:0.75rem; display:block;">RECOVERED MESSAGE</span>
            <span style="color:#10B981; font-weight:bold; font-size:1.4rem;">${recoveredMsgHtml}</span>
          </div>
        </div>
        <div style="font-size:0.7rem; color:var(--muted); margin-top:0.4rem;">The software application reads the byte queue, completing the communication loop.</div>
      </div>
    `;

    pipelineContainer.innerHTML = pipelineHtml;
  }
}

function renderSpiSharedRhythm() {
  const container = document.getElementById('spi-shared-rhythm');
  if (!container) return;

  container.className = 'edgecase-wrapper';
  
  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Shared Rhythm</div>
    <div class="edgecase-subheader">CPOL and CPHA Configuration Mismatch</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Adjust Clock Polarity (CPOL) and Clock Phase (CPHA) to simulate how SPI devices align sampling windows and detect timing-induced data corruption.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Timing Configuration</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1.5rem;">
        <!-- Master Column -->
        <div>
          <div class="panel-title" style="color:var(--blue); font-size:0.85rem; margin-bottom:0.75rem;">Master Timing Registers</div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-m-cpol" style="font-size:0.7rem;">Master CPOL</label>
            <select id="ec-m-cpol" class="edgecase-select">
              <option value="0" selected>CPOL = 0 (Idle Low)</option>
              <option value="1">CPOL = 1 (Idle High)</option>
            </select>
          </div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-m-cpha" style="font-size:0.7rem;">Master CPHA</label>
            <select id="ec-m-cpha" class="edgecase-select">
              <option value="0" selected>CPHA = 0 (Sample Leading Edge)</option>
              <option value="1">CPHA = 1 (Sample Trailing Edge)</option>
            </select>
          </div>
        </div>

        <!-- Slave Column -->
        <div>
          <div class="panel-title" style="color:#E2E8F0; font-size:0.85rem; margin-bottom:0.75rem;">Slave Timing Registers</div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-s-cpol" style="font-size:0.7rem;">Slave CPOL</label>
            <select id="ec-s-cpol" class="edgecase-select">
              <option value="0" selected>CPOL = 0 (Idle Low)</option>
              <option value="1">CPOL = 1 (Idle High)</option>
            </select>
          </div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-s-cpha" style="font-size:0.7rem;">Slave CPHA</label>
            <select id="ec-s-cpha" class="edgecase-select">
              <option value="0" selected>CPHA = 0 (Sample Leading Edge)</option>
              <option value="1">CPHA = 1 (Sample Trailing Edge)</option>
            </select>
          </div>
        </div>

        <!-- Agreement Column -->
        <div>
          <div class="panel-title" style="color:#10B981; font-size:0.85rem; margin-bottom:0.75rem;">Mode Agreement</div>
          <div id="ec-spi-agreement-container"></div>
        </div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="pipeline-step">System Controls</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: 3fr 1fr; gap:1rem; align-items:end;">
        <div class="edgecase-control-group" style="margin:0;">
          <label for="ec-spi-text" style="font-size:0.7rem;">Enter Message (Max 12 chars)</label>
          <input type="text" id="ec-spi-text" class="edgecase-input" value="Hello" maxlength="12" style="width:100%;">
        </div>
        <button id="ec-spi-transmit-btn" class="edgecase-button" style="margin:0; width:100%; height:38px;">TRANSMIT</button>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Physical Waveform Timing Trace (Inspecting First Character)</div>
    <div class="edgecase-visual" id="ec-spi-waveform-container" style="background:#0F172A; min-height:230px; position:relative;"></div>

    <!-- OUTPUT PANELS -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-top:1.5rem;">
      <div>
        <div class="pipeline-step">Protocol Transaction Log</div>
        <div id="ec-spi-log" class="terminal-box"></div>
      </div>
      <div>
        <div class="pipeline-step">Data Recovery Outcome</div>
        <div class="panel-box" style="height:200px; display:flex; flex-direction:column; justify-content:center; gap:0.5rem; box-sizing:border-box;">
          <div style="font-family:var(--mono); font-size:0.65rem; color:var(--muted); text-transform:uppercase;">Slave Shift Register (Input Buffer):</div>
          <div id="ec-spi-rx-register" class="register-container" style="margin:0;"></div>
          <div id="ec-spi-outcome" style="margin-top:0.4rem;"></div>
        </div>
      </div>
    </div>
  `;

  // Get DOM elements
  const mCpolSel = document.getElementById('ec-m-cpol');
  const mCphaSel = document.getElementById('ec-m-cpha');
  const sCpolSel = document.getElementById('ec-s-cpol');
  const sCphaSel = document.getElementById('ec-s-cpha');
  
  const textInput = document.getElementById('ec-spi-text');
  const transmitBtn = document.getElementById('ec-spi-transmit-btn');
  
  const agreementContainer = document.getElementById('ec-spi-agreement-container');
  const waveformContainer = document.getElementById('ec-spi-waveform-container');
  const logContainer = document.getElementById('ec-spi-log');
  const rxRegisterContainer = document.getElementById('ec-spi-rx-register');
  const outcomeContainer = document.getElementById('ec-spi-outcome');

  let message = "Hello";
  let tempMessage = "Hello";
  let animating = false;
  let animStep = 20;

  textInput.addEventListener('input', () => {
    tempMessage = textInput.value;
  });

  textInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      transmitBtn.click();
    }
  });

  transmitBtn.addEventListener('click', async () => {
    if (animating) return;
    message = tempMessage || " ";
    animating = true;
    animStep = 0;
    
    for (let step = 0; step <= 17; step++) {
      animStep = step;
      updateUi();
      await new Promise(resolve => setTimeout(resolve, 150));
    }
    
    animating = false;
    animStep = 20;
    updateUi();
  });

  const selectInputs = [mCpolSel, mCphaSel, sCpolSel, sCphaSel];
  selectInputs.forEach(sel => {
    sel.addEventListener('change', () => {
      updateUi();
    });
  });

  updateUi();

  function updateUi() {
    const mCpol = parseInt(mCpolSel.value);
    const mCpha = parseInt(mCphaSel.value);
    const sCpol = parseInt(sCpolSel.value);
    const sCpha = parseInt(sCphaSel.value);

    const cpolOk = (mCpol === sCpol);
    const cphaOk = (mCpha === sCpha);
    const agreementOk = cpolOk && cphaOk;

    const cpolIcon = cpolOk ? "✓" : "✗";
    const cpolClass = cpolOk ? "agreement-ok" : "agreement-fail";
    const cphaIcon = cphaOk ? "✓" : "✗";
    const cphaClass = cphaOk ? "agreement-ok" : "agreement-fail";

    agreementContainer.innerHTML = `
      <div class="agreement-item ${cpolClass}">${cpolIcon} Clock Polarity: Master=${mCpol} vs Slave=${sCpol}</div>
      <div class="agreement-item ${cphaClass}">${cphaIcon} Clock Phase: Master=${mCpha} vs Slave=${sCpha}</div>
      ${agreementOk ? 
        `<div class="agreement-item agreement-ok" style="font-weight:bold;text-align:center;">✓ Bus Synchronized (Mode ${(mCpol << 1) | mCpha})</div>` : 
        `<div class="agreement-item agreement-fail" style="font-weight:bold;text-align:center;">✗ Phase Mismatch Detected!</div>`}
    `;

    const activeChar = message.length > 0 ? message[0] : ' ';
    const charCode = activeChar.charCodeAt(0);
    const txBits = [];
    for (let b = 0; b < 8; b++) {
      txBits.push((charCode >> (7 - b)) & 1);
    }

    const x_edges = [];
    for (let i = 0; i < 16; i++) {
      x_edges.push(135 + i * 35);
    }

    const slaveSampleXs = [];
    if (sCpha === 0) {
      for (let i = 0; i < 16; i += 2) {
        slaveSampleXs.push(x_edges[i]);
      }
    } else {
      for (let i = 1; i < 16; i += 2) {
        slaveSampleXs.push(x_edges[i]);
      }
    }

    const svgW = 900;
    const svgH = 230;
    const padLeft = 80;
    const svgBlocks = [];

    // CS Line
    const csYHigh = 30;
    const csYLow = 45;
    const csPath = `M 0,${csYHigh} L 100,${csYHigh} L 100,${csYLow} L 695,${csYLow} L 695,${csYHigh} L ${svgW},${csYHigh}`;
    svgBlocks.push(`<path d="${csPath}" fill="none" stroke="#F59E0B" stroke-width="2" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${csYLow - 2}" fill="#F59E0B" font-family="var(--mono)" font-size="8" text-anchor="end">CS</text>`);

    // SCLK Line
    const sclkYHigh = 70;
    const sclkYLow = 90;
    const sclkIdle = mCpol === 1 ? sclkYHigh : sclkYLow;
    const sclkActive = mCpol === 1 ? sclkYLow : sclkYHigh;

    let sclkPath = `M 0,${sclkIdle} L 135,${sclkIdle}`;
    let currY = sclkIdle;
    x_edges.forEach(x => {
      const nextY = currY === sclkIdle ? sclkActive : sclkIdle;
      sclkPath += ` L ${x},${currY} L ${x},${nextY}`;
      currY = nextY;
    });
    sclkPath += ` L ${svgW},${sclkIdle}`;
    svgBlocks.push(`<path d="${sclkPath}" fill="none" stroke="#3B82F6" stroke-width="2" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${sclkYLow - 2}" fill="#3B82F6" font-family="var(--mono)" font-size="8" text-anchor="end">SCLK</text>`);

    // MOSI Waveform
    const mosiYHigh = 115;
    const mosiYLow = 135;
    let mosiPath = `M 0,${mosiYHigh} L 100,${mosiYHigh}`;
    const mosiSegments = [];
    if (mCpha === 0) {
      mosiSegments.push([100, 170, txBits[0]]);
      for (let b = 1; b < 8; b++) {
        mosiSegments.push([170 + (b - 1) * 70, 170 + b * 70, txBits[b]]);
      }
      mosiSegments.push([660, svgW, 1]);
    } else {
      mosiSegments.push([100, 135, 1]);
      for (let b = 0; b < 8; b++) {
        mosiSegments.push([135 + b * 70, 135 + (b + 1) * 70, txBits[b]]);
      }
      mosiSegments.push([695, svgW, 1]);
    }

    mosiSegments.forEach(([start_x, end_x, val]) => {
      const yVal = val === 1 ? mosiYHigh : mosiYLow;
      mosiPath += ` L ${start_x},${yVal} L ${end_x},${yVal}`;
    });
    svgBlocks.push(`<path d="${mosiPath}" fill="none" stroke="#FFFFFF" stroke-width="2" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${mosiYLow - 2}" fill="#FFFFFF" font-family="var(--mono)" font-size="8" text-anchor="end">MOSI</text>`);

    // MISO Waveform
    const misoBits = [0, 1, 0, 1, 1, 0, 1, 0];
    const misoYHigh = 160;
    const misoYLow = 180;
    let misoPath = `M 0,${misoYHigh} L 100,${misoYHigh}`;
    const misoSegments = [];
    if (mCpha === 0) {
      misoSegments.push([100, 170, misoBits[0]]);
      for (let b = 1; b < 8; b++) {
        misoSegments.push([170 + (b - 1) * 70, 170 + b * 70, misoBits[b]]);
      }
      misoSegments.push([660, svgW, 1]);
    } else {
      misoSegments.push([100, 135, 1]);
      for (let b = 0; b < 8; b++) {
        misoSegments.push([135 + b * 70, 135 + (b + 1) * 70, misoBits[b]]);
      }
      misoSegments.push([695, svgW, 1]);
    }

    misoSegments.forEach(([start_x, end_x, val]) => {
      const yVal = val === 1 ? misoYHigh : misoYLow;
      misoPath += ` L ${start_x},${yVal} L ${end_x},${yVal}`;
    });
    svgBlocks.push(`<path d="${misoPath}" fill="none" stroke="#10B981" stroke-width="2" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${misoYLow - 2}" fill="#10B981" font-family="var(--mono)" font-size="8" text-anchor="end">MISO</text>`);

    // Draw Slave Sampling Ticks
    slaveSampleXs.forEach((xs, idx) => {
      if (animStep >= idx * 2 + 1) {
        const color = agreementOk ? "#10B981" : "#EF6868";
        const dash = agreementOk ? "2,2" : "1,2";
        let sampledVal = 1;
        for (let s = 0; s < mosiSegments.length; s++) {
          const [start_x, end_x, val] = mosiSegments[s];
          if (xs >= start_x && xs <= end_x) {
            sampledVal = val;
            break;
          }
        }
        svgBlocks.push(`<line x1="${xs}" y1="50" x2="${xs}" y2="200" stroke="${color}" stroke-dasharray="${dash}" stroke-width="1" />`);
        svgBlocks.push(`<circle cx="${xs}" cy="${sCpol === 1 ? sclkYHigh : sclkYLow}" r="3" fill="${color}" />`);
        svgBlocks.push(`<circle cx="${xs}" cy="${sampledVal === 1 ? mosiYHigh : mosiYLow}" r="3.5" fill="${color}" stroke="#0F172A" />`);
        svgBlocks.push(`<text x="${xs}" y="215" fill="${color}" font-family="var(--mono)" font-size="8" text-anchor="middle" font-weight="bold">S${idx}(${sampledVal})</text>`);
      }
    });

    // Time Sweep Cursor
    if (animating && animStep < 18) {
      const cursorX = 100 + animStep * 35;
      svgBlocks.push(`<line x1="${cursorX}" y1="15" x2="${cursorX}" y2="200" stroke="#3B82F6" stroke-width="1.5" />`);
    }

    waveformContainer.innerHTML = `<svg viewBox="0 0 ${svgW} ${svgH}" width="100%">${svgBlocks.join('')}</svg>`;

    // Compute Slave RX Register Bits
    const rxRegisterBits = ["_", "_", "_", "_", "_", "_", "_", "_"];
    for (let idx = 0; idx < 8; idx++) {
      if (animStep >= idx * 2 + 1) {
        const xs = slaveSampleXs[idx];
        let sampledVal = 0;
        for (let s = 0; s < mosiSegments.length; s++) {
          const [start_x, end_x, val] = mosiSegments[s];
          if (xs >= start_x && xs <= end_x) {
            sampledVal = val;
            break;
          }
        }
        rxRegisterBits[idx] = String(sampledVal);
      }
    }

    let cellsHtml = "";
    rxRegisterBits.forEach((bit, idx) => {
      let cls = "register-cell";
      if (bit !== "_") {
        cls += agreementOk ? " fifo-active-rx" : " fifo-active";
      }
      cellsHtml += `
        <div class="${cls}" style="display:inline-block; margin-right:0.25rem;">
          <div class="register-label">D${7 - idx}</div>
          <div class="register-val">${bit}</div>
        </div>
      `;
    });
    rxRegisterContainer.innerHTML = cellsHtml;

    // Logs
    const logs = ["[0.0ms] Master asserts CS low... Starting SPI transaction."];
    if (animStep >= 1) {
      logs.push(`[0.2ms] SCLK active. Polarity Idle=${mCpol === 1 ? 'High' : 'Low'}. Phase CPHA=${mCpha}.`);
    }
    for (let idx = 0; idx < 8; idx++) {
      if (animStep >= idx * 2 + 1) {
        const xs = slaveSampleXs[idx];
        let val = 0;
        for (let s = 0; s < mosiSegments.length; s++) {
          const [start_x, end_x, v] = mosiSegments[s];
          if (xs >= start_x && xs <= end_x) {
            val = v;
            break;
          }
        }
        const edgeType = (idx % 2 === 0) ? (sCpha === 0 ? "leading" : "trailing") : (sCpha === 0 ? "trailing" : "leading");
        const edgeDirection = (mCpol === 0) ? (edgeType === "leading" ? "rising" : "falling") : (edgeType === "leading" ? "falling" : "rising");
        
        logs.push(`[Bit ${7 - idx}] Slave samples MOSI on ${edgeDirection} edge -> Read ${val}.`);
        if (!agreementOk) {
          logs.push(`[WARNING] Timing mismatch! Slave sampled on unstable boundary.`);
        }
      }
    }
    if (animStep >= 16) {
      logs.push("[2.8ms] SCLK clock train finishes.");
      logs.push("[3.0ms] Master deasserts CS High... Transaction closed.");
      if (agreementOk) {
        logs.push("[SUCCESS] Bus alignment clean. Data verified.");
      } else {
        logs.push("[FAIL] Phase mismatch. Slave sampled transitions. Bits corrupted.");
      }
    }
    logContainer.innerHTML = logs.join('<br>');
    logContainer.scrollTop = logContainer.scrollHeight;

    // Outcome
    let recoveredStr = "";
    if (animStep >= 16) {
      if (agreementOk) {
        recoveredStr = message;
      } else {
        for (let i = 0; i < message.length; i++) {
          const val = message.charCodeAt(i);
          let recVal = val;
          if (mCpha !== sCpha && mCpol === sCpol) {
            recVal = (val << 1) & 0xFF;
          } else if (mCpol !== sCpol && mCpha === sCpha) {
            recVal = (val >> 1) & 0xFF;
          } else {
            recVal = (~val) & 0xFF;
          }
          recoveredStr += (recVal >= 32 && recVal <= 126) ? String.fromCharCode(recVal) : "?";
        }
      }
    } else {
      recoveredStr = "...";
    }

    outcomeContainer.innerHTML = `
      <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.5rem; font-family:var(--mono); margin-top:0.4rem;">
        <div>
          <span style="color:var(--muted); font-size:0.65rem; display:block;">TX DATA</span>
          <span style="font-weight:bold; font-size:1.1rem; color:#FFF;">${escHtml(message)}</span>
        </div>
        <div>
          <span style="color:var(--muted); font-size:0.65rem; display:block;">RX RECOVERED</span>
          <span style="font-weight:bold; font-size:1.1rem; color:${agreementOk ? '#10B981' : '#EF6868'};">${escHtml(recoveredStr)}</span>
        </div>
      </div>
    `;
  }
}

function renderSpiSilentConversation() {
  const container = document.getElementById('spi-silent-conversation');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Silent Conversation</div>
    <div class="edgecase-subheader">Chip Select Contention & Tri-State Collisions</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Toggle individual Chip Select lines to observe normal addressing, floating high lines, and physical electrical contention on the shared MISO bus.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Bus Selection Control</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap:1rem;">
        <div>
          <div class="panel-title" style="color:#10B981; font-size:0.8rem; margin-bottom:0.4rem;">Flash Memory</div>
          <div style="display:flex; align-items:center; gap:0.4rem;">
            <input type="checkbox" id="ec-sc-flash" class="edgecase-checkbox" style="cursor:pointer;">
            <label for="ec-sc-flash" style="font-family:var(--mono); font-size:0.7rem; color:var(--text); cursor:pointer;">Assert CS0</label>
          </div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.25rem; font-family:var(--mono);">Responds: 0xA5 (10100101)</div>
        </div>
        <div>
          <div class="panel-title" style="color:#3B82F6; font-size:0.8rem; margin-bottom:0.4rem;">Temp Sensor</div>
          <div style="display:flex; align-items:center; gap:0.4rem;">
            <input type="checkbox" id="ec-sc-sensor" class="edgecase-checkbox" style="cursor:pointer;">
            <label for="ec-sc-sensor" style="font-family:var(--mono); font-size:0.7rem; color:var(--text); cursor:pointer;">Assert CS1</label>
          </div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.25rem; font-family:var(--mono);">Responds: 0x3C (00111100)</div>
        </div>
        <div>
          <div class="panel-title" style="color:#F59E0B; font-size:0.8rem; margin-bottom:0.4rem;">ADC Converter</div>
          <div style="display:flex; align-items:center; gap:0.4rem;">
            <input type="checkbox" id="ec-sc-adc" class="edgecase-checkbox" style="cursor:pointer;">
            <label for="ec-sc-adc" style="font-family:var(--mono); font-size:0.7rem; color:var(--text); cursor:pointer;">Assert CS2</label>
          </div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.25rem; font-family:var(--mono);">Responds: 0x5A (01011010)</div>
        </div>
        <div>
          <div class="panel-title" style="color:#EC4899; font-size:0.8rem; margin-bottom:0.4rem;">OLED Display</div>
          <div style="display:flex; align-items:center; gap:0.4rem;">
            <input type="checkbox" id="ec-sc-display" class="edgecase-checkbox" style="cursor:pointer;">
            <label for="ec-sc-display" style="font-family:var(--mono); font-size:0.7rem; color:var(--text); cursor:pointer;">Assert CS3</label>
          </div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.25rem; font-family:var(--mono);">Responds: 0xF0 (11110000)</div>
        </div>
      </div>
    </div>

    <!-- SYSTEM STATUS -->
    <div class="pipeline-step">System Status</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: 3fr 1fr; gap:1rem; align-items:center;">
        <div id="ec-sc-status-container"></div>
        <button id="ec-sc-transmit-btn" class="edgecase-button" style="margin:0; width:100%; height:38px;">RUN SIMULATION</button>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Physical Waveform Trace (Shared Bus State)</div>
    <div class="edgecase-visual" id="ec-sc-waveform-container" style="background:#0F172A; min-height:240px; position:relative;"></div>

    <!-- OUTPUT PANELS -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-top:1.5rem;">
      <div>
        <div class="pipeline-step">Bus Logging Terminal</div>
        <div id="ec-sc-log" class="terminal-box"></div>
      </div>
      <div>
        <div class="pipeline-step">Electrical Bus Status</div>
        <div class="panel-box" id="ec-sc-electrical-status" style="height:200px; display:flex; flex-direction:column; justify-content:center; gap:0.5rem; box-sizing:border-box;"></div>
      </div>
    </div>
  `;

  // DOM elements
  const flashCb = document.getElementById('ec-sc-flash');
  const sensorCb = document.getElementById('ec-sc-sensor');
  const adcCb = document.getElementById('ec-sc-adc');
  const displayCb = document.getElementById('ec-sc-display');
  const transmitBtn = document.getElementById('ec-sc-transmit-btn');

  const statusContainer = document.getElementById('ec-sc-status-container');
  const waveformContainer = document.getElementById('ec-sc-waveform-container');
  const logContainer = document.getElementById('ec-sc-log');
  const electricalStatus = document.getElementById('ec-sc-electrical-status');

  let animating = false;
  let animStep = 20;

  const checkboxes = [flashCb, sensorCb, adcCb, displayCb];
  checkboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      updateUi();
    });
  });

  transmitBtn.addEventListener('click', async () => {
    if (animating) return;
    animating = true;
    animStep = 0;
    for (let step = 0; step <= 16; step++) {
      animStep = step;
      updateUi();
      await new Promise(resolve => setTimeout(resolve, 120));
    }
    animating = false;
    animStep = 20;
    updateUi();
  });

  updateUi();

  function updateUi() {
    const flashActive = flashCb.checked;
    const sensorActive = sensorCb.checked;
    const adcActive = adcCb.checked;
    const displayActive = displayCb.checked;

    const assertedDevices = [];
    if (flashActive) assertedDevices.push("Flash");
    if (sensorActive) assertedDevices.push("Sensor");
    if (adcActive) assertedDevices.push("ADC");
    if (displayActive) assertedDevices.push("Display");

    const numAsserted = assertedDevices.length;

    // Render Status
    if (numAsserted === 0) {
      statusContainer.innerHTML = `<div class="agreement-item agreement-warning" style="font-weight:bold;text-align:center;font-size:0.9rem;margin:0;">⚠️ Bus Idle (Floating Tri-State). MISO Reads 0xFF (Pull-up).</div>`;
    } else if (numAsserted === 1) {
      statusContainer.innerHTML = `<div class="agreement-item agreement-ok" style="font-weight:bold;text-align:center;font-size:0.9rem;margin:0;">✓ Active Slave: ${assertedDevices[0]} (Single Device Driving MISO)</div>`;
    } else {
      statusContainer.innerHTML = `<div class="agreement-item agreement-fail" style="font-weight:bold;text-align:center;font-size:0.9rem;margin:0;">💥 CRITICAL: BUS CONTENTION! Multiple Slaves driving MISO: ${assertedDevices.join(' & ')}</div>`;
    }

    const deviceBits = {
      "Flash": [1, 0, 1, 0, 0, 1, 0, 1],
      "Sensor": [0, 0, 1, 1, 1, 1, 0, 0],
      "ADC": [0, 1, 0, 1, 1, 0, 1, 0],
      "Display": [1, 1, 1, 1, 0, 0, 0, 0]
    };

    const misoDisplayBits = [];
    for (let bitIdx = 0; bitIdx < 8; bitIdx++) {
      const drivenValues = [];
      assertedDevices.forEach(dev => {
        drivenValues.push(deviceBits[dev][bitIdx]);
      });

      if (numAsserted === 0) {
        misoDisplayBits.push(1);
      } else if (numAsserted === 1) {
        misoDisplayBits.push(drivenValues[0]);
      } else {
        const uniqueVals = Array.from(new Set(drivenValues));
        if (uniqueVals.length === 1) {
          misoDisplayBits.push(drivenValues[0]);
        } else {
          misoDisplayBits.push("X");
        }
      }
    }

    const svgW = 950;
    const svgH = 240;
    const padLeft = 110;
    const xEdges = [];
    for (let i = 0; i < 16; i++) {
      xEdges.push(padLeft + 45 + i * 35);
    }

    const svgBlocks = [];

    // CS lines
    const cs0Color = flashActive ? "#10B981" : "#475569";
    const cs0Y = 20;
    const cs0Path = `M ${padLeft},${cs0Y} L ${xEdges[0]},${cs0Y} L ${xEdges[0]},${cs0Y + (flashActive ? 10 : 0)} L ${xEdges[14]},${cs0Y + (flashActive ? 10 : 0)} L ${xEdges[14]},${cs0Y} L ${svgW},${cs0Y}`;
    svgBlocks.push(`<path d="${cs0Path}" fill="none" stroke="${cs0Color}" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${cs0Y + 3}" fill="${cs0Color}" font-family="var(--mono)" font-size="8" text-anchor="end">CS_Flash (CS0)</text>`);

    const cs1Color = sensorActive ? "#3B82F6" : "#475569";
    const cs1Y = 45;
    const cs1Path = `M ${padLeft},${cs1Y} L ${xEdges[0]},${cs1Y} L ${xEdges[0]},${cs1Y + (sensorActive ? 10 : 0)} L ${xEdges[14]},${cs1Y + (sensorActive ? 10 : 0)} L ${xEdges[14]},${cs1Y} L ${svgW},${cs1Y}`;
    svgBlocks.push(`<path d="${cs1Path}" fill="none" stroke="${cs1Color}" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${cs1Y + 3}" fill="${cs1Color}" font-family="var(--mono)" font-size="8" text-anchor="end">CS_Sensor (CS1)</text>`);

    const cs2Color = adcActive ? "#F59E0B" : "#475569";
    const cs2Y = 70;
    const cs2Path = `M ${padLeft},${cs2Y} L ${xEdges[0]},${cs2Y} L ${xEdges[0]},${cs2Y + (adcActive ? 10 : 0)} L ${xEdges[14]},${cs2Y + (adcActive ? 10 : 0)} L ${xEdges[14]},${cs2Y} L ${svgW},${cs2Y}`;
    svgBlocks.push(`<path d="${cs2Path}" fill="none" stroke="${cs2Color}" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${cs2Y + 3}" fill="${cs2Color}" font-family="var(--mono)" font-size="8" text-anchor="end">CS_ADC (CS2)</text>`);

    const cs3Color = displayActive ? "#EC4899" : "#475569";
    const cs3Y = 95;
    const cs3Path = `M ${padLeft},${cs3Y} L ${xEdges[0]},${cs3Y} L ${xEdges[0]},${cs3Y + (displayActive ? 10 : 0)} L ${xEdges[14]},${cs3Y + (displayActive ? 10 : 0)} L ${xEdges[14]},${cs3Y} L ${svgW},${cs3Y}`;
    svgBlocks.push(`<path d="${cs3Path}" fill="none" stroke="${cs3Color}" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${cs3Y + 3}" fill="${cs3Color}" font-family="var(--mono)" font-size="8" text-anchor="end">CS_Display (CS3)</text>`);

    // SCLK
    const sclkYHigh = 120;
    const sclkYLow = 135;
    let sclkPath = `M 0,${sclkYLow} L ${xEdges[0]},${sclkYLow}`;
    let currY = sclkYLow;
    for (let i = 0; i < 14; i++) {
      const nextY = currY === sclkYLow ? sclkYHigh : sclkYLow;
      sclkPath += ` L ${xEdges[i]},${currY} L ${xEdges[i]},${nextY}`;
      currY = nextY;
    }
    sclkPath += ` L ${svgW},${sclkYLow}`;
    svgBlocks.push(`<path d="${sclkPath}" fill="none" stroke="#6366F1" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${sclkYLow - 2}" fill="#6366F1" font-family="var(--mono)" font-size="8" text-anchor="end">SCLK (Clock)</text>`);

    // MOSI
    const mosiYHigh = 155;
    const mosiYLow = 170;
    let mosiPath = `M 0,${mosiYLow} L ${xEdges[0]},${mosiYLow}`;
    for (let i = 0; i < 8; i++) {
      const yVal = (i % 2 === 0) ? mosiYHigh : mosiYLow;
      mosiPath += ` L ${xEdges[2 * i]},${yVal} L ${xEdges[2 * i + 1]},${yVal}`;
    }
    mosiPath += ` L ${svgW},${mosiYLow}`;
    svgBlocks.push(`<path d="${mosiPath}" fill="none" stroke="#94A3B8" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${mosiYLow - 2}" fill="#94A3B8" font-family="var(--mono)" font-size="8" text-anchor="end">MOSI (Data Out)</text>`);

    // MISO
    const misoYHigh = 190;
    const misoYLow = 205;
    const misoYMid = 197.5;
    const misoStartColor = numAsserted <= 1 ? (numAsserted === 0 ? "#F59E0B" : "#10B981") : "#EF6868";

    for (let i = 0; i < 8; i++) {
      const val = misoDisplayBits[i];
      const xStart = xEdges[2 * i];
      const xEnd = xEdges[2 * i + 1];

      if (val === 1) {
        svgBlocks.push(`<path d="M ${xStart},${misoYHigh} L ${xEnd},${misoYHigh}" fill="none" stroke="#10B981" stroke-width="2" />`);
      } else if (val === 0) {
        svgBlocks.push(`<path d="M ${xStart},${misoYLow} L ${xEnd},${misoYLow}" fill="none" stroke="#10B981" stroke-width="2" />`);
      } else if (val === "X") {
        svgBlocks.push(`
          <path d="M ${xStart},${misoYHigh} L ${xEnd},${misoYHigh}" fill="none" stroke="#EF6868" stroke-width="2" />
          <path d="M ${xStart},${misoYLow} L ${xEnd},${misoYLow}" fill="none" stroke="#EF6868" stroke-width="2" />
          <path d="M ${xStart},${misoYHigh} L ${xEnd},${misoYLow}" fill="none" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="2,2" />
          <path d="M ${xStart},${misoYLow} L ${xEnd},${misoYHigh}" fill="none" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="2,2" />
          <rect x="${xStart}" y="${misoYHigh}" width="${xEnd - xStart}" height="${misoYLow - misoYHigh}" fill="rgba(239, 104, 104, 0.15)" />
          <text x="${(xStart + xEnd) / 2}" y="${misoYMid + 3}" fill="#EF6868" font-family="var(--mono)" font-size="8" font-weight="bold" text-anchor="middle">CONFLICT</text>
        `);
      }
    }

    for (let i = 0; i < 7; i++) {
      const xMidStart = xEdges[2 * i + 1];
      const xMidEnd = xEdges[2 * i + 2];
      const valPrev = misoDisplayBits[i];
      const valNext = misoDisplayBits[i + 1];

      const y1 = (valPrev === 1 || valPrev === "X") ? misoYHigh : misoYLow;
      const y2 = (valNext === 1 || valNext === "X") ? misoYHigh : misoYLow;
      const color = (valPrev === "X" || valNext === "X") ? "#EF6868" : "#10B981";

      svgBlocks.push(`<path d="M ${xMidStart},${y1} L ${xMidEnd},${y2}" fill="none" stroke="${color}" stroke-width="2" />`);
    }

    svgBlocks.push(`<path d="M 0,${misoYHigh} L ${xEdges[0]},${misoYHigh}" fill="none" stroke="${misoStartColor}" stroke-width="1.5" />`);
    const yLast = (misoDisplayBits[7] === 1 || misoDisplayBits[7] === "X") ? misoYHigh : misoYLow;
    svgBlocks.push(`<path d="M ${xEdges[15]},${yLast} L ${svgW},${yLast}" fill="none" stroke="${misoStartColor}" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${misoYLow - 2}" fill="${misoStartColor}" font-family="var(--mono)" font-size="8" text-anchor="end">MISO (Data In)</text>`);

    if (animating && animStep < 16) {
      const cursorX = xEdges[0] + animStep * 35;
      svgBlocks.push(`<line x1="${cursorX}" y1="10" x2="${cursorX}" y2="225" stroke="#3B82F6" stroke-width="1.5" />`);
    }

    waveformContainer.innerHTML = `<svg viewBox="0 0 ${svgW} ${svgH}" width="100%">${svgBlocks.join('')}</svg>`;

    // Logging Terminal
    const logs = [];
    if (numAsserted === 0) {
      logs.push("[0.0ms] Master pulls all CS lines High (deasserted).");
      logs.push("[0.2ms] SCLK active, driving 8 clock pulses.");
      logs.push("[0.5ms] MISO wire is placed in high-impedance (tri-state) mode by all slaves.");
      logs.push("[0.8ms] Physical bus pull-up resistor pulls MISO voltage up to VCC (+3.3V).");
      for (let idx = 0; idx < 8; idx++) {
        if (animStep >= idx * 2) {
          logs.push(`[Bit ${7 - idx}] Master samples MISO High -> Read 1 (Tri-stated).`);
        }
      }
      if (animStep >= 16) {
        logs.push("[2.5ms] Clock pulses complete. Transaction ended.");
        logs.push("[Outcome] Master successfully read 0xFF (tri-stated bus).");
      }
    } else if (numAsserted === 1) {
      const devName = assertedDevices[0];
      const devHex = devName === "Flash" ? "0xA5" : (devName === "Sensor" ? "0x3C" : (devName === "ADC" ? "0x5A" : "0xF0"));
      logs.push(`[0.0ms] Master pulls CS_${devName} Low (asserted). All other CS lines remain High.`);
      logs.push(`[0.2ms] peripheral '${devName}' wakes up, enables output driver on MISO trace.`);
      logs.push("[0.4ms] SCLK clock line begins pulsing.");
      for (let idx = 0; idx < 8; idx++) {
        if (animStep >= idx * 2) {
          const val = deviceBits[devName][idx];
          logs.push(`[Bit ${7 - idx}] ${devName} drives MISO: ${val} -> Master samples: ${val}.`);
        }
      }
      if (animStep >= 16) {
        logs.push("[2.5ms] Clock pulses complete. CS deasserted.");
        logs.push(`[Outcome] Communication clean. Master successfully read ${devHex} from ${devName}.`);
      }
    } else {
      const conflictNames = assertedDevices.slice(0, -1).join(', ') + " and " + assertedDevices[assertedDevices.length - 1];
      logs.push(`[CRITICAL] Master asserts multiple CS lines simultaneously: ${conflictNames}!`);
      logs.push("[0.1ms] Multiple output drivers enabled on the shared MISO physical trace.");
      logs.push("[0.2ms] SCLK begins pulsing. Peripherals attempt to transmit concurrent bytes.");
      for (let idx = 0; idx < 8; idx++) {
        if (animStep >= idx * 2) {
          const vals = assertedDevices.map(dev => deviceBits[dev][idx]);
          const uniqueVals = Array.from(new Set(vals));
          if (uniqueVals.length === 1) {
            logs.push(`[Bit ${7 - idx}] All devices driving ${vals[0]} -> Master samples: ${vals[0]} (No collision).`);
          } else {
            const details = assertedDevices.map(dev => `${dev[0]}=${deviceBits[dev][idx]}`).join(' vs ');
            logs.push(`[COLLISION] Bit ${7 - idx} conflict: ${details}.`);
            logs.push(`            MISO line voltage collapses. Logic state indeterminate.`);
          }
        }
      }
      if (animStep >= 16) {
        logs.push("[2.5ms] Transaction terminated.");
        logs.push("[CRITICAL] Bus contention caused short circuits. Current spike > 50mA recorded.");
        logs.push("[CRITICAL] Data read is corrupted/indeterminate. High hardware damage risk!");
      }
    }

    logContainer.innerHTML = logs.join('<br>');
    logContainer.scrollTop = logContainer.scrollHeight;

    // Electrical Status
    if (numAsserted === 0) {
      electricalStatus.innerHTML = `
        <div style="font-family:var(--mono); font-size:0.75rem; color:var(--muted);">MISO BUS VOLTAGE LEVEL:</div>
        <div style="font-family:var(--mono); font-size:1.4rem; color:#F59E0B; font-weight:bold;">~ 3.3V (Tri-State Pull-Up)</div>
        <div style="font-family:var(--mono); font-size:0.7rem; color:#A5F3FC; line-height:1.4;">Current consumption: 0.0mA (Min)<br>Recovered Byte: 0xFF (Idle)</div>
      `;
    } else if (numAsserted === 1) {
      const dev = assertedDevices[0];
      const devHex = dev === "Flash" ? "0xA5" : (dev === "Sensor" ? "0x3C" : (dev === "ADC" ? "0x5A" : "0xF0"));
      electricalStatus.innerHTML = `
        <div style="font-family:var(--mono); font-size:0.75rem; color:var(--muted);">MISO BUS VOLTAGE (${dev}):</div>
        <div style="font-family:var(--mono); font-size:1.4rem; color:#10B981; font-weight:bold;">Clean Digital 0V / 3.3V Transitions</div>
        <div style="font-family:var(--mono); font-size:0.7rem; color:#A5F3FC; line-height:1.4;">Current consumption: ~1.2mA (Nominal)<br>Recovered Byte: ${devHex}</div>
      `;
    } else {
      electricalStatus.innerHTML = `
        <div style="font-family:var(--mono); font-size:0.75rem; color:#EF6868; font-weight:bold;">⚠️ ELECTRICAL HAZARD: SHORT CIRCUIT</div>
        <div style="font-family:var(--mono); font-size:1.4rem; color:#EF6868; font-weight:bold;">~ 1.6V Intermediate (Contention)</div>
        <div style="font-family:var(--mono); font-size:0.7rem; color:#EF6868; line-height:1.4;">Current consumption: &gt; 48.5mA (EXCESSIVE HEAT)<br>Recovered Byte: ERROR / GARBAGE</div>
      `;
    }
  }
}

function renderI2cSharedBus() {
  const container = document.getElementById('i2c-shared-bus');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Shared Bus</div>
    <div class="edgecase-subheader">Watch an I2C conversation unfold.</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Select a peripheral transaction and toggle device responsiveness to see how addressing, START/STOP conditions, and ACK/NACK signaling operate.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Transaction Selector</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1.5rem;">
        <!-- Option Column -->
        <div>
          <div class="panel-title" style="color:var(--blue); font-size:0.85rem; margin-bottom:0.75rem;">Transaction Select</div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-i2c-op" style="font-size:0.7rem;">Target Peripheral Operation</label>
            <select id="ec-i2c-op" class="edgecase-select">
              <option value="temp" selected>Read Temp Sensor (Address 0x48)</option>
              <option value="eeprom">Write EEPROM (Address 0x50, Data 0x3F)</option>
              <option value="oled">Write OLED Display (Address 0x3C, Cmd 0xAF)</option>
            </select>
          </div>
        </div>

        <!-- Responsiveness Column -->
        <div>
          <div class="panel-title" style="color:#E2E8F0; font-size:0.85rem; margin-bottom:0.75rem;">Device Presence</div>
          <div style="display:flex; align-items:center; gap:0.4rem; height:45px;">
            <input type="checkbox" id="ec-i2c-ack" class="edgecase-checkbox" checked style="cursor:pointer;">
            <label for="ec-i2c-ack" style="font-family:var(--mono); font-size:0.75rem; color:var(--text); cursor:pointer;">Target Device Responding (ACK)</label>
          </div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.25rem; font-family:var(--mono);">Uncheck to simulate NACK error.</div>
        </div>

        <!-- Agreement Column -->
        <div>
          <div class="panel-title" style="color:#10B981; font-size:0.85rem; margin-bottom:0.75rem;">Physical Bus Mode</div>
          <div id="ec-i2c-mode-status"></div>
        </div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="pipeline-step">System Controls</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: 3fr 1fr; gap:1rem; align-items:center;">
        <div style="font-size:0.75rem; color:var(--text); font-family:var(--mono);" id="ec-i2c-instruction-preview"></div>
        <button id="ec-i2c-transmit-btn" class="edgecase-button" style="margin:0; width:100%; height:38px;">TRANSMIT</button>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Physical Waveform Trace (Shared SDA / SCL Lines)</div>
    <div class="edgecase-visual" id="ec-i2c-waveform-container" style="background:#0F172A; min-height:190px; position:relative;"></div>

    <!-- OUTPUT PANELS -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-top:1.5rem;">
      <div>
        <div class="pipeline-step">Protocol Transaction Log</div>
        <div id="ec-i2c-log" class="terminal-box"></div>
      </div>
      <div>
        <div class="pipeline-step">Data Recovery Outcome</div>
        <div class="panel-box" style="height:200px; display:flex; flex-direction:column; justify-content:center; gap:0.5rem; box-sizing:border-box;">
          <div style="font-family:var(--mono); font-size:0.65rem; color:var(--muted); text-transform:uppercase;">Shift Register (Input Buffer):</div>
          <div id="ec-i2c-rx-register" class="register-container" style="margin:0;"></div>
          <div id="ec-i2c-outcome" style="margin-top:0.4rem;"></div>
        </div>
      </div>
    </div>
  `;

  // DOM elements
  const opSel = document.getElementById('ec-i2c-op');
  const ackCb = document.getElementById('ec-i2c-ack');
  const transmitBtn = document.getElementById('ec-i2c-transmit-btn');

  const modeStatus = document.getElementById('ec-i2c-mode-status');
  const instructionPreview = document.getElementById('ec-i2c-instruction-preview');
  const waveformContainer = document.getElementById('ec-i2c-waveform-container');
  const logContainer = document.getElementById('ec-i2c-log');
  const rxRegisterContainer = document.getElementById('ec-i2c-rx-register');
  const outcomeContainer = document.getElementById('ec-i2c-outcome');

  let animating = false;
  let animStep = 22;

  opSel.addEventListener('change', () => {
    updateUi();
  });

  ackCb.addEventListener('change', () => {
    updateUi();
  });

  transmitBtn.addEventListener('click', async () => {
    if (animating) return;
    animating = true;
    animStep = 0;

    const op = opSel.value;
    const isResponding = ackCb.checked;
    
    // Total steps to run: 
    // If NACKed on address: 12 steps (START + 8 address/RW bits + 1 NACK bit + 2 STOP steps)
    // If ACKed: 22 steps (START + 8 address/RW bits + 1 ACK bit + 8 data bits + 1 Master ACK bit + 3 STOP steps)
    const maxSteps = isResponding ? 22 : 12;

    for (let step = 0; step <= maxSteps; step++) {
      animStep = step;
      updateUi();
      await new Promise(resolve => setTimeout(resolve, 140));
    }

    animating = false;
    animStep = 22;
    updateUi();
  });

  updateUi();

  function updateUi() {
    const op = opSel.value;
    const isResponding = ackCb.checked;

    // Address & parameters
    let addr = 0x48;
    let rwb = 1; // Read
    let dataByte = 0x2C; // 28 degC
    let desc = "";

    if (op === "temp") {
      addr = 0x48;
      rwb = 1;
      dataByte = 0x2C;
      desc = "Instruction: i2c_read(0x48) -> Read temperature register (expect 0x2C)";
    } else if (op === "eeprom") {
      addr = 0x50;
      rwb = 0;
      dataByte = 0x3F;
      desc = "Instruction: i2c_write(0x50, 0x3F) -> Write data byte 0x3F to EEPROM memory address";
    } else if (op === "oled") {
      addr = 0x3C;
      rwb = 0;
      dataByte = 0xAF;
      desc = "Instruction: i2c_write(0x3C, 0xAF) -> Write command byte 0xAF to OLED graphics controller";
    }

    instructionPreview.innerText = desc;

    modeStatus.innerHTML = `
      <div class="agreement-item agreement-ok" style="font-weight:bold;text-align:center;margin:0;">
        Wired-AND Open-Drain Bus Active
      </div>
    `;

    // Parse bits
    // 7 address bits
    const addrBits = [];
    for (let b = 6; b >= 0; b--) {
      addrBits.push((addr >> b) & 1);
    }
    const rwBit = rwb;
    const slaveAckBit = isResponding ? 0 : 1; // Active low ACK

    // 8 data bits
    const dataBits = [];
    for (let b = 7; b >= 0; b--) {
      dataBits.push((dataByte >> b) & 1);
    }
    const masterAckBit = 0; // Master ACKs read, or slave ACKs write (always 0 for clean simulation)

    // Waveform rendering
    const svgW = 920;
    const svgH = 180;
    const padLeft = 80;
    const sclYHigh = 45;
    const sclYLow = 65;
    const sdaYHigh = 105;
    const sdaYLow = 125;

    const svgBlocks = [];

    // Calculate SCL clock pulses
    const totalPulses = isResponding ? 18 : 9;
    const xEdges = [];
    for (let p = 0; p < totalPulses; p++) {
      xEdges.push(120 + p * 35);
    }

    // 1. SCL Line
    let sclPath = `M 0,${sclYHigh} L 100,${sclYHigh}`;
    if (animStep > 0) {
      sclPath += ` L 120,${sclYHigh}`;
      for (let p = 0; p < totalPulses; p++) {
        const xs = xEdges[p];
        const xm = xs + 17.5;
        const xe = xs + 35;
        sclPath += ` L ${xs},${sclYLow} L ${xm},${sclYLow} L ${xm},${sclYHigh} L ${xe},${sclYHigh}`;
      }
      sclPath += ` L ${svgW},${sclYHigh}`;
    } else {
      sclPath += ` L ${svgW},${sclYHigh}`;
    }
    svgBlocks.push(`<path d="${sclPath}" fill="none" stroke="#3B82F6" stroke-width="2" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${sclYLow - 2}" fill="#3B82F6" font-family="var(--mono)" font-size="8" text-anchor="end">SCL (Clock)</text>`);

    // 2. SDA Line
    let sdaPath = `M 0,${sdaYHigh}`;
    if (animStep > 0) {
      // START transition
      sdaPath += ` L 100,${sdaYHigh} L 100,${sdaYLow} L 120,${sdaYLow}`;
      
      let currentSdaVal = 0;
      for (let p = 0; p < totalPulses; p++) {
        const xs = xEdges[p];
        const xe = xs + 35;
        
        let val = 1;
        if (p < 7) {
          val = addrBits[p];
        } else if (p === 7) {
          val = rwBit;
        } else if (p === 8) {
          val = slaveAckBit;
        } else if (p < 17) {
          val = dataBits[p - 9];
        } else if (p === 17) {
          val = masterAckBit;
        }
        
        const yVal = val === 1 ? sdaYHigh : sdaYLow;
        sdaPath += ` L ${xs},${yVal} L ${xe},${yVal}`;
        currentSdaVal = val;
      }
      
      // STOP transition
      const stopXStart = 120 + totalPulses * 35 + 10;
      const stopXEnd = stopXStart + 15;
      const stopYVal = currentSdaVal === 1 ? sdaYHigh : sdaYLow;
      sdaPath += ` L ${stopXStart},${stopYVal} L ${stopXStart},${sdaYLow} L ${stopXEnd},${sdaYHigh} L ${svgW},${sdaYHigh}`;
    } else {
      sdaPath += ` L ${svgW},${sdaYHigh}`;
    }
    svgBlocks.push(`<path d="${sdaPath}" fill="none" stroke="#10B981" stroke-width="2" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${sdaYLow - 2}" fill="#10B981" font-family="var(--mono)" font-size="8" text-anchor="end">SDA (Data)</text>`);

    // 3. Sampling markers and text
    // Draw vertical sampling ticks on SCL rising edges
    for (let p = 0; p < totalPulses; p++) {
      if (animStep >= p + 2) {
        const xs = xEdges[p] + 17.5; // rising edge is in the middle of pulse period
        let val = 1;
        if (p < 7) {
          val = addrBits[p];
        } else if (p === 7) {
          val = rwBit;
        } else if (p === 8) {
          val = slaveAckBit;
        } else if (p < 17) {
          val = dataBits[p - 9];
        } else if (p === 17) {
          val = masterAckBit;
        }

        const color = (p === 8 && !isResponding) ? "#EF6868" : "#E2E8F0";
        svgBlocks.push(`<line x1="${xs}" y1="35" x2="${xs}" y2="145" stroke="${color}" stroke-dasharray="2,2" stroke-width="0.8" />`);
        svgBlocks.push(`<circle cx="${xs}" cy="${sclYHigh}" r="2.5" fill="#3B82F6" />`);
        svgBlocks.push(`<circle cx="${xs}" cy="${val === 1 ? sdaYHigh : sdaYLow}" r="3" fill="${color}" stroke="#0F172A" />`);
        
        let label = val;
        if (p === 8) label = val === 0 ? "ACK" : "NACK";
        if (p === 17) label = "ACK";
        svgBlocks.push(`<text x="${xs}" y="156" fill="${color}" font-family="var(--mono)" font-size="7" text-anchor="middle" font-weight="bold">${label}</text>`);
      }
    }

    // Cursor
    if (animating && animStep <= totalPulses + 2) {
      let cursorX = 100;
      if (animStep === 1) cursorX = 100;
      else if (animStep >= 2 && animStep <= totalPulses + 1) {
        cursorX = xEdges[animStep - 2] + 17.5;
      } else {
        cursorX = 120 + totalPulses * 35 + 15;
      }
      svgBlocks.push(`<line x1="${cursorX}" y1="15" x2="${cursorX}" y2="155" stroke="#3B82F6" stroke-width="1.5" />`);
    }

    waveformContainer.innerHTML = `<svg viewBox="0 0 ${svgW} ${svgH}" width="100%">${svgBlocks.join('')}</svg>`;

    // Shift Register Preview
    const rxRegisterBits = ["_", "_", "_", "_", "_", "_", "_", "_"];
    if (animStep >= 2) {
      if (animStep <= 9) {
        for (let idx = 0; idx < animStep - 1; idx++) {
          rxRegisterBits[idx] = String(addrBits[idx]);
        }
      } else if (animStep === 10) {
        for (let idx = 0; idx < 7; idx++) rxRegisterBits[idx] = String(addrBits[idx]);
        rxRegisterBits[7] = String(rwBit);
      } else if (animStep >= 11 && animStep <= 19) {
        // Data bits shifting
        for (let idx = 0; idx < animStep - 11; idx++) {
          rxRegisterBits[idx] = String(dataBits[idx]);
        }
      } else {
        for (let idx = 0; idx < 8; idx++) rxRegisterBits[idx] = String(dataBits[idx]);
      }
    }

    let cellsHtml = "";
    rxRegisterBits.forEach((bit, idx) => {
      let cls = "register-cell";
      if (bit !== "_") {
        cls += isResponding ? " fifo-active-rx" : " fifo-active";
      }
      cellsHtml += `
        <div class="${cls}" style="display:inline-block; margin-right:0.25rem;">
          <div class="register-label">D${7 - idx}</div>
          <div class="register-val">${bit}</div>
        </div>
      `;
    });
    rxRegisterContainer.innerHTML = cellsHtml;

    // Logs
    const logs = ["[0.0ms] Bus Idle. SDA and SCL pulled HIGH via resistors."];
    if (animStep >= 1) {
      logs.push("[0.2ms] START Condition: SDA pulled LOW while SCL is HIGH.");
    }
    for (let p = 0; p < totalPulses; p++) {
      if (animStep >= p + 2) {
        if (p < 7) {
          logs.push(`[Address Bit ${6 - p}] Master writes address bit -> SDA = ${addrBits[p]}. sampled on SCL rise.`);
        } else if (p === 7) {
          logs.push(`[Read/Write] Master writes direction bit -> SDA = ${rwBit} (${rwBit === 1 ? 'Read' : 'Write'}).`);
        } else if (p === 8) {
          if (isResponding) {
            logs.push("[9th Clock] Handshake: Target slave pulls SDA LOW (ACK). Address verified.");
          } else {
            logs.push("[9th Clock] Handshake: SDA remains HIGH (NACK). No responding slave detected at address!");
          }
        } else if (p < 17) {
          const bitIdx = p - 9;
          const sender = rwb === 1 ? "Slave" : "Master";
          logs.push(`[Data Bit ${7 - bitIdx}] ${sender} drives SDA = ${dataBits[bitIdx]}. sampled on SCL rise.`);
        } else if (p === 17) {
          const receiver = rwb === 1 ? "Master" : "Slave";
          logs.push(`[Data Handshake] ${receiver} pulls SDA LOW (ACK) to confirm byte receipt.`);
        }
      }
    }
    if (animStep >= 20 || (animStep >= 11 && !isResponding)) {
      if (!isResponding) {
        logs.push("[2.2ms] Aborting transaction due to NACK.");
      }
      logs.push("[STOP Condition] SDA pulled LOW->HIGH while SCL is HIGH. Bus released.");
    }

    logContainer.innerHTML = logs.join('<br>');
    logContainer.scrollTop = logContainer.scrollHeight;

    // Outcome
    let recoveredStr = "";
    if (animStep >= 20) {
      recoveredStr = `Address Match! Target responding. Recovered status: Success.`;
    } else if (animStep >= 11 && !isResponding) {
      recoveredStr = `ERROR: Not Acknowledged (NACK). Address 0x${addr.toString(16).toUpperCase()} is non-existent.`;
    } else {
      recoveredStr = "...";
    }

    outcomeContainer.innerHTML = `
      <div style="font-family:var(--mono); margin-top:0.4rem; font-size:0.75rem;">
        <div>
          <span style="color:var(--muted); font-size:0.65rem; display:block;">TARGET ADDRESS</span>
          <span style="font-weight:bold; font-size:1.0rem; color:#FFF;">0x${addr.toString(16).toUpperCase()} (${rwb === 1 ? 'READ' : 'WRITE'})</span>
        </div>
        <div style="margin-top:0.4rem;">
          <span style="color:var(--muted); font-size:0.65rem; display:block;">TRANSACTION STATUS</span>
          <span style="font-weight:bold; font-size:0.9rem; color:${isResponding ? '#10B981' : '#EF6868'};">${recoveredStr}</span>
        </div>
      </div>
    `;
  }
}

function renderI2cBusArbitration() {
  const container = document.getElementById('i2c-bus-arbitration');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Polite Argument</div>
    <div class="edgecase-subheader">Multi-Master Arbitration Simulator</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      See how I2C open-drain physics enables two masters to start transmitting at the same time and resolve their conflict gracefully.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Arbitration Settings</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1.5rem;">
        <!-- Master A Column -->
        <div>
          <div class="panel-title" style="color:var(--blue); font-size:0.85rem; margin-bottom:0.75rem;">Master A Output</div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-arb-a" style="font-size:0.7rem;">Byte to Transmit</label>
            <select id="ec-arb-a" class="edgecase-select">
              <option value="0x5A" selected>0x5A (01011010)</option>
              <option value="0x6C">0x6C (01101100)</option>
              <option value="0x7F">0x7F (01111111)</option>
            </select>
          </div>
        </div>

        <!-- Master B Column -->
        <div>
          <div class="panel-title" style="color:#EC4899; font-size:0.85rem; margin-bottom:0.75rem;">Master B Output</div>
          <div class="edgecase-control-group" style="margin-bottom:0.6rem;">
            <label for="ec-arb-b" style="font-size:0.7rem;">Byte to Transmit</label>
            <select id="ec-arb-b" class="edgecase-select">
              <option value="0x5A">0x5A (01011010)</option>
              <option value="0x6C" selected>0x6C (01101100)</option>
              <option value="0x3C">0x3C (00111100)</option>
            </select>
          </div>
        </div>

        <!-- Status Column -->
        <div>
          <div class="panel-title" style="color:#10B981; font-size:0.85rem; margin-bottom:0.75rem;">Conflict Resolver</div>
          <div id="ec-arb-status" class="agreement-item" style="margin:0; text-align:center; font-weight:bold; font-size:0.8rem;"></div>
        </div>
      </div>
    </div>

    <!-- SYSTEM CONTROLS -->
    <div class="pipeline-step">System Controls</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: 3fr 1fr; gap:1rem; align-items:center;">
        <div style="font-size:0.75rem; color:var(--text); font-family:var(--mono);">
          Both masters will start transmitting simultaneously on the shared open-drain bus.
        </div>
        <button id="ec-arb-transmit-btn" class="edgecase-button" style="margin:0; width:100%; height:38px;">START ARBITRATION</button>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Physical Waveform Arbitration Trace (Shared Open-Drain Bus)</div>
    <div class="edgecase-visual" id="ec-arb-waveform-container" style="background:#0F172A; min-height:240px; position:relative;"></div>

    <!-- OUTPUT PANELS -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-top:1.5rem;">
      <div>
        <div class="pipeline-step">Bus Logging Terminal</div>
        <div id="ec-arb-log" class="terminal-box"></div>
      </div>
      <div>
        <div class="pipeline-step">Arbitration States</div>
        <div class="panel-box" id="ec-arb-summary" style="height:200px; display:flex; flex-direction:column; justify-content:center; gap:0.5rem; box-sizing:border-box;"></div>
      </div>
    </div>
  `;

  // DOM elements
  const aSel = document.getElementById('ec-arb-a');
  const bSel = document.getElementById('ec-arb-b');
  const transmitBtn = document.getElementById('ec-arb-transmit-btn');

  const statusBox = document.getElementById('ec-arb-status');
  const waveformContainer = document.getElementById('ec-arb-waveform-container');
  const logContainer = document.getElementById('ec-arb-log');
  const summaryContainer = document.getElementById('ec-arb-summary');

  let animating = false;
  let animStep = 20;

  aSel.addEventListener('change', () => {
    updateUi();
  });

  bSel.addEventListener('change', () => {
    updateUi();
  });

  transmitBtn.addEventListener('click', async () => {
    if (animating) return;
    animating = true;
    animStep = 0;

    for (let step = 0; step <= 11; step++) {
      animStep = step;
      updateUi();
      await new Promise(resolve => setTimeout(resolve, 150));
    }

    animating = false;
    animStep = 20;
    updateUi();
  });

  updateUi();

  function updateUi() {
    const valA = parseInt(aSel.value);
    const valB = parseInt(bSel.value);

    // Convert to bit arrays
    const bitsA = [];
    const bitsB = [];
    for (let i = 7; i >= 0; i--) {
      bitsA.push((valA >> i) & 1);
      bitsB.push((valB >> i) & 1);
    }

    // Calculate arbitration dropout
    let activeA = true;
    let activeB = true;
    let lostStepA = -1;
    let lostStepB = -1;

    const actualSdaBits = [];
    for (let i = 0; i < 8; i++) {
      const bitA = activeA ? bitsA[i] : 1;
      const bitB = activeB ? bitsB[i] : 1;
      const sharedBit = bitA & bitB;
      actualSdaBits.push(sharedBit);

      if (activeA && bitA === 1 && sharedBit === 0) {
        activeA = false;
        lostStepA = i;
      }
      if (activeB && bitB === 1 && sharedBit === 0) {
        activeB = false;
        lostStepB = i;
      }
    }

    // Update status badge
    if (lostStepA === -1 && lostStepB === -1) {
      statusBox.className = "agreement-item agreement-ok";
      statusBox.innerHTML = "✓ Transactions Identical. No Collision.";
    } else if (lostStepA !== -1) {
      statusBox.className = "agreement-item agreement-warning";
      statusBox.innerHTML = "✓ Master B Victorious. A backed off.";
    } else {
      statusBox.className = "agreement-item agreement-warning";
      statusBox.innerHTML = "✓ Master A Victorious. B backed off.";
    }

    // Render Waveforms SVG
    const svgW = 950;
    const svgH = 240;
    const padLeft = 110;
    const yAHigh = 25, yALow = 40;
    const yBHigh = 70, yBLow = 85;
    const ySharedHigh = 115, ySharedLow = 130;
    const ySclHigh = 160, ySclLow = 175;

    const xEdges = [];
    for (let i = 0; i < 9; i++) {
      xEdges.push(padLeft + 45 + i * 70);
    }

    const svgBlocks = [];

    // Master A SDA
    let pathA = `M 0,${yAHigh} L ${xEdges[0]},${yAHigh}`;
    let actA = true;
    for (let i = 0; i < 8; i++) {
      const startX = xEdges[i];
      const endX = xEdges[i+1];
      const bit = actA ? bitsA[i] : 1;
      const yVal = bit === 1 ? yAHigh : yALow;
      pathA += ` L ${startX},${yVal} L ${endX},${yVal}`;
      if (actA && lostStepA === i) actA = false;
    }
    pathA += ` L ${svgW},${yAHigh}`;
    svgBlocks.push(`<path d="${pathA}" fill="none" stroke="#3B82F6" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${yALow}" fill="#3B82F6" font-family="var(--mono)" font-size="8" text-anchor="end">Master A SDA</text>`);

    // Master B SDA
    let pathB = `M 0,${yBHigh} L ${xEdges[0]},${yBHigh}`;
    let actB = true;
    for (let i = 0; i < 8; i++) {
      const startX = xEdges[i];
      const endX = xEdges[i+1];
      const bit = actB ? bitsB[i] : 1;
      const yVal = bit === 1 ? yBHigh : yBLow;
      pathB += ` L ${startX},${yVal} L ${endX},${yVal}`;
      if (actB && lostStepB === i) actB = false;
    }
    pathB += ` L ${svgW},${yBHigh}`;
    svgBlocks.push(`<path d="${pathB}" fill="none" stroke="#EC4899" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${yBLow}" fill="#EC4899" font-family="var(--mono)" font-size="8" text-anchor="end">Master B SDA</text>`);

    // Shared SDA Line
    let pathShared = `M 0,${ySharedHigh} L ${xEdges[0]},${ySharedHigh}`;
    for (let i = 0; i < 8; i++) {
      const startX = xEdges[i];
      const endX = xEdges[i+1];
      const bit = actualSdaBits[i];
      const yVal = bit === 1 ? ySharedHigh : ySharedLow;
      pathShared += ` L ${startX},${yVal} L ${endX},${yVal}`;
    }
    pathShared += ` L ${svgW},${ySharedHigh}`;
    svgBlocks.push(`<path d="${pathShared}" fill="none" stroke="#10B981" stroke-width="2" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${ySharedLow}" fill="#10B981" font-family="var(--mono)" font-size="8" text-anchor="end">Shared SDA Bus</text>`);

    // Shared SCL Line
    let pathScl = `M 0,${ySclHigh} L ${xEdges[0]},${ySclHigh}`;
    for (let i = 0; i < 8; i++) {
      const startX = xEdges[i];
      const midX = startX + 35;
      const endX = xEdges[i+1];
      pathScl += ` L ${startX},${ySclLow} L ${midX},${ySclLow} L ${midX},${ySclHigh} L ${endX},${ySclHigh}`;
    }
    pathScl += ` L ${svgW},${ySclHigh}`;
    svgBlocks.push(`<path d="${pathScl}" fill="none" stroke="#6366F1" stroke-width="1.5" />`);
    svgBlocks.push(`<text x="${padLeft - 15}" y="${ySclLow}" fill="#6366F1" font-family="var(--mono)" font-size="8" text-anchor="end">SCL (Clock)</text>`);

    // Highlight Dropout Step
    if (lostStepA !== -1) {
      const xDropout = xEdges[lostStepA] + 35; // SCL rising edge/sample point
      svgBlocks.push(`<line x1="${xDropout}" y1="10" x2="${xDropout}" y2="190" stroke="#EF6868" stroke-dasharray="2,2" stroke-width="1" />`);
      svgBlocks.push(`<text x="${xDropout}" y="15" fill="#EF6868" font-family="var(--mono)" font-size="7" font-weight="bold" text-anchor="middle">A BACKED OFF</text>`);
    }
    if (lostStepB !== -1) {
      const xDropout = xEdges[lostStepB] + 35;
      svgBlocks.push(`<line x1="${xDropout}" y1="10" x2="${xDropout}" y2="190" stroke="#EF6868" stroke-dasharray="2,2" stroke-width="1" />`);
      svgBlocks.push(`<text x="${xDropout}" y="15" fill="#EF6868" font-family="var(--mono)" font-size="7" font-weight="bold" text-anchor="middle">B BACKED OFF</text>`);
    }

    // Cursor
    if (animating && animStep <= 9) {
      const cursorX = xEdges[0] + animStep * 70 + 35;
      svgBlocks.push(`<line x1="${cursorX}" y1="10" x2="${cursorX}" y2="190" stroke="#3B82F6" stroke-width="1.5" />`);
    }

    waveformContainer.innerHTML = `<svg viewBox="0 0 ${svgW} ${svgH}" width="100%">${svgBlocks.join('')}</svg>`;

    // Logs
    const logs = ["[0.0ms] Multi-Master Sync: Both Master A and Master B pull SDA LOW simultaneously."];
    logs.push("[0.1ms] Both clock generators sync up on the shared SCL line.");
    
    let curA = true;
    let curB = true;
    for (let i = 0; i < 8; i++) {
      if (animStep >= i + 1) {
        const bitA = curA ? bitsA[i] : 1;
        const bitB = curB ? bitsB[i] : 1;
        const shared = actualSdaBits[i];
        
        logs.push(`[Bit ${7-i}] A drives ${bitA}, B drives ${bitB}. Shared SDA Bus resolves to ${shared}.`);
        
        if (curA && lostStepA === i) {
          logs.push(`[COLLISION] Master A wrote 1 but sensed LOW on SDA. Master A lost arbitration and backed off.`);
          curA = false;
        }
        if (curB && lostStepB === i) {
          logs.push(`[COLLISION] Master B wrote 1 but sensed LOW on SDA. Master B lost arbitration and backed off.`);
          curB = false;
        }
      }
    }
    if (animStep >= 9) {
      logs.push("[SUCCESS] Arbitration phase complete. Single active master owns the bus trace.");
    }
    logContainer.innerHTML = logs.join('<br>');
    logContainer.scrollTop = logContainer.scrollHeight;

    // Summary panel
    const statusA = lostStepA === -1 ? `<span style="color:#10B981;font-weight:bold;">Active / Won</span>` : `<span style="color:#EF6868;">Lost (Backed off at Bit ${7-lostStepA})</span>`;
    const statusB = lostStepB === -1 ? `<span style="color:#10B981;font-weight:bold;">Active / Won</span>` : `<span style="color:#EF6868;">Lost (Backed off at Bit ${7-lostStepB})</span>`;

    summaryContainer.innerHTML = `
      <div style="font-family:var(--mono); font-size:0.75rem; color:var(--muted); text-transform:uppercase;">Master A State:</div>
      <div style="font-family:var(--mono); font-size:0.95rem; color:#FFF; margin-bottom:0.6rem;">${statusA}</div>
      <div style="font-family:var(--mono); font-size:0.75rem; color:var(--muted); text-transform:uppercase;">Master B State:</div>
      <div style="font-family:var(--mono); font-size:0.95rem; color:#FFF;">${statusB}</div>
    `;
  }
}

function renderCanConversationOfDominance() {
  const container = document.getElementById('can-conversation-of-dominance');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Conversation of Dominance</div>
    <div class="edgecase-subheader">Watch Arbitration Happen</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Configure three nodes with 11-bit identifiers (in Hex) and watch them compete for bus access. Dominant bits (0) override recessive bits (1).
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Identifier Configuration</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:1.25rem;">
        <div>
          <div class="panel-title" style="color:#3B82F6; font-size:0.8rem; margin-bottom:0.4rem;">Node 1 (Engine ECU)</div>
          <input type="text" id="ec-can-id1" class="edgecase-select" style="font-family:var(--mono); background:var(--surface2); border:1px solid var(--border); color:#FFF; padding:0.4rem; border-radius:4px; width:100%;" value="0x3F4">
        </div>
        <div>
          <div class="panel-title" style="color:#EC4899; font-size:0.8rem; margin-bottom:0.4rem;">Node 2 (ABS Controller)</div>
          <input type="text" id="ec-can-id2" class="edgecase-select" style="font-family:var(--mono); background:var(--surface2); border:1px solid var(--border); color:#FFF; padding:0.4rem; border-radius:4px; width:100%;" value="0x3A2">
        </div>
        <div>
          <div class="panel-title" style="color:#A855F7; font-size:0.8rem; margin-bottom:0.4rem;">Node 3 (Body Control)</div>
          <input type="text" id="ec-can-id3" class="edgecase-select" style="font-family:var(--mono); background:var(--surface2); border:1px solid var(--border); color:#FFF; padding:0.4rem; border-radius:4px; width:100%;" value="0x5B1">
        </div>
      </div>
    </div>

    <!-- SYSTEM CONTROLS -->
    <div class="pipeline-step">System Controls</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: 3fr 1fr; gap:1rem; align-items:center;">
        <div style="font-size:0.75rem; color:var(--text); font-family:var(--mono);">
          Click to start transmission. The nodes will write their IDs bit-by-bit onto the differential bus.
        </div>
        <button id="ec-can-transmit-btn" class="edgecase-button" style="margin:0; width:100%; height:38px;">TRANSMIT</button>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Physical Waveform Arbitration Trace (Shared Differential Bus)</div>
    <div class="edgecase-visual" id="ec-can-waveform-container" style="background:#0F172A; min-height:280px; position:relative;"></div>

    <!-- OUTPUT PANELS -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-top:1.5rem;">
      <div>
        <div class="pipeline-step">Arbitration Log</div>
        <div id="ec-can-log" class="terminal-box"></div>
      </div>
      <div>
        <div class="pipeline-step">Node Active States</div>
        <div class="panel-box" id="ec-can-summary" style="height:200px; display:flex; flex-direction:column; justify-content:center; gap:0.5rem; box-sizing:border-box;"></div>
      </div>
    </div>
  `;

  const id1Input = document.getElementById('ec-can-id1');
  const id2Input = document.getElementById('ec-can-id2');
  const id3Input = document.getElementById('ec-can-id3');
  const transmitBtn = document.getElementById('ec-can-transmit-btn');
  const waveformContainer = document.getElementById('ec-can-waveform-container');
  const logContainer = document.getElementById('ec-can-log');
  const summaryContainer = document.getElementById('ec-can-summary');

  let animating = false;
  let animStep = 20;

  function parseHex(val, defaultVal) {
    try {
      let clean = val.trim();
      if (!clean.startsWith('0x')) clean = '0x' + clean;
      const parsed = parseInt(clean, 16);
      if (isNaN(parsed) || parsed < 0 || parsed > 0x7FF) return defaultVal;
      return parsed;
    } catch(e) {
      return defaultVal;
    }
  }

  transmitBtn.addEventListener('click', () => {
    if (animating) return;
    animating = true;
    animStep = 0;
    runAnimation();
  });

  function runAnimation() {
    if (!animating) return;

    const id1 = parseHex(id1Input.value, 0x3F4);
    const id2 = parseHex(id2Input.value, 0x3A2);
    const id3 = parseHex(id3Input.value, 0x5B1);

    // Convert to 11 bits
    const bits1 = [];
    const bits2 = [];
    const bits3 = [];
    for (let i = 10; i >= 0; i--) {
      bits1.push((id1 >> i) & 1);
      bits2.push((id2 >> i) & 1);
      bits3.push((id3 >> i) & 1);
    }

    // Step-by-step state calculation
    const states = [];
    let act1 = true, act2 = true, act3 = true;
    let logLines = ["Initializing CAN arbitration sequence...", "Nodes check for bus idle. Bus is free.", "Simultaneously transmitting SOF (Start of Frame: Dominant 0)..."];

    for (let s = 0; s < 11; s++) {
      const bit1 = bits1[s];
      const bit2 = bits2[s];
      const bit3 = bits3[s];

      const out1 = act1 ? bit1 : 1;
      const out2 = act2 ? bit2 : 1;
      const out3 = act3 ? bit3 : 1;

      // Shared bus resolves to dominant (0) if any active node writes 0.
      const busState = out1 & out2 & out3;

      let stepDesc = `Bit ${10-s}: `;
      let dropouts = [];

      if (act1 && bit1 === 1 && busState === 0) {
        act1 = false;
        dropouts.push("Node 1 dropped out (wrote 1, read 0)");
      }
      if (act2 && bit2 === 1 && busState === 0) {
        act2 = false;
        dropouts.push("Node 2 dropped out (wrote 1, read 0)");
      }
      if (act3 && bit3 === 1 && busState === 0) {
        act3 = false;
        dropouts.push("Node 3 dropped out (wrote 1, read 0)");
      }

      stepDesc += `[Node 1: ${act1 ? bit1 : '-'}, Node 2: ${act2 ? bit2 : '-'}, Node 3: ${act3 ? bit3 : '-'}] => Bus: ${busState}`;
      if (dropouts.length > 0) {
        stepDesc += ` | ${dropouts.join(", ")}`;
      }

      logLines.push(stepDesc);

      states.push({
        step: s,
        bits: [bit1, bit2, bit3],
        actives: [act1, act2, act3],
        bus: busState,
        dropouts: dropouts
      });
    }

    let winner = 1;
    if (act2) winner = 2;
    if (act3) winner = 3;
    logLines.push(`Arbitration completed. Node ${winner} wins and gains bus control.`);

    if (animStep <= 11) {
      // Draw SVG waveform
      drawWaveforms(bits1, bits2, bits3, states, animStep);
      
      // Update Log
      logContainer.innerHTML = logLines.slice(0, animStep + 3).map(l => `<div>${escHtml(l)}</div>`).join('');
      logContainer.scrollTop = logContainer.scrollHeight;

      // Update Summary panel
      updateSummary(states, animStep, winner);

      animStep++;
      setTimeout(runAnimation, 1200);
    } else {
      animating = false;
    }
  }

  function drawWaveforms(bits1, bits2, bits3, states, currentStep) {
    const w = waveformContainer.clientWidth || 700;
    const h = 260;
    const pad = 100;
    const stepW = (w - pad - 40) / 11;

    let svg = `<svg width="100%" height="100%" viewBox="0 0 ${w} ${h}" style="font-family:var(--mono);">`;

    // Draw background grid lines for bit boundaries
    for (let i = 0; i <= 11; i++) {
      const x = pad + i * stepW;
      svg += `<line x1="${x}" y1="10" x2="${x}" y2="${h - 20}" stroke="var(--border)" stroke-dasharray="2,2"/>`;
      if (i < 11) {
        svg += `<text x="${x + stepW/2}" y="${h - 5}" fill="var(--muted)" font-size="9" text-anchor="middle">Bit ${10-i}</text>`;
      }
    }

    // Row settings
    const rows = [
      { name: "Node 1 TX", y: 35, color: "#3B82F6", bits: bits1, idx: 0 },
      { name: "Node 2 TX", y: 85, color: "#EC4899", bits: bits2, idx: 1 },
      { name: "Node 3 TX", y: 135, color: "#A855F7", bits: bits3, idx: 2 },
      { name: "Shared Bus", y: 195, color: "#10B981", bits: states.map(s => s.bus), idx: -1 }
    ];

    rows.forEach(r => {
      // Row Label
      svg += `<text x="10" y="${r.y + 5}" fill="${r.color}" font-size="10" font-weight="bold">${r.name}</text>`;

      // Generate signal path
      let path = `M ${pad} ${r.y + (r.bits[0] === 1 ? -12 : 12)}`;

      for (let i = 0; i < 11; i++) {
        const xStart = pad + i * stepW;
        const xEnd = pad + (i + 1) * stepW;
        let val = r.bits[i];

        if (r.idx !== -1) {
          // For node signals, if it dropped out, show it floating HIGH (1)
          if (i > 0 && !states[i-1].actives[r.idx]) {
            val = 1;
          }
        }

        const yVal = r.y + (val === 1 ? -12 : 12);
        
        // Horizontal line
        path += ` L ${xStart} ${yVal} L ${xEnd} ${yVal}`;

        // If node dropped out exactly at this step, draw a mark
        if (r.idx !== -1 && i < currentStep && states[i].dropouts.some(d => d.includes(`Node ${r.idx + 1}`))) {
          svg += `<circle cx="${xStart + stepW/2}" cy="${yVal}" r="5" fill="#EF6868"/>`;
          svg += `<text x="${xStart + stepW/2}" y="${yVal - 8}" fill="#EF6868" font-size="8" text-anchor="middle" font-weight="bold">LOST</text>`;
        }
      }

      svg += `<path d="${path}" fill="none" stroke="${r.color}" stroke-width="2"/>`;
    });

    // Draw active cursor
    if (currentStep < 11) {
      const cursorX = pad + currentStep * stepW;
      svg += `<rect x="${cursorX}" y="10" width="${stepW}" height="${h - 30}" fill="rgba(59, 130, 246, 0.08)" stroke="var(--blue)" stroke-width="1" stroke-dasharray="4,4"/>`;
    }

    svg += `</svg>`;
    waveformContainer.innerHTML = svg;
  }

  function updateSummary(states, currentStep, winner) {
    if (currentStep === 0) {
      summaryContainer.innerHTML = `<div style="font-family:var(--mono); font-size:0.8rem; color:#FFF; text-align:center;">Sequence started...</div>`;
      return;
    }

    const idx = Math.min(currentStep - 1, 10);
    const s = states[idx];

    const s1 = s.actives[0] ? `<span style="color:#10B981;font-weight:bold;">ACTIVE</span>` : `<span style="color:#EF6868;">DROPPED OUT</span>`;
    const s2 = s.actives[1] ? `<span style="color:#10B981;font-weight:bold;">ACTIVE</span>` : `<span style="color:#EF6868;">DROPPED OUT</span>`;
    const s3 = s.actives[2] ? `<span style="color:#10B981;font-weight:bold;">ACTIVE</span>` : `<span style="color:#EF6868;">DROPPED OUT</span>`;

    summaryContainer.innerHTML = `
      <div style="font-family:var(--mono); font-size:0.75rem; color:var(--muted); text-transform:uppercase;">Node 1 (Engine ECU):</div>
      <div style="font-family:var(--mono); font-size:0.85rem; color:#FFF; margin-bottom:0.5rem;">${s1} (ID bits: ${bitsHtml(states, 0, currentStep)})</div>
      <div style="font-family:var(--mono); font-size:0.75rem; color:var(--muted); text-transform:uppercase;">Node 2 (ABS Controller):</div>
      <div style="font-family:var(--mono); font-size:0.85rem; color:#FFF; margin-bottom:0.5rem;">${s2} (ID bits: ${bitsHtml(states, 1, currentStep)})</div>
      <div style="font-family:var(--mono); font-size:0.75rem; color:var(--muted); text-transform:uppercase;">Node 3 (Body Control):</div>
      <div style="font-family:var(--mono); font-size:0.85rem; color:#FFF; margin-bottom:0.5rem;">${s3} (ID bits: ${bitsHtml(states, 2, currentStep)})</div>
      ${currentStep >= 11 ? `<div style="margin-top:0.4rem; font-family:var(--mono); font-weight:bold; font-size:0.8rem; color:#10B981; text-align:center;">Winner: Node ${winner} (Lowest ID wins!)</div>` : ''}
    `;
  }

  function bitsHtml(states, nodeIdx, currentStep) {
    let out = '';
    for (let i = 0; i < 11; i++) {
      let char = states[i].bits[nodeIdx];
      let color = 'var(--muted)';
      if (i < currentStep) {
        color = states[i].actives[nodeIdx] ? '#FFF' : '#EF6868';
      }
      out += `<span style="color:${color}; margin-right:2px;">${char}</span>`;
    }
    return out;
  }

  // Draw initial waveforms on load
  drawWaveforms([0,1,1,1,1,1,1,0,1,0,0], [0,1,1,1,0,1,0,0,0,1,0], [1,0,1,1,0,1,1,0,0,0,1], Array(11).fill({ bus: 1,actives:[true,true,true], dropouts:[] }), 11);
  summaryContainer.innerHTML = `<div style="font-family:var(--mono); font-size:0.8rem; color:var(--muted); text-align:center;">Configure identifiers and click TRANSMIT to watch arbitration live.</div>`;
}

function renderCanJourneyOfAFrame() {
  const container = document.getElementById('can-journey-of-a-frame');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Journey of a CAN Frame</div>
    <div class="edgecase-subheader">Watch a Message Travel through the CAN Controller</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Follow a CAN frame step-by-step from the application layer, through registers, Message RAM, bit-stuffing, the differential bus, and final arrival.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Frame Settings</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1.25rem;">
        <div>
          <div class="panel-title" style="color:var(--blue); font-size:0.8rem; margin-bottom:0.4rem;">Message Identifier</div>
          <input type="text" id="ec-jf-id" class="edgecase-select" style="font-family:var(--mono); background:var(--surface2); border:1px solid var(--border); color:#FFF; padding:0.4rem; border-radius:4px; width:100%;" value="0x1F4">
        </div>
        <div>
          <div class="panel-title" style="color:#10B981; font-size:0.8rem; margin-bottom:0.4rem;">Data Payload (Hex bytes)</div>
          <input type="text" id="ec-jf-data" class="edgecase-select" style="font-family:var(--mono); background:var(--surface2); border:1px solid var(--border); color:#FFF; padding:0.4rem; border-radius:4px; width:100%;" value="0xDE 0xAD 0xBE 0xEF">
        </div>
      </div>
    </div>

    <!-- PIPELINE STEPPER -->
    <div class="pipeline-step">Pipeline Progress</div>
    <div class="panel-box" style="padding:1rem; overflow-x:auto;">
      <div id="ec-jf-stepper" style="display:flex; justify-content:space-between; align-items:center; min-width:650px;"></div>
    </div>

    <!-- STAGE DETAIL PANEL -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem;">
      <div>
        <div class="pipeline-step">Current Stage Mechanics</div>
        <div class="panel-box" id="ec-jf-details" style="min-height:220px; display:flex; flex-direction:column; justify-content:flex-start; gap:0.6rem; box-sizing:border-box;"></div>
      </div>
      <div>
        <div class="pipeline-step">Controller Signal Log</div>
        <div id="ec-jf-log" class="terminal-box" style="height:220px;"></div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div style="margin-top:1rem; display:flex; justify-content:flex-end;">
      <button id="ec-jf-transmit-btn" class="edgecase-button" style="margin:0; width:150px; height:38px;">TRANSMIT</button>
    </div>
  `;

  const idInput = document.getElementById('ec-jf-id');
  const dataInput = document.getElementById('ec-jf-data');
  const stepperContainer = document.getElementById('ec-jf-stepper');
  const detailsContainer = document.getElementById('ec-jf-details');
  const logContainer = document.getElementById('ec-jf-log');
  const transmitBtn = document.getElementById('ec-jf-transmit-btn');

  const stages = [
    { title: "Application", desc: "The software application calls the driver function: <code>can_transmit(0x1F4, [0xDE, 0xAD, 0xBE, 0xEF])</code>. The core processor prepares to hand over control." },
    { title: "CAN Controller", desc: "The driver writes the transmit request command to the CAN Controller peripheral register (TXBAR - Transmit Buffer Add Request register), setting up transmission flags." },
    { title: "Message RAM", desc: "The peripheral writes the frame description into a dedicated <strong>Message RAM</strong> partition. <i>Connection to <a onclick=\"openItem('the-hidden-geography-of-firmware', 'blogs')\" style=\"color:var(--blue); cursor:pointer; text-decoration:underline;\">The Hidden Geography of Firmware</a></i>: On microcontrollers like STM32H7, Message RAM sits in a specific SRAM block. A misalignment in the register base offset triggers a hardware bus fault or silent frame drops." },
    { title: "Frame Builder", desc: "The CAN controller IP packages the identifier, DLC (Data Length Code = 4), and the hex payload into a structured serial frame, ready for physical bitwise streaming." },
    { title: "Arbitration", desc: "The transceiver checks if the bus is idle, then asserts SOF and transmits the 11 ID bits (00111110100) onto the bus, listening to ensure no higher-priority message collides." },
    { title: "Bit Stuffing", desc: "As bits flow, the hardware controller monitors the stream. If it detects five consecutive 1s or 0s, it automatically inserts an opposite bit (stuff bit) to keep the receiver clocks synchronized." },
    { title: "CRC Generator", desc: "The hardware calculates a 15-bit Cyclic Redundancy Check (CRC) over the address and payload, appending the checksum to the frame for error validation." },
    { title: "Differential Bus", desc: "The CAN transceiver drives the physical twisted-pair wire. Logic 0 pushes CANH to 3.5V and CANL to 1.5V (Dominant). Logic 1 leaves both lines floating at 2.5V (Recessive)." },
    { title: "Receiving Node", desc: "The receiving transceiver senses the differential voltage. Validating the CRC, it overrides the ACK slot with a dominant 0 to acknowledge correct delivery." },
    { title: "App Delivery", desc: "The receiving CAN controller copies the received payload from its FIFO Message RAM buffer to CPU registers, triggering an RX interrupt so the destination application can process the data." }
  ];

  let currentStageIdx = 0;
  let animating = false;

  function renderStepper() {
    stepperContainer.innerHTML = stages.map((s, idx) => {
      let color = "var(--muted)";
      if (idx === currentStageIdx) color = "var(--blue)";
      else if (idx < currentStageIdx) color = "#10B981";

      const bullet = idx < currentStageIdx ? "✓" : idx + 1;
      const lineHtml = idx < stages.length - 1 ? `<div style="flex-grow:1; height:2px; background:${idx < currentStageIdx ? '#10B981' : 'var(--border)'}; margin:0 6px;"></div>` : '';

      return `
        <div style="display:flex; align-items:center; flex-grow:${idx < stages.length - 1 ? 1 : 0}">
          <div style="width:24px; height:24px; border-radius:50%; border:2px solid ${color}; display:flex; align-items:center; justify-content:center; font-family:var(--mono); font-size:0.7rem; font-weight:bold; color:${color}; background:#0F172A;" title="${s.title}">
            ${bullet}
          </div>
          ${lineHtml}
        </div>
      `;
    }).join('');
  }

  function updateStage() {
    renderStepper();
    const stage = stages[currentStageIdx];
    const logTimestamp = new Date().toISOString().slice(11, 19);

    // Show details
    detailsContainer.innerHTML = `
      <div style="font-family:'Syne',sans-serif; font-size:1rem; font-weight:bold; color:#FFF;">${currentStageIdx + 1}. ${stage.title}</div>
      <p style="font-size:0.85rem; color:#CBD5E1; line-height:1.6; margin-top:0.4rem;">${stage.desc}</p>
    `;

    // Append to log
    const valId = idInput.value.trim();
    const valData = dataInput.value.trim();
    let logLine = `[${logTimestamp}] Stage ${currentStageIdx + 1}: ${stage.title} - `;
    if (currentStageIdx === 0) logLine += `Preparing packet ID ${valId}, payload [${valData}]`;
    else if (currentStageIdx === 2) logLine += `Wrote descriptor boundaries to CAN Message RAM`;
    else if (currentStageIdx === 4) logLine += `Starting bit-arbitration with ID bits`;
    else if (currentStageIdx === 7) logLine += `Driving physical lines CANH/CANL`;
    else if (currentStageIdx === 8) logLine += `ACK assertion detected (Dominant 0 in slot)`;
    else logLine += `OK`;

    logContainer.innerHTML += `<div>${escHtml(logLine)}</div>`;
    logContainer.scrollTop = logContainer.scrollHeight;
  }

  transmitBtn.addEventListener('click', () => {
    if (animating) return;
    animating = true;
    currentStageIdx = 0;
    logContainer.innerHTML = `<div>[${new Date().toISOString().slice(11, 19)}] Transmit sequence started.</div>`;
    animatePipeline();
  });

  function animatePipeline() {
    if (currentStageIdx < stages.length) {
      updateStage();
      currentStageIdx++;
      setTimeout(animatePipeline, 2000);
    } else {
      animating = false;
      logContainer.innerHTML += `<div style="color:#10B981;font-weight:bold;">[SYSTEM] Frame transaction completed successfully.</div>`;
    }
  }

  // Draw initial
  currentStageIdx = 0;
  renderStepper();
  detailsContainer.innerHTML = `<div style="font-family:var(--mono); font-size:0.85rem; color:var(--muted); text-align:center;">Configure message and press TRANSMIT to watch the frame pipeline.</div>`;
  logContainer.innerHTML = `<div style="font-family:var(--mono); font-size:0.75rem; color:var(--muted);">Terminal idle.</div>`;
}

function renderTimerBuilder() {
  const container = document.getElementById('timer-builder');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Race Against Time</div>
    <div class="edgecase-subheader">Configure Hardware Timer Registers & Waveform Generation</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Interact with clock prescalers, auto-reload value (ARR), and compare match threshold (CCR) to see how digital signals are structured in hardware.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Register Configurations</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1.25rem;">
        <div class="edgecase-control-group">
          <label for="ec-tb-clk">Clock Source Frequency</label>
          <select id="ec-tb-clk" class="edgecase-select">
            <option value="1000000" selected>1 MHz (Internal Oscillator)</option>
            <option value="8000000">8 MHz (HSE Crystal)</option>
            <option value="16000000">16 MHz (PLL Speed)</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-tb-psc">Prescaler (PSC Register value)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-tb-psc" class="edgecase-slider" min="0" max="1000" value="9">
            <span id="ec-tb-psc-val" class="edgecase-slider-val">9</span>
          </div>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-tb-bits">Counter Register Size</label>
          <select id="ec-tb-bits" class="edgecase-select">
            <option value="8" selected>8-bit (Max count: 255)</option>
            <option value="16">16-bit (Max count: 65535)</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-tb-arr">Auto-Reload (ARR Register)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-tb-arr" class="edgecase-slider" min="1" max="255" value="99">
            <span id="ec-tb-arr-val" class="edgecase-slider-val">99</span>
          </div>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-tb-ccr">Compare Value (CCR Register)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-tb-ccr" class="edgecase-slider" min="0" max="99" value="49">
            <span id="ec-tb-ccr-val" class="edgecase-slider-val">49</span>
          </div>
        </div>
      </div>
    </div>

    <!-- VISUAL COMPARATOR & COUNTER PLOT -->
    <div class="pipeline-step">Hardware Counting & Signal Generation Waveform</div>
    <div class="edgecase-visual" style="background:#0F172A; padding:1.25rem;">
      <svg id="ec-tb-svg" viewBox="0 0 800 240" style="width:100%; height:auto; overflow:visible;">
        <!-- Waveform drawings will go here -->
      </svg>
    </div>

    <!-- CALCULATIONS PANEL -->
    <div class="pipeline-step">Calculated Technical Metrics</div>
    <div class="edgecase-output-panel">
      <div class="edgecase-output-grid">
        <div class="edgecase-output-box">
          <div class="edgecase-output-label">Divider Ratio (PSC + 1)</div>
          <div class="edgecase-output-val" id="ec-tb-calc-div">10</div>
        </div>
        <div class="edgecase-output-box">
          <div class="edgecase-output-label">Counter Frequency (f_CNT)</div>
          <div class="edgecase-output-val" id="ec-tb-calc-fcnt">100.00 kHz</div>
        </div>
        <div class="edgecase-output-box">
          <div class="edgecase-output-label">Overflow Frequency (Interrupt)</div>
          <div class="edgecase-output-val" id="ec-tb-calc-farr">1.00 kHz (1.00 ms period)</div>
        </div>
        <div class="edgecase-output-box">
          <div class="edgecase-output-label">Compare Match Event Duty Cycle</div>
          <div class="edgecase-output-val" id="ec-tb-calc-duty">50.0%</div>
        </div>
      </div>
    </div>
  `;

  // Grab element references
  const clkSelect = document.getElementById('ec-tb-clk');
  const pscSlider = document.getElementById('ec-tb-psc');
  const pscValText = document.getElementById('ec-tb-psc-val');
  const bitsSelect = document.getElementById('ec-tb-bits');
  const arrSlider = document.getElementById('ec-tb-arr');
  const arrValText = document.getElementById('ec-tb-arr-val');
  const ccrSlider = document.getElementById('ec-tb-ccr');
  const ccrValText = document.getElementById('ec-tb-ccr-val');
  const svg = document.getElementById('ec-tb-svg');

  // Calc texts
  const calcDiv = document.getElementById('ec-tb-calc-div');
  const calcFcnt = document.getElementById('ec-tb-calc-fcnt');
  const calcFarr = document.getElementById('ec-tb-calc-farr');
  const calcDuty = document.getElementById('ec-tb-calc-duty');

  // Handle register bits changing slider limits
  bitsSelect.addEventListener('change', () => {
    const bits = parseInt(bitsSelect.value);
    const maxVal = bits === 8 ? 255 : 2000;
    arrSlider.max = maxVal;
    if (parseInt(arrSlider.value) > maxVal) {
      arrSlider.value = maxVal;
      arrValText.textContent = maxVal;
    }
    updateLimitsAndCalculations();
  });

  // Event listeners for real-time slider updates
  pscSlider.addEventListener('input', () => {
    pscValText.textContent = pscSlider.value;
    updateLimitsAndCalculations();
  });

  arrSlider.addEventListener('input', () => {
    arrValText.textContent = arrSlider.value;
    ccrSlider.max = arrSlider.value;
    if (parseInt(ccrSlider.value) > parseInt(arrSlider.value)) {
      ccrSlider.value = arrSlider.value;
      ccrValText.textContent = arrSlider.value;
    }
    updateLimitsAndCalculations();
  });

  ccrSlider.addEventListener('input', () => {
    ccrValText.textContent = ccrSlider.value;
    updateLimitsAndCalculations();
  });

  clkSelect.addEventListener('change', updateLimitsAndCalculations);

  let tOffset = 0;

  function updateLimitsAndCalculations() {
    const fOsc = parseFloat(clkSelect.value);
    const pscVal = parseInt(pscSlider.value);
    const arrVal = parseInt(arrSlider.value);
    const ccrVal = parseInt(ccrSlider.value);

    // Div ratio
    const divRatio = pscVal + 1;
    calcDiv.textContent = `${divRatio} (divided by PSC+1)`;

    // Counter frequency
    const fCnt = fOsc / divRatio;
    if (fCnt >= 1000000) {
      calcFcnt.textContent = `${(fCnt / 1000000).toFixed(2)} MHz`;
    } else {
      calcFcnt.textContent = `${(fCnt / 1000).toFixed(2)} kHz`;
    }

    // Overflow freq
    const fArr = fCnt / (arrVal + 1);
    const periodMs = (1000 / fArr);
    if (fArr >= 1000) {
      calcFarr.textContent = `${(fArr / 1000).toFixed(2)} kHz (period: ${periodMs.toFixed(3)} ms)`;
    } else {
      calcFarr.textContent = `${fArr.toFixed(2)} Hz (period: ${periodMs.toFixed(2)} ms)`;
    }

    // Compare duty cycle
    const dutyPercent = ((ccrVal / arrVal) * 100).toFixed(1);
    calcDuty.textContent = `${dutyPercent}% (CCR / ARR)`;
  }

  function drawTimerWaveforms() {
    // Check if element is still in DOM (prevents background loop running on page change)
    if (!document.getElementById('timer-builder')) return;

    const arrVal = parseInt(arrSlider.value);
    const ccrVal = parseInt(ccrSlider.value);

    const width = 800;
    const height = 240;
    const padding = 40;

    tOffset += 0.8; // animation velocity

    let svgContent = `
      <!-- Background grid -->
      <defs>
        <pattern id="tb-grid" width="20" height="20" patternUnits="userSpaceOnUse">
          <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(148,163,184,0.03)" stroke-width="1"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#tb-grid)" rx="6" />
    `;

    // Coordinates mapping
    const chartYTop = 30;
    const chartYBottom = 120;
    const chartHeight = chartYBottom - chartYTop;

    // Draw ARR threshold line
    svgContent += `
      <line x1="${padding}" y1="${chartYTop}" x2="${width - padding}" y2="${chartYTop}" stroke="rgba(239, 68, 68, 0.4)" stroke-dasharray="3,3" stroke-width="1.5" />
      <text x="${width - padding + 5}" y="${chartYTop + 4}" fill="rgba(239, 68, 68, 0.8)" font-family="var(--mono)" font-size="0.65rem">ARR (${arrVal})</text>
    `;

    // Draw CCR threshold line
    const ccrY = chartYBottom - (ccrVal / arrVal) * chartHeight;
    svgContent += `
      <line x1="${padding}" y1="${ccrY}" x2="${width - padding}" y2="${ccrY}" stroke="rgba(59, 130, 246, 0.6)" stroke-dasharray="4,2" stroke-width="1.5" />
      <text x="${width - padding + 5}" y="${ccrY + 4}" fill="rgba(59, 130, 246, 0.9)" font-family="var(--mono)" font-size="0.65rem">CCR (${ccrVal})</text>
    `;

    // Draw baseline
    svgContent += `
      <line x1="${padding}" y1="${chartYBottom}" x2="${width - padding}" y2="${chartYBottom}" stroke="var(--border)" stroke-width="1" />
      <text x="${padding - 30}" y="${chartYBottom + 4}" fill="var(--muted)" font-family="var(--mono)" font-size="0.65rem">0</text>
    `;

    const periodWidth = 200;
    let matchPulses = [];
    let overflowPulses = [];

    // Draw counter trace (sawtooth)
    let pathD = "";
    const startX = padding;
    const endX = width - padding;

    for (let x = startX; x <= endX; x++) {
      const cycleX = (x + tOffset) % periodWidth;
      const progress = cycleX / periodWidth;
      const cntValVal = progress * arrVal;
      const y = chartYBottom - progress * chartHeight;

      if (x === startX) {
        pathD += `M ${x} ${y}`;
      } else {
        const prevCycleX = (x - 1 + tOffset) % periodWidth;
        if (cycleX < prevCycleX) {
          pathD += ` L ${x} ${chartYBottom} M ${x} ${chartYBottom - chartHeight}`;
          overflowPulses.push(x);
        } else {
          pathD += ` L ${x} ${y}`;
        }
      }

      const prevProgress = ((x - 1 + tOffset) % periodWidth) / periodWidth;
      const prevCntVal = prevProgress * arrVal;
      if (prevCntVal <= ccrVal && cntValVal > ccrVal) {
        matchPulses.push(x);
      }
    }

    svgContent += `<path d="${pathD}" fill="none" stroke="#E2E8F0" stroke-width="2" />`;

    // Draw PWM Output wave
    const outYTop = 150;
    const outYBottom = 190;

    let pwmPathD = "";
    for (let x = startX; x <= endX; x++) {
      const cycleX = (x + tOffset) % periodWidth;
      const progress = cycleX / periodWidth;
      const cntValVal = progress * arrVal;
      const isHigh = cntValVal < ccrVal;
      const y = isHigh ? outYTop : outYBottom;

      if (x === startX) {
        pwmPathD += `M ${x} ${y}`;
      } else {
        const prevCycleX = (x - 1 + tOffset) % periodWidth;
        const prevProgress = prevCycleX / periodWidth;
        const prevCnt = prevProgress * arrVal;
        const prevHigh = prevCnt < ccrVal;
        if (isHigh !== prevHigh) {
          pwmPathD += ` L ${x} ${prevHigh ? outYBottom : outYTop} L ${x} ${y}`;
        } else {
          pwmPathD += ` L ${x} ${y}`;
        }
      }
    }

    svgContent += `
      <line x1="${padding}" y1="${outYBottom}" x2="${width - padding}" y2="${outYBottom}" stroke="var(--border)" stroke-width="1" />
      <text x="${padding - 30}" y="${outYBottom - 10}" fill="#10B981" font-family="var(--mono)" font-size="0.65rem">PWM</text>
      <text x="${padding - 30}" y="${outYTop + 10}" fill="#10B981" font-family="var(--mono)" font-size="0.65rem">OUT</text>
      <path d="${pwmPathD}" fill="none" stroke="#10B981" stroke-width="2" />
    `;

    matchPulses.forEach(x => {
      svgContent += `
        <line x1="${x}" y1="${chartYTop}" x2="${x}" y2="${chartYBottom}" stroke="rgba(59, 130, 246, 0.2)" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="${x}" cy="${chartYBottom - (ccrVal / arrVal) * chartHeight}" r="4" fill="var(--blue)" />
        <path d="M ${x - 5} 140 L ${x} 133 L ${x + 5} 140 Z" fill="var(--blue)" />
      `;
    });

    overflowPulses.forEach(x => {
      svgContent += `
        <line x1="${x}" y1="${chartYTop}" x2="${x}" y2="${chartYBottom}" stroke="rgba(239, 68, 68, 0.2)" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="${x}" cy="${chartYBottom}" r="4" fill="#EF6868" />
        <text x="${x - 18}" y="${chartYTop - 8}" fill="#EF6868" font-family="var(--mono)" font-size="0.6rem">OVERFLOW</text>
      `;
    });

    svg.innerHTML = svgContent;

    container.animationId = requestAnimationFrame(drawTimerWaveforms);
  }

  // Cancel previous animations if any
  if (container.animationId) {
    cancelAnimationFrame(container.animationId);
  }

  updateLimitsAndCalculations();
  drawTimerWaveforms();
}

function renderPwmPainter() {
  const container = document.getElementById('pwm-painter');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: Painting with Time</div>
    <div class="edgecase-subheader">Pulse Width Modulation (PWM) and Average Power Integration</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Adjust the frequency and duty cycle to inspect how digital pulses simulate analog voltages, driving physical loads like LEDs and DC motors.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">PWM Waveform Configuration</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:1.5rem;">
        <div class="edgecase-control-group">
          <label for="ec-pwm-freq">PWM Frequency</label>
          <select id="ec-pwm-freq" class="edgecase-select">
            <option value="50">50 Hz (Servo Motor / Low speed)</option>
            <option value="500">500 Hz (Standard Arduino PWM)</option>
            <option value="2000" selected>2.0 kHz (Audible motor drive)</option>
            <option value="10000">10.0 kHz (Ultrasonic range / LED dimming)</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-pwm-duty">Duty Cycle (0% to 100%)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-pwm-duty" class="edgecase-slider" min="0" max="100" value="50">
            <span id="ec-pwm-duty-val" class="edgecase-slider-val">50%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- LOADS DISPLAY (SIDE-BY-SIDE LED & MOTOR) -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-bottom:1.5rem;">
      <div>
        <div class="pipeline-step">Output Load 1: Dimmable LED</div>
        <div class="panel-box" style="height:150px; display:flex; flex-direction:column; justify-content:center; align-items:center; background:#0F172A;">
          <svg width="60" height="80" viewBox="0 0 60 80" style="overflow:visible;">
            <!-- LED Bulb Body -->
            <path d="M 15 45 L 15 35 C 15 20 45 20 45 35 L 45 45 Z" fill="#1E293B" stroke="var(--border)" stroke-width="2" />
            <!-- LED Glow Layer -->
            <path id="ec-led-glow" d="M 15 45 L 15 35 C 15 20 45 20 45 35 L 45 45 Z" fill="#10B981" opacity="0.5" style="filter: drop-shadow(0px 0px 12px #10B981);" />
            <!-- LED Metal Base and Leads -->
            <rect x="20" y="45" width="20" height="6" fill="#64748B" rx="1" />
            <line x1="25" y1="51" x2="25" y2="75" stroke="#94A3B8" stroke-width="2" />
            <line x1="35" y1="51" x2="35" y2="75" stroke="#94A3B8" stroke-width="2" />
          </svg>
          <div style="font-family:var(--mono); font-size:0.75rem; color:var(--text); margin-top:0.75rem;" id="ec-led-status">LED Brightness: 50%</div>
        </div>
      </div>
      <div>
        <div class="pipeline-step">Output Load 2: DC Fan Motor</div>
        <div class="panel-box" style="height:150px; display:flex; flex-direction:column; justify-content:center; align-items:center; background:#0F172A;">
          <svg width="90" height="90" viewBox="0 0 100 100" style="overflow:visible;">
            <!-- Outer casing -->
            <circle cx="50" cy="50" r="45" fill="none" stroke="var(--border)" stroke-width="2" />
            <!-- Motor Hub -->
            <circle cx="50" cy="50" r="10" fill="#334155" />
            <!-- Fan blades group -->
            <g id="ec-fan-blades" transform="rotate(0, 50, 50)">
              <!-- Blade 1 -->
              <path d="M 50 40 C 40 30 40 10 50 10 C 60 10 60 30 50 40 Z" fill="#E2E8F0" />
              <!-- Blade 2 -->
              <path d="M 60 50 C 70 40 90 40 90 50 C 90 60 70 60 60 50 Z" fill="#E2E8F0" />
              <!-- Blade 3 -->
              <path d="M 50 60 C 60 70 60 90 50 90 C 40 90 40 70 50 60 Z" fill="#E2E8F0" />
              <!-- Blade 4 -->
              <path d="M 40 50 C 30 60 10 60 10 50 C 10 40 30 40 40 50 Z" fill="#E2E8F0" />
            </g>
          </svg>
          <div style="font-family:var(--mono); font-size:0.75rem; color:var(--text); margin-top:0.75rem;" id="ec-fan-status">Fan RPM: ~1500 RPM</div>
        </div>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Inspected Pulse Waveform (Time domain)</div>
    <div class="edgecase-visual" style="background:#0F172A; padding:1.25rem;">
      <svg id="ec-pwm-svg" viewBox="0 0 800 140" style="width:100%; height:auto; overflow:visible;">
        <!-- PWM trace -->
      </svg>
    </div>

    <!-- STATS PANEL -->
    <div class="pipeline-step">Timing & Signal Metrics</div>
    <div class="edgecase-output-panel">
      <div class="edgecase-output-grid">
        <div class="edgecase-output-box">
          <div class="edgecase-output-label">Signal Period (T)</div>
          <div class="edgecase-output-val" id="ec-pwm-calc-period">0.50 ms (500 µs)</div>
        </div>
        <div class="edgecase-output-box">
          <div class="edgecase-output-label">On-Time / Pulse Width (T_on)</div>
          <div class="edgecase-output-val" id="ec-pwm-calc-ton">0.25 ms (250 µs)</div>
        </div>
        <div class="edgecase-output-box">
          <div class="edgecase-output-label">Off-Time (T_off)</div>
          <div class="edgecase-output-val" id="ec-pwm-calc-toff">0.25 ms (250 µs)</div>
        </div>
        <div class="edgecase-output-box">
          <div class="edgecase-output-label">Equivalent DC Voltage</div>
          <div class="edgecase-output-val" id="ec-pwm-calc-vavg">1.65 V (at 3.3V Logic)</div>
        </div>
      </div>
    </div>
  `;

  const freqSelect = document.getElementById('ec-pwm-freq');
  const dutySlider = document.getElementById('ec-pwm-duty');
  const dutyValText = document.getElementById('ec-pwm-duty-val');

  const ledGlow = document.getElementById('ec-led-glow');
  const ledStatus = document.getElementById('ec-led-status');
  const fanBlades = document.getElementById('ec-fan-blades');
  const fanStatus = document.getElementById('ec-fan-status');

  const pwmSvg = document.getElementById('ec-pwm-svg');

  const calcPeriod = document.getElementById('ec-pwm-calc-period');
  const calcTon = document.getElementById('ec-pwm-calc-ton');
  const calcToff = document.getElementById('ec-pwm-calc-toff');
  const calcVavg = document.getElementById('ec-pwm-calc-vavg');

  let fanAngle = 0;

  dutySlider.addEventListener('input', () => {
    dutyValText.textContent = `${dutySlider.value}%`;
    updatePWMCalculations();
  });

  freqSelect.addEventListener('change', updatePWMCalculations);

  function updatePWMCalculations() {
    const freq = parseFloat(freqSelect.value);
    const duty = parseFloat(dutySlider.value);

    // Period
    const periodSeconds = 1 / freq;
    const periodMs = periodSeconds * 1000;
    const periodUs = periodSeconds * 1000000;
    calcPeriod.textContent = `${periodMs.toFixed(2)} ms (${Math.round(periodUs)} µs)`;

    // Ton
    const tonMs = periodMs * (duty / 100);
    const tonUs = periodUs * (duty / 100);
    calcTon.textContent = `${tonMs.toFixed(2)} ms (${Math.round(tonUs)} µs)`;

    // Toff
    const toffMs = periodMs * ((100 - duty) / 100);
    const toffUs = periodUs * ((100 - duty) / 100);
    calcToff.textContent = `${toffMs.toFixed(2)} ms (${Math.round(toffUs)} µs)`;

    // Equivalent Voltage
    const vAvg = 3.3 * (duty / 100);
    calcVavg.textContent = `${vAvg.toFixed(2)} V (3.3V reference)`;

    // Update LED glow
    ledGlow.setAttribute('opacity', duty / 100);
    ledStatus.textContent = `LED Brightness: ${duty}%`;

    // Update Fan RPM label
    const maxRpm = 3000;
    const currentRpm = Math.round(maxRpm * (duty / 100));
    fanStatus.textContent = `Fan RPM: ~${currentRpm} RPM`;
  }

  function drawPwmWaveform() {
    if (!document.getElementById('pwm-painter')) return;

    const duty = parseFloat(dutySlider.value);
    const width = 800;
    const height = 140;
    const padding = 40;

    let svgContent = `
      <rect width="100%" height="100%" fill="none" rx="6" />
      <line x1="${padding}" y1="${height - 20}" x2="${width - padding}" y2="${height - 20}" stroke="var(--border)" stroke-width="1" />
      <line x1="${padding}" y1="20" x2="${width - padding}" y2="20" stroke="var(--border)" stroke-dasharray="3,3" stroke-width="1" />
      <text x="${padding - 30}" y="24" fill="var(--muted)" font-family="var(--mono)" font-size="0.65rem">3.3V</text>
      <text x="${padding - 30}" y="${height - 16}" fill="var(--muted)" font-family="var(--mono)" font-size="0.65rem">0V</text>
    `;

    const cycleWidth = 175;
    let pathD = "";
    const startX = padding;
    const endX = width - padding;

    const highY = 20;
    const lowY = height - 20;

    for (let x = startX; x <= endX; x++) {
      const cycleX = (x - padding) % cycleWidth;
      const progress = cycleX / cycleWidth;
      const isHigh = progress < (duty / 100);
      const y = isHigh ? highY : lowY;

      if (x === startX) {
        pathD += `M ${x} ${y}`;
      } else {
        const prevCycleX = (x - 1 - padding) % cycleWidth;
        const prevProgress = prevCycleX / cycleWidth;
        const prevHigh = prevProgress < (duty / 100);

        if (isHigh !== prevHigh) {
          pathD += ` L ${x} ${prevHigh ? lowY : highY} L ${x} ${y}`;
        } else {
          pathD += ` L ${x} ${y}`;
        }
      }
    }

    svgContent += `<path d="${pathD}" fill="none" stroke="#10B981" stroke-width="2.5" />`;

    pwmSvg.innerHTML = svgContent;

    const speed = (duty / 100) * 15;
    fanAngle = (fanAngle + speed) % 360;
    fanBlades.setAttribute('transform', `rotate(${fanAngle}, 50, 50)`);

    container.animationId = requestAnimationFrame(drawPwmWaveform);
  }

  if (container.animationId) {
    cancelAnimationFrame(container.animationId);
  }

  updatePWMCalculations();
  drawPwmWaveform();
}

function renderCapturingReality() {
  const container = document.getElementById('capturing-reality');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: Capturing Reality</div>
    <div class="edgecase-subheader">Watch Analog Signals Become Digital Numbers</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Adjust signal frequency, amplitude, ADC resolution, and sampling rate to see how reality is sliced in time and quantized in levels.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Signal & Converter Configuration</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:1.25rem;">
        <div class="edgecase-control-group">
          <label for="ec-cr-type">Signal Type</label>
          <select id="ec-cr-type" class="edgecase-select">
            <option value="sine" selected>Sine Wave (Smooth vibration)</option>
            <option value="triangle">Triangle Wave (Linear ramp)</option>
            <option value="sawtooth">Sawtooth Wave (Asymmetric rise)</option>
            <option value="noisy">Noisy Signal (Complex sum + noise)</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-cr-freq">Signal Frequency (Hz)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-cr-freq" class="edgecase-slider" min="1" max="10" value="3">
            <span id="ec-cr-freq-val" class="edgecase-slider-val">3 Hz</span>
          </div>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-cr-amp">Signal Amplitude (V)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-cr-amp" class="edgecase-slider" min="5" max="33" value="25">
            <span id="ec-cr-amp-val" class="edgecase-slider-val">2.5V</span>
          </div>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-cr-res">ADC Resolution</label>
          <select id="ec-cr-res" class="edgecase-select">
            <option value="3" selected>3-bit (8 Levels)</option>
            <option value="4">4-bit (16 Levels)</option>
            <option value="8">8-bit (256 Levels)</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-cr-rate">Sampling Rate (Hz)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-cr-rate" class="edgecase-slider" min="5" max="80" value="20">
            <span id="ec-cr-rate-val" class="edgecase-slider-val">20 Hz</span>
          </div>
        </div>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Reconstructed Waveform (Green) vs. Original Analog (Gray)</div>
    <div class="edgecase-visual" style="background:#0F172A; padding:1.25rem;">
      <svg id="ec-cr-svg" viewBox="0 0 800 240" style="width:100%; height:auto; overflow:visible;">
        <!-- Waveforms will be drawn dynamically -->
      </svg>
    </div>

    <!-- METRICS & DECODED TABLE -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem;">
      <div>
        <div class="pipeline-step">Sensing Metrics</div>
        <div class="edgecase-output-panel" style="min-height:180px;">
          <div class="edgecase-output-grid" style="grid-template-columns: 1fr 1fr; gap:0.75rem;">
            <div class="edgecase-output-box" style="padding:0.6rem;">
              <div class="edgecase-output-label">Step Size (LSB)</div>
              <div class="edgecase-output-val" id="ec-cr-calc-lsb" style="font-size:0.8rem;">471.4 mV</div>
            </div>
            <div class="edgecase-output-box" style="padding:0.6rem;">
              <div class="edgecase-output-label">Sampling Period</div>
              <div class="edgecase-output-val" id="ec-cr-calc-period" style="font-size:0.8rem;">50.0 ms</div>
            </div>
            <div class="edgecase-output-box" style="padding:0.6rem;">
              <div class="edgecase-output-label">Nyquist Threshold</div>
              <div class="edgecase-output-val" id="ec-cr-calc-nyquist" style="font-size:0.8rem;">6 Hz</div>
            </div>
            <div class="edgecase-output-box" style="padding:0.6rem;">
              <div class="edgecase-output-label">Nyquist Criteria</div>
              <div class="edgecase-output-val" id="ec-cr-calc-nyq-status" style="font-size:0.8rem;">Satisfied</div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <div class="pipeline-step">Digital Output Buffer Log</div>
        <div class="terminal-box" id="ec-cr-log" style="height:180px; font-size:0.68rem; padding:0.5rem; overflow-y:auto; line-height:1.4;">
          <!-- Decoded data logs -->
        </div>
      </div>
    </div>
  `;

  // References
  const typeSelect = document.getElementById('ec-cr-type');
  const freqSlider = document.getElementById('ec-cr-freq');
  const freqVal = document.getElementById('ec-cr-freq-val');
  const ampSlider = document.getElementById('ec-cr-amp');
  const ampVal = document.getElementById('ec-cr-amp-val');
  const resSelect = document.getElementById('ec-cr-res');
  const rateSlider = document.getElementById('ec-cr-rate');
  const rateVal = document.getElementById('ec-cr-rate-val');
  const svg = document.getElementById('ec-cr-svg');
  const logDiv = document.getElementById('ec-cr-log');

  const calcLsb = document.getElementById('ec-cr-calc-lsb');
  const calcPeriod = document.getElementById('ec-cr-calc-period');
  const calcNyquist = document.getElementById('ec-cr-calc-nyquist');
  const calcNyqStatus = document.getElementById('ec-cr-calc-nyq-status');

  // Listeners
  typeSelect.addEventListener('change', updateSimulation);
  resSelect.addEventListener('change', updateSimulation);

  freqSlider.addEventListener('input', () => {
    freqVal.textContent = `${freqSlider.value} Hz`;
    updateSimulation();
  });

  ampSlider.addEventListener('input', () => {
    ampVal.textContent = `${(ampSlider.value / 10).toFixed(1)}V`;
    updateSimulation();
  });

  rateSlider.addEventListener('input', () => {
    rateVal.textContent = `${rateSlider.value} Hz`;
    updateSimulation();
  });

  function updateSimulation() {
    if (!document.getElementById('capturing-reality')) return;

    const signalType = typeSelect.value;
    const f_sig = parseFloat(freqSlider.value);
    const amp = parseFloat(ampSlider.value) / 10;
    const res = parseInt(resSelect.value);
    const f_sample = parseFloat(rateSlider.value);

    // Calculate metrics
    const steps = Math.pow(2, res) - 1;
    const lsb = (3.3 / steps) * 1000;
    calcLsb.textContent = `${lsb.toFixed(1)} mV`;

    const samplePeriodMs = 1000 / f_sample;
    calcPeriod.textContent = `${samplePeriodMs.toFixed(1)} ms`;

    const nyquist = 2 * f_sig;
    calcNyquist.textContent = `${nyquist} Hz`;

    const satisfiesNyquist = f_sample >= nyquist;
    if (satisfiesNyquist) {
      calcNyqStatus.innerHTML = `<span style="color:#10B981;font-weight:bold;">✓ Met</span>`;
    } else {
      calcNyqStatus.innerHTML = `<span style="color:#EF6868;font-weight:bold;">✗ Violated</span>`;
    }

    // Render SVG Waveforms
    const width = 800;
    const height = 240;
    const padding = 40;
    const plotW = width - 2 * padding;
    const plotH = height - 2 * padding;

    function getAnalogVoltage(t) {
      const center = 1.65;
      const maxAmp = Math.min(amp, 1.65);

      if (signalType === 'sine') {
        return center + maxAmp * Math.sin(2 * Math.PI * f_sig * t);
      } else if (signalType === 'triangle') {
        const period = 1 / f_sig;
        const phase = (t % period) / period;
        const value = phase < 0.5 ? (4 * phase - 1) : (3 - 4 * phase);
        return center + maxAmp * value;
      } else if (signalType === 'sawtooth') {
        const period = 1 / f_sig;
        const phase = (t % period) / period;
        return center + maxAmp * (2 * phase - 1);
      } else {
        const s1 = Math.sin(2 * Math.PI * f_sig * t);
        const s2 = 0.3 * Math.sin(2 * Math.PI * (f_sig * 2.3) * t + 1.2);
        const n = 0.15 * Math.sin(100 * t);
        return center + (maxAmp / 1.3) * (s1 + s2 + n);
      }
    }

    function getX(t) {
      return padding + t * plotW;
    }
    function getY(v) {
      const clampedV = Math.max(0, Math.min(3.3, v));
      return height - padding - (clampedV / 3.3) * plotH;
    }

    let svgContent = `
      <!-- Background Grid -->
      <defs>
        <pattern id="cr-grid" width="20" height="20" patternUnits="userSpaceOnUse">
          <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(148,163,184,0.03)" stroke-width="1"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#cr-grid)" rx="6" />
      
      <!-- Ruler Grid Lines for Quantization Levels -->
      <line x1="${padding}" y1="${padding}" x2="${width - padding}" y2="${padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />
      <text x="${padding - 28}" y="${padding + 4}" fill="var(--muted)" font-family="var(--mono)" font-size="9">3.3V</text>
      
      <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />
      <text x="${padding - 28}" y="${height - padding + 4}" fill="var(--muted)" font-family="var(--mono)" font-size="9">0V</text>
      
      <line x1="${padding}" y1="${height / 2}" x2="${width - padding}" y2="${height / 2}" stroke="rgba(148, 163, 184, 0.08)" stroke-width="1" stroke-dasharray="2,2" />
      <text x="${padding - 33}" y="${height / 2 + 4}" fill="var(--muted)" font-family="var(--mono)" font-size="9">1.65V</text>
    `;

    let analogPath = "";
    const stepsCount = 200;
    for (let i = 0; i <= stepsCount; i++) {
      const t = i / stepsCount;
      const v = getAnalogVoltage(t);
      const x = getX(t);
      const y = getY(v);
      if (i === 0) {
        analogPath += `M ${x} ${y}`;
      } else {
        analogPath += ` L ${x} ${y}`;
      }
    }
    svgContent += `<path d="${analogPath}" fill="none" stroke="rgba(148, 163, 184, 0.3)" stroke-width="2" />`;

    const totalSamples = Math.floor(f_sample);
    let samplePoints = [];
    let reconstructedPoints = [];
    let logLines = [];

    for (let i = 0; i <= totalSamples; i++) {
      const t = i / f_sample;
      if (t > 1.0) break;

      const v_anal = getAnalogVoltage(t);
      const rawCode = Math.round((v_anal / 3.3) * steps);
      const code = Math.max(0, Math.min(steps, rawCode));
      const v_quant = (code / steps) * 3.3;

      const x = getX(t);
      const y_quant = getY(v_quant);

      samplePoints.push({ x, y: y_quant, t, v_anal, v_quant, code });

      if (i === 0) {
        reconstructedPoints.push({ x, y: y_quant });
      } else {
        reconstructedPoints.push({ x, y: samplePoints[i - 1].y });
        reconstructedPoints.push({ x, y: y_quant });
      }

      const timeMs = (t * 1000).toFixed(1);
      const binCode = code.toString(2).padStart(res, '0');
      const hexCode = code.toString(16).toUpperCase().padStart(2, '0');
      logLines.push(`[${timeMs}ms] Vin = ${v_anal.toFixed(3)}V -> ADC: ${code} (0b${binCode} / 0x${hexCode}) -> Vout = ${v_quant.toFixed(3)}V`);
    }

    samplePoints.forEach(pt => {
      svgContent += `<line x1="${pt.x}" y1="${padding}" x2="${pt.x}" y2="${height - padding}" stroke="rgba(59, 130, 246, 0.15)" stroke-width="1" stroke-dasharray="3,3" />`;
    });

    let staircasePath = "";
    reconstructedPoints.forEach((pt, idx) => {
      if (idx === 0) {
        staircasePath += `M ${pt.x} ${pt.y}`;
      } else {
        staircasePath += ` L ${pt.x} ${pt.y}`;
      }
    });
    if (samplePoints.length > 0) {
      staircasePath += ` L ${width - padding} ${samplePoints[samplePoints.length - 1].y}`;
    }
    svgContent += `<path d="${staircasePath}" fill="none" stroke="#10B981" stroke-width="2" />`;

    samplePoints.forEach(pt => {
      svgContent += `
        <circle cx="${pt.x}" cy="${pt.y}" r="3.5" fill="#EF6868" />
        <circle cx="${pt.x}" cy="${pt.y}" r="6" fill="none" stroke="#EF6868" stroke-width="1" opacity="0.4" />
      `;
    });

    svg.innerHTML = svgContent;

    logDiv.innerHTML = logLines.map(line => `<div>${escHtml(line)}</div>`).join('');
    logDiv.scrollTop = logDiv.scrollHeight;
  }

  updateSimulation();
}

function renderCostOfObservation() {
  const container = document.getElementById('cost-of-observation');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Cost of Observation</div>
    <div class="edgecase-subheader">Visualizing Signal Corruptions: Aliasing, Clipping & Quantization Noise</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Adjust parameters below to trigger typical measurement errors: sample below 2x frequency to induce aliasing; drop reference voltage below amplitude to clip; lower resolution to increase quantization steps.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Measurement System Parameters</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:1.25rem;">
        <div class="edgecase-control-group">
          <label for="ec-co-freq">Signal Frequency (Hz)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-co-freq" class="edgecase-slider" min="1" max="15" value="5">
            <span id="ec-co-freq-val" class="edgecase-slider-val">5 Hz</span>
          </div>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-co-rate">Sampling Rate (Hz)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-co-rate" class="edgecase-slider" min="2" max="30" value="8">
            <span id="ec-co-rate-val" class="edgecase-slider-val">8 Hz</span>
          </div>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-co-res">ADC Resolution</label>
          <select id="ec-co-res" class="edgecase-select">
            <option value="3" selected>3-bit (8 Levels)</option>
            <option value="4">4-bit (16 Levels)</option>
            <option value="12">12-bit (4096 Levels)</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-co-vref">Reference Voltage (V)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-co-vref" class="edgecase-slider" min="10" max="50" value="25">
            <span id="ec-co-vref-val" class="edgecase-slider-val">2.5V</span>
          </div>
        </div>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Measured Reconstructed Signal (Green) vs. True Analog Wave (Gray)</div>
    <div class="edgecase-visual" style="background:#0F172A; padding:1.25rem;">
      <svg id="ec-co-svg" viewBox="0 0 800 240" style="width:100%; height:auto; overflow:visible;">
        <!-- Waveforms will be drawn dynamically -->
      </svg>
    </div>

    <!-- DIAGNOSTIC STATUS PANEL -->
    <div class="pipeline-step">System Diagnostic Lock Alerts</div>
    <div class="edgecase-output-panel" style="padding:1rem;">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1rem;" id="ec-co-alerts-grid">
        <!-- Dynamic warnings go here -->
      </div>
    </div>
  `;

  // References
  const freqSlider = document.getElementById('ec-co-freq');
  const freqVal = document.getElementById('ec-co-freq-val');
  const rateSlider = document.getElementById('ec-co-rate');
  const rateVal = document.getElementById('ec-co-rate-val');
  const resSelect = document.getElementById('ec-co-res');
  const vrefSlider = document.getElementById('ec-co-vref');
  const vrefVal = document.getElementById('ec-co-vref-val');
  const svg = document.getElementById('ec-co-svg');
  const alertsGrid = document.getElementById('ec-co-alerts-grid');

  // Event Listeners
  resSelect.addEventListener('change', updateSimulation);

  freqSlider.addEventListener('input', () => {
    freqVal.textContent = `${freqSlider.value} Hz`;
    updateSimulation();
  });

  rateSlider.addEventListener('input', () => {
    rateVal.textContent = `${rateSlider.value} Hz`;
    updateSimulation();
  });

  vrefSlider.addEventListener('input', () => {
    vrefVal.textContent = `${(vrefSlider.value / 10).toFixed(1)}V`;
    updateSimulation();
  });

  function updateSimulation() {
    if (!document.getElementById('cost-of-observation')) return;

    const f_sig = parseFloat(freqSlider.value);
    const f_sample = parseFloat(rateSlider.value);
    const res = parseInt(resSelect.value);
    const vref = parseFloat(vrefSlider.value) / 10;

    const sig_center = 1.65;
    const sig_amp = 1.3;

    // Check failure modes
    const isAliased = f_sample < 2 * f_sig;
    const isClipped = (sig_center + sig_amp > vref) || (sig_center - sig_amp < 0);
    const hasHighNoise = res === 3;
    const hasRangeUnderutilization = vref >= 4.0;

    // Build diagnostics
    let alertsHtml = "";
    if (isAliased) {
      alertsHtml += `
        <div class="agreement-item agreement-fail" style="border-radius:6px; padding:0.6rem; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2);">
          <div style="font-weight:bold; font-size:0.75rem;">✗ ALIASING DETECTED</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">Sample rate ${f_sample} Hz is less than Nyquist rate (${2 * f_sig} Hz). High-frequency detail is folded back into a false lower frequency.</div>
        </div>
      `;
    } else {
      alertsHtml += `
        <div class="agreement-item agreement-ok" style="border-radius:6px; padding:0.6rem; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);">
          <div style="font-weight:bold; font-size:0.75rem;">✓ NYQUIST LOCK</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">Sample rate is sufficient to capture waveforms without folding distortion.</div>
        </div>
      `;
    }

    if (isClipped) {
      alertsHtml += `
        <div class="agreement-item agreement-fail" style="border-radius:6px; padding:0.6rem; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2);">
          <div style="font-weight:bold; font-size:0.75rem;">✗ SIGNAL CLIPPING</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">Signal peak (${(sig_center + sig_amp).toFixed(2)}V) exceeds VREF (${vref.toFixed(1)}V). Voltage above VREF is saturated to maximum digital code.</div>
        </div>
      `;
    } else if (hasRangeUnderutilization) {
      alertsHtml += `
        <div class="agreement-item" style="border-radius:6px; padding:0.6rem; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); color:#F59E0B;">
          <div style="font-weight:bold; font-size:0.75rem;">⚠ UNDER-UTILIZED RANGE</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">VREF (${vref.toFixed(1)}V) is much larger than signal peak. Digital counts use only a fraction of dynamic range.</div>
        </div>
      `;
    } else {
      alertsHtml += `
        <div class="agreement-item agreement-ok" style="border-radius:6px; padding:0.6rem; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);">
          <div style="font-weight:bold; font-size:0.75rem;">✓ RANGE ALIGNED</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">VREF perfectly envelopes the signal span without saturation or wasteful range.</div>
        </div>
      `;
    }

    if (hasHighNoise) {
      alertsHtml += `
        <div class="agreement-item" style="border-radius:6px; padding:0.6rem; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); color:#F59E0B;">
          <div style="font-weight:bold; font-size:0.75rem;">⚠ QUANTIZATION STEPS</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">3-bit resolution mesh divides VREF into only 8 steps. Severe rounding error results in coarse signal steps.</div>
        </div>
      `;
    } else {
      alertsHtml += `
        <div class="agreement-item agreement-ok" style="border-radius:6px; padding:0.6rem; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);">
          <div style="font-weight:bold; font-size:0.75rem;">✓ LOW QUANTIZATION NOISE</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">Resolution is fine enough to approximate the curve smoothly.</div>
        </div>
      `;
    }

    alertsGrid.innerHTML = alertsHtml;

    // Render SVG
    const width = 800;
    const height = 240;
    const padding = 40;
    const plotW = width - 2 * padding;
    const plotH = height - 2 * padding;

    function getAnalogVoltage(t) {
      return sig_center + sig_amp * Math.sin(2 * Math.PI * f_sig * t);
    }

    function getX(t) {
      return padding + t * plotW;
    }
    function getY(v) {
      const clampedV = Math.max(0, Math.min(vref, v));
      return height - padding - (clampedV / vref) * plotH;
    }

    let svgContent = `
      <rect width="100%" height="100%" fill="none" rx="6" />
      <line x1="${padding}" y1="${padding}" x2="${width - padding}" y2="${padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />
      <text x="${padding - 28}" y="${padding + 4}" fill="var(--muted)" font-family="var(--mono)" font-size="9">${vref.toFixed(1)}V</text>
      
      <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />
      <text x="${padding - 28}" y="${height - padding + 4}" fill="var(--muted)" font-family="var(--mono)" font-size="9">0V</text>
    `;

    let analogPath = "";
    const stepsCount = 200;
    for (let i = 0; i <= stepsCount; i++) {
      const t = i / stepsCount;
      const v = getAnalogVoltage(t);
      const x = getX(t);
      const y = getY(v);
      if (i === 0) {
        analogPath += `M ${x} ${y}`;
      } else {
        analogPath += ` L ${x} ${y}`;
      }
    }
    svgContent += `<path d="${analogPath}" fill="none" stroke="rgba(148, 163, 184, 0.2)" stroke-width="2" />`;

    const steps = Math.pow(2, res) - 1;
    const totalSamples = Math.floor(f_sample);
    let samplePoints = [];
    let reconstructedPoints = [];

    for (let i = 0; i <= totalSamples; i++) {
      const t = i / f_sample;
      if (t > 1.0) break;

      const v_anal = getAnalogVoltage(t);
      const rawCode = Math.round((v_anal / vref) * steps);
      const code = Math.max(0, Math.min(steps, rawCode));
      const v_quant = (code / steps) * vref;

      const x = getX(t);
      const y_quant = getY(v_quant);

      samplePoints.push({ x, y: y_quant });

      if (i === 0) {
        reconstructedPoints.push({ x, y: y_quant });
      } else {
        reconstructedPoints.push({ x, y: samplePoints[i - 1].y });
        reconstructedPoints.push({ x, y: y_quant });
      }
    }

    samplePoints.forEach(pt => {
      svgContent += `<line x1="${pt.x}" y1="${padding}" x2="${pt.x}" y2="${height - padding}" stroke="rgba(59, 130, 246, 0.12)" stroke-width="1" stroke-dasharray="3,3" />`;
    });

    let staircasePath = "";
    reconstructedPoints.forEach((pt, idx) => {
      if (idx === 0) {
        staircasePath += `M ${pt.x} ${pt.y}`;
      } else {
        staircasePath += ` L ${pt.x} ${pt.y}`;
      }
    });
    if (samplePoints.length > 0) {
      staircasePath += ` L ${width - padding} ${samplePoints[samplePoints.length - 1].y}`;
    }
    svgContent += `<path d="${staircasePath}" fill="none" stroke="#10B981" stroke-width="2" />`;

    samplePoints.forEach(pt => {
      svgContent += `<circle cx="${pt.x}" cy="${pt.y}" r="3" fill="#EF6868" />`;
    });

    svg.innerHTML = svgContent;
  }

  updateSimulation();
}

function renderPaintingWithVoltage() {
  const container = document.getElementById('painting-with-voltage');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: Painting with Voltage</div>
    <div class="edgecase-subheader">Watch Numbers Become Analog Voltages</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Adjust resolution, reference voltage, and digital input value to watch how a number transforms into an analog voltage level.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Converter Configuration</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:1.25rem;">
        <div class="edgecase-control-group">
          <label for="ec-pv-res">DAC Resolution</label>
          <select id="ec-pv-res" class="edgecase-select">
            <option value="3" selected>3-bit (8 Levels)</option>
            <option value="4">4-bit (16 Levels)</option>
            <option value="8">8-bit (256 Levels)</option>
            <option value="12">12-bit (4096 Levels)</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-pv-vref">Reference Voltage (V)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-pv-vref" class="edgecase-slider" min="10" max="50" value="33">
            <span id="ec-pv-vref-val" class="edgecase-slider-val">3.3V</span>
          </div>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-pv-code">Digital Input Code</label>
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <input type="range" id="ec-pv-code" class="edgecase-slider" min="0" max="7" value="4" style="flex-grow:1;">
            <span id="ec-pv-code-val" class="edgecase-slider-val" style="min-width:45px;">4</span>
          </div>
        </div>
      </div>
    </div>

    <!-- METRICS & GAUGE PANEL -->
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-top:1rem;">
      <!-- GAUGE DISPLAY -->
      <div>
        <div class="pipeline-step">Analog Voltmeter Gauge</div>
        <div class="edgecase-visual" style="background:#0F172A; padding:1.25rem; display:flex; justify-content:center; align-items:center; min-height:220px;">
          <svg id="ec-pv-svg" viewBox="0 0 300 200" style="width:100%; max-width:260px; height:auto; overflow:visible;">
            <!-- Voltmeter drawn dynamically -->
          </svg>
        </div>
      </div>

      <!-- METRICS & DIGITAL OUT -->
      <div>
        <div class="pipeline-step">Output Calculations & Register Log</div>
        <div class="edgecase-output-panel" style="min-height:220px; display:flex; flex-direction:column; justify-content:space-between;">
          <div class="edgecase-output-grid" style="grid-template-columns: 1fr 1fr; gap:0.75rem; padding:0.25rem;">
            <div class="edgecase-output-box" style="padding:0.5rem;">
              <div class="edgecase-output-label">Resolution Steps</div>
              <div class="edgecase-output-val" id="ec-pv-calc-steps" style="font-size:0.8rem;">8 Steps</div>
            </div>
            <div class="edgecase-output-box" style="padding:0.5rem;">
              <div class="edgecase-output-label">LSB Size (Step Width)</div>
              <div class="edgecase-output-val" id="ec-pv-calc-lsb" style="font-size:0.8rem;">471.4 mV</div>
            </div>
            <div class="edgecase-output-box" style="padding:0.5rem;">
              <div class="edgecase-output-label">Binary Value</div>
              <div class="edgecase-output-val" id="ec-pv-calc-binary" style="font-size:0.8rem; font-family:var(--mono);">100</div>
            </div>
            <div class="edgecase-output-box" style="padding:0.5rem;">
              <div class="edgecase-output-label">Output Voltage</div>
              <div class="edgecase-output-val" id="ec-pv-calc-vout" style="font-size:0.9rem; font-weight:bold; color:#10B981;">1.886 V</div>
            </div>
          </div>
          
          <div class="terminal-box" id="ec-pv-log" style="height:85px; font-size:0.65rem; padding:0.4rem; overflow-y:auto; line-height:1.3; margin-top:0.5rem;">
            <!-- Register transaction logs -->
          </div>
        </div>
      </div>
    </div>
  `;

  // References
  const resSelect = document.getElementById('ec-pv-res');
  const vrefSlider = document.getElementById('ec-pv-vref');
  const vrefVal = document.getElementById('ec-pv-vref-val');
  const codeSlider = document.getElementById('ec-pv-code');
  const codeVal = document.getElementById('ec-pv-code-val');
  const svg = document.getElementById('ec-pv-svg');
  const logDiv = document.getElementById('ec-pv-log');

  const calcSteps = document.getElementById('ec-pv-calc-steps');
  const calcLsb = document.getElementById('ec-pv-calc-lsb');
  const calcBinary = document.getElementById('ec-pv-calc-binary');
  const calcVout = document.getElementById('ec-pv-calc-vout');

  // Event Listeners
  resSelect.addEventListener('change', () => {
    const res = parseInt(resSelect.value);
    const steps = Math.pow(2, res) - 1;
    codeSlider.max = steps;
    // Set a proportional value
    const fraction = parseFloat(codeSlider.value) / parseInt(codeSlider.max);
    codeSlider.value = Math.round(fraction * steps);
    codeVal.textContent = codeSlider.value;
    updateSimulation();
  });

  vrefSlider.addEventListener('input', () => {
    vrefVal.textContent = `${(vrefSlider.value / 10).toFixed(1)}V`;
    updateSimulation();
  });

  codeSlider.addEventListener('input', () => {
    codeVal.textContent = codeSlider.value;
    updateSimulation();
  });

  let lastCode = -1;
  let lastRes = -1;
  let lastVref = -1;

  function updateSimulation() {
    if (!document.getElementById('painting-with-voltage')) return;

    const res = parseInt(resSelect.value);
    const vref = parseFloat(vrefSlider.value) / 10;
    const code = parseInt(codeSlider.value);
    const steps = Math.pow(2, res) - 1;

    // Constrain code
    const validCode = Math.max(0, Math.min(steps, code));

    // Calculate metrics
    const lsb = (vref / steps) * 1000;
    const vout = (validCode / steps) * vref;

    calcSteps.textContent = `${steps + 1} Levels`;
    calcLsb.textContent = `${lsb.toFixed(1)} mV`;
    calcBinary.textContent = validCode.toString(2).padStart(res, '0');
    calcVout.textContent = `${vout.toFixed(3)} V`;

    // Append to register log if anything changed
    if (validCode !== lastCode || res !== lastRes || vref !== lastVref) {
      const timestamp = new Date().toISOString().slice(11, 19);
      const hexStr = "0x" + validCode.toString(16).toUpperCase().padStart(Math.ceil(res/4), '0');
      let logLine = `[${timestamp}] Write Register: ${hexStr} (Bin: ${validCode.toString(2).padStart(res, '0')}) -> Output: ${vout.toFixed(3)} V`;
      logDiv.innerHTML += `<div>${escHtml(logLine)}</div>`;
      logDiv.scrollTop = logDiv.scrollHeight;
      
      lastCode = validCode;
      lastRes = res;
      lastVref = vref;
    }

    // Render SVG Voltmeter
    const cx = 150;
    const cy = 130;
    const r = 80;
    const fraction = vout / vref;
    const angle = Math.PI * (1 - fraction); // Semicircle from left to right

    // Needle coordinates
    const nx = cx + r * Math.cos(angle);
    const ny = cy - r * Math.sin(angle);

    // Build meter arcs
    let meterContent = `
      <!-- Background grid pattern -->
      <defs>
        <pattern id="pv-grid" width="15" height="15" patternUnits="userSpaceOnUse">
          <path d="M 15 0 L 0 0 0 15" fill="none" stroke="rgba(148,163,184,0.03)" stroke-width="1"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#pv-grid)" rx="6" />

      <!-- Outer voltmeter arc outline -->
      <path d="M 60 130 A 90 90 0 0 1 240 130" fill="none" stroke="rgba(148, 163, 184, 0.15)" stroke-width="8" stroke-linecap="round" />
      <path d="M 60 130 A 90 90 0 0 1 ${cx + 90 * Math.cos(angle)} ${cy - 90 * Math.sin(angle)}" fill="none" stroke="#10B981" stroke-width="8" stroke-linecap="round" />

      <!-- Center spindle -->
      <circle cx="${cx}" cy="${cy}" r="12" fill="#1E293B" stroke="rgba(148, 163, 184, 0.3)" stroke-width="2" />
      <circle cx="${cx}" cy="${cy}" r="4" fill="#EF6868" />

      <!-- Needle pointer line -->
      <line x1="${cx}" y1="${cy}" x2="${nx}" y2="${ny}" stroke="#EF6868" stroke-width="2.5" stroke-linecap="round" />

      <!-- Scale Ticks (5 ticks: 0%, 25%, 50%, 75%, 100%) -->
    `;

    for (let i = 0; i <= 4; i++) {
      const frac = i / 4;
      const a = Math.PI * (1 - frac);
      const txStart = cx + 86 * Math.cos(a);
      const tyStart = cy - 86 * Math.sin(a);
      const txEnd = cx + 94 * Math.cos(a);
      const tyEnd = cy - 94 * Math.sin(a);
      const lx = cx + 106 * Math.cos(a);
      const ly = cy - 106 * Math.sin(a);
      
      const vTick = frac * vref;

      meterContent += `
        <line x1="${txStart}" y1="${tyStart}" x2="${txEnd}" y2="${tyEnd}" stroke="rgba(148, 163, 184, 0.4)" stroke-width="1.5" />
        <text x="${lx}" y="${ly + 3}" fill="var(--muted)" font-family="var(--mono)" font-size="7" text-anchor="middle">${vTick.toFixed(1)}V</text>
      `;
    }

    // Text Display inside meter
    meterContent += `
      <text x="${cx}" y="${cy + 30}" fill="#FFF" font-weight="bold" font-size="14" text-anchor="middle">${vout.toFixed(3)} V</text>
      <text x="${cx}" y="${cy + 45}" fill="var(--muted)" font-family="var(--mono)" font-size="8" text-anchor="middle">DAC OUTPUT</text>
    `;

    svg.innerHTML = meterContent;
  }

  updateSimulation();
}

function renderIllusionOfSmoothness() {
  const container = document.getElementById('illusion-of-smoothness');
  if (!container) return;

  container.className = 'edgecase-wrapper';

  container.innerHTML = `
    <div class="edgecase-header">EdgeCase: The Illusion of Smoothness</div>
    <div class="edgecase-subheader">How Sequence Timing & Filters Create Continuous Waves</div>
    <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-bottom:1.5rem;">
      Adjust the waveform type, resolution, update frequency, and filter cutoff to witness how discrete staircases are integrated into smooth analog physics.
    </div>

    <!-- CONFIGURATION SETTINGS -->
    <div class="pipeline-step">Signal Generation & Filtering Parameters</div>
    <div class="panel-box">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:1.25rem;">
        <div class="edgecase-control-group">
          <label for="ec-is-type">Waveform Type</label>
          <select id="ec-is-type" class="edgecase-select">
            <option value="sine" selected>Sine Wave</option>
            <option value="triangle">Triangle Wave</option>
            <option value="sawtooth">Sawtooth Wave</option>
            <option value="square">Square Wave</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-is-res">DAC Resolution</label>
          <select id="ec-is-res" class="edgecase-select">
            <option value="3" selected>3-bit (8 Levels)</option>
            <option value="4">4-bit (16 Levels)</option>
            <option value="8">8-bit (256 Levels)</option>
          </select>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-is-rate">Update Frequency (Hz)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-is-rate" class="edgecase-slider" min="10" max="120" value="30">
            <span id="ec-is-rate-val" class="edgecase-slider-val">30 Hz</span>
          </div>
        </div>
        <div class="edgecase-control-group">
          <label for="ec-is-cutoff">RC Filter Cutoff (Hz)</label>
          <div class="edgecase-slider-container">
            <input type="range" id="ec-is-cutoff" class="edgecase-slider" min="5" max="100" value="40">
            <span id="ec-is-cutoff-val" class="edgecase-slider-val">40 Hz</span>
          </div>
        </div>
      </div>
    </div>

    <!-- WAVEFORM DISPLAY -->
    <div class="pipeline-step">Continuous Ideal (Gray) vs. Stepped DAC (Red) vs. Reconstructed Analog (Green)</div>
    <div class="edgecase-visual" style="background:#0F172A; padding:1.25rem;">
      <svg id="ec-is-svg" viewBox="0 0 800 240" style="width:100%; height:auto; overflow:visible;">
        <!-- Waveforms drawn dynamically -->
      </svg>
    </div>

    <!-- DIAGNOSTIC STATUS PANEL -->
    <div class="pipeline-step">Filter Alignment Alert</div>
    <div class="edgecase-output-panel" style="padding:1rem;">
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:1rem;" id="ec-is-alerts-grid">
        <!-- Alerts output dynamically -->
      </div>
    </div>
  `;

  // References
  const typeSelect = document.getElementById('ec-is-type');
  const resSelect = document.getElementById('ec-is-res');
  const rateSlider = document.getElementById('ec-is-rate');
  const rateVal = document.getElementById('ec-is-rate-val');
  const cutoffSlider = document.getElementById('ec-is-cutoff');
  const cutoffVal = document.getElementById('ec-is-cutoff-val');
  const svg = document.getElementById('ec-is-svg');
  const alertsGrid = document.getElementById('ec-is-alerts-grid');

  // Listeners
  typeSelect.addEventListener('change', updateSimulation);
  resSelect.addEventListener('change', updateSimulation);

  rateSlider.addEventListener('input', () => {
    rateVal.textContent = `${rateSlider.value} Hz`;
    updateSimulation();
  });

  cutoffSlider.addEventListener('input', () => {
    cutoffVal.textContent = `${cutoffSlider.value} Hz`;
    updateSimulation();
  });

  function updateSimulation() {
    if (!document.getElementById('illusion-of-smoothness')) return;

    const waveType = typeSelect.value;
    const res = parseInt(resSelect.value);
    const f_update = parseFloat(rateSlider.value);
    const f_cutoff = parseFloat(cutoffSlider.value);

    const f_sig = 3;
    const vref = 3.3;
    const sig_center = 1.65;
    const sig_amp = 1.2;
    const steps = Math.pow(2, res) - 1;

    const isFilterTooHigh = f_cutoff > f_update * 0.7;
    const isFilterTooLow = f_cutoff < f_sig * 1.5;

    let alertsHtml = "";
    if (isFilterTooHigh) {
      alertsHtml += `
        <div class="agreement-item" style="border-radius:6px; padding:0.6rem; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); color:#F59E0B;">
          <div style="font-weight:bold; font-size:0.75rem;">⚠ INSUFFICIENT FILTERING</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">Filter cutoff (${f_cutoff} Hz) is too close to update rate (${f_update} Hz). High-frequency switching staircases remain visible on the output.</div>
        </div>
      `;
    } else if (isFilterTooLow) {
      alertsHtml += `
        <div class="agreement-item agreement-fail" style="border-radius:6px; padding:0.6rem; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2);">
          <div style="font-weight:bold; font-size:0.75rem;">✗ SEVERE ATTENUATION</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">Filter cutoff (${f_cutoff} Hz) is too low. The filter blocks our target signal (${f_sig} Hz), leading to massive amplitude loss and phase delay.</div>
        </div>
      `;
    } else {
      alertsHtml += `
        <div class="agreement-item agreement-ok" style="border-radius:6px; padding:0.6rem; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);">
          <div style="font-weight:bold; font-size:0.75rem;">✓ RECONSTRUCTION LOCK</div>
          <div style="font-size:0.6rem; color:var(--muted); margin-top:0.15rem;">Cutoff frequency is balanced. High-frequency steps are completely smoothed out while preserving signal amplitude.</div>
        </div>
      `;
    }
    alertsGrid.innerHTML = alertsHtml;

    const width = 800;
    const height = 240;
    const padding = 40;
    const plotW = width - 2 * padding;
    const plotH = height - 2 * padding;

    function getIdealVoltage(t) {
      if (waveType === 'sine') {
        return sig_center + sig_amp * Math.sin(2 * Math.PI * f_sig * t);
      } else if (waveType === 'triangle') {
        const period = 1 / f_sig;
        const phase = (t % period) / period;
        const val = phase < 0.5 ? (4 * phase - 1) : (3 - 4 * phase);
        return sig_center + sig_amp * val;
      } else if (waveType === 'sawtooth') {
        const period = 1 / f_sig;
        const phase = (t % period) / period;
        return sig_center + sig_amp * (2 * phase - 1);
      } else {
        const val = Math.sin(2 * Math.PI * f_sig * t) >= 0 ? 1 : -1;
        return sig_center + sig_amp * val;
      }
    }

    function getX(t) {
      return padding + t * plotW;
    }
    function getY(v) {
      const clampedV = Math.max(0, Math.min(vref, v));
      return height - padding - (clampedV / vref) * plotH;
    }

    let svgContent = `
      <rect width="100%" height="100%" fill="none" rx="6" />
      <line x1="${padding}" y1="${padding}" x2="${width - padding}" y2="${padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />
      <text x="${padding - 28}" y="${padding + 4}" fill="var(--muted)" font-family="var(--mono)" font-size="9">3.3V</text>
      
      <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />
      <text x="${padding - 28}" y="${height - padding + 4}" fill="var(--muted)" font-family="var(--mono)" font-size="9">0V</text>
    `;

    let idealPath = "";
    const samplesCount = 300;
    for (let i = 0; i <= samplesCount; i++) {
      const t = i / samplesCount;
      const v = getIdealVoltage(t);
      const x = getX(t);
      const y = getY(v);
      if (i === 0) idealPath += `M ${x} ${y}`;
      else idealPath += ` L ${x} ${y}`;
    }
    svgContent += `<path d="${idealPath}" fill="none" stroke="rgba(148, 163, 184, 0.18)" stroke-width="1.5" stroke-dasharray="3,3" />`;

    const updateSteps = Math.floor(f_update);
    let stepPoints = [];
    for (let i = 0; i <= updateSteps; i++) {
      const t = i / f_update;
      const v_ideal = getIdealVoltage(t);
      const rawCode = Math.round((v_ideal / vref) * steps);
      const code = Math.max(0, Math.min(steps, rawCode));
      const v_quant = (code / steps) * vref;
      stepPoints.push({ t, v: v_quant });
    }

    let steppedPath = "";
    stepPoints.forEach((pt, idx) => {
      const x = getX(pt.t);
      const y = getY(pt.v);
      if (idx === 0) {
        steppedPath += `M ${x} ${y}`;
      } else {
        steppedPath += ` H ${x} V ${y}`;
      }
    });
    svgContent += `<path d="${steppedPath}" fill="none" stroke="#EF6868" stroke-width="1.5" stroke-opacity="0.8" />`;

    const dt = 1.0 / samplesCount;
    const tau = 1.0 / (2 * Math.PI * f_cutoff);
    const alpha = dt / (tau + dt);
    
    let filteredPath = "";
    let y_lpf = getIdealVoltage(0);
    
    for (let i = 0; i <= samplesCount; i++) {
      const t = i / samplesCount;
      const activeStepIdx = Math.floor(t * f_update);
      const clampedIdx = Math.min(activeStepIdx, stepPoints.length - 1);
      const x_val = stepPoints[clampedIdx].v;
      
      y_lpf = alpha * x_val + (1.0 - alpha) * y_lpf;
      
      const x = getX(t);
      const y = getY(y_lpf);
      if (i === 0) filteredPath += `M ${x} ${y}`;
      else filteredPath += ` L ${x} ${y}`;
    }
    svgContent += `<path d="${filteredPath}" fill="none" stroke="#10B981" stroke-width="2.5" />`;

    svg.innerHTML = svgContent;
  }

  updateSimulation();
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
