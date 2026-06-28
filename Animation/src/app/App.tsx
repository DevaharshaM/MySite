import treeImage from "@/imports/homeTree.png"
import { motion } from "motion/react"

// Fixed mote data — stable across renders
const MOTES = [
  { x: 42.3, y: 78, sz: 1.8, dur: 8.2,  dl: 4.1,  op: 0.22, dr: -3  },
  { x: 56.1, y: 82, sz: 1.4, dur: 9.5,  dl: 5.3,  op: 0.18, dr:  2  },
  { x: 48.7, y: 75, sz: 2.1, dur: 7.8,  dl: 3.8,  op: 0.24, dr: -1  },
  { x: 53.4, y: 80, sz: 1.6, dur: 10.2, dl: 6.0,  op: 0.20, dr:  3  },
  { x: 44.2, y: 85, sz: 1.3, dur: 8.8,  dl: 4.5,  op: 0.16, dr: -4  },
  { x: 60.8, y: 79, sz: 2.0, dur: 9.1,  dl: 5.8,  op: 0.21, dr:  4  },
  { x: 38.5, y: 83, sz: 1.5, dur: 7.5,  dl: 7.2,  op: 0.17, dr: -2  },
  { x: 50.2, y: 72, sz: 1.9, dur: 11.0, dl: 3.5,  op: 0.20, dr:  1  },
  { x: 55.6, y: 86, sz: 1.2, dur: 8.5,  dl: 8.0,  op: 0.15, dr:  5  },
  { x: 46.4, y: 88, sz: 2.0, dur: 9.8,  dl: 4.8,  op: 0.23, dr: -3  },
  { x: 52.1, y: 74, sz: 1.6, dur: 8.0,  dl: 6.5,  op: 0.19, dr:  2  },
  { x: 40.9, y: 77, sz: 1.4, dur: 10.5, dl: 5.1,  op: 0.16, dr: -5  },
  { x: 58.3, y: 81, sz: 1.8, dur: 7.2,  dl: 7.8,  op: 0.21, dr:  3  },
  { x: 47.7, y: 90, sz: 1.3, dur: 9.3,  dl: 9.2,  op: 0.15, dr: -1  },
  { x: 54.5, y: 76, sz: 2.0, dur: 8.7,  dl: 5.6,  op: 0.24, dr:  4  },
  { x: 43.8, y: 84, sz: 1.7, dur: 10.0, dl: 7.5,  op: 0.19, dr: -4  },
  { x: 49.3, y: 87, sz: 1.5, dur: 9.0,  dl: 4.2,  op: 0.17, dr:  2  },
  { x: 57.2, y: 78, sz: 1.8, dur: 8.3,  dl: 6.8,  op: 0.22, dr: -2  },
  { x: 45.1, y: 80, sz: 1.2, dur: 11.2, dl: 8.5,  op: 0.14, dr:  5  },
  { x: 51.5, y: 83, sz: 2.1, dur: 7.9,  dl: 3.9,  op: 0.26, dr: -3  },
]

export default function App() {
  return (
    <>
      <style>{`
        /* Register custom properties so the browser interpolates them */
        @property --ry {
          syntax: '<percentage>';
          inherits: false;
          initial-value: -30%;
        }
        @property --op {
          syntax: '<number>';
          inherits: false;
          initial-value: 0;
        }
        @property --dr {
          syntax: '<length>';
          inherits: false;
          initial-value: 0px;
        }

        /* Bottom-to-top mask reveal — slow through roots, quickens at canopy */
        @keyframes awaken {
          0%   { --ry: -30%; }
          5%   { --ry: -2%;  }
          22%  { --ry: 26%;  }
          45%  { --ry: 52%;  }
          65%  { --ry: 74%;  }
          82%  { --ry: 90%;  }
          100% { --ry: 132%; }
        }

        .tree-mask {
          animation: awaken 10s cubic-bezier(0.4, 0, 0.2, 1) both;
          mask-image: linear-gradient(
            to top,
            black 0%,
            black var(--ry),
            transparent calc(var(--ry) + 28%),
            transparent 100%
          );
          -webkit-mask-image: linear-gradient(
            to top,
            black 0%,
            black var(--ry),
            transparent calc(var(--ry) + 28%),
            transparent 100%
          );
        }

        /* Leaf sway — starts after reveal completes */
        @keyframes sway {
          0%, 100% { transform: rotate(0deg)      scale(1.000); }
          30%      { transform: rotate(0.38deg)   scale(1.002); }
          70%      { transform: rotate(-0.38deg)  scale(0.999); }
        }

        .sway {
          transform-origin: 50% 90%;
          animation: sway 7.5s ease-in-out infinite;
          animation-delay: 9.5s;
          will-change: transform;
        }

        /* Floating motes — rise and fade */
        @keyframes mote-rise {
          0%   { opacity: 0;           transform: translateY(0px)    translateX(0px);   }
          12%  { opacity: var(--op);                                                     }
          88%  { opacity: var(--op);                                                     }
          100% { opacity: 0;           transform: translateY(-190px) translateX(var(--dr)); }
        }
      `}</style>

      <div
        className="relative w-full h-screen overflow-hidden"
        style={{ background: "#07050c" }}
      >

        {/* ── Sway wrapper (rotates the whole tree) ── */}
        <div className="absolute inset-0 flex items-center justify-center sway">

          {/* ── Mask reveal ── */}
          <div className="tree-mask w-full h-full flex items-center justify-center">
            <img
              src={treeImage}
              alt="Ancient banyan tree awakening at dawn"
              className="w-full h-full object-contain select-none"
              draggable={false}
            />
          </div>
        </div>

        {/* ── Cinematic vignette — always on, frames the scene ── */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background:
              "radial-gradient(ellipse 86% 86% at 50% 48%, transparent 38%, rgba(7,5,12,0.92) 100%)",
          }}
        />

        {/* ── Root spark — first sign of life ── */}
        <motion.div
          className="absolute pointer-events-none"
          style={{
            bottom: "2%",
            left: "50%",
            width: "34%",
            height: "17%",
            background:
              "radial-gradient(ellipse 75% 80% at 50% 95%, rgba(226,158,38,0.72) 0%, rgba(200,120,16,0.36) 42%, transparent 72%)",
            filter: "blur(18px)",
            mixBlendMode: "screen" as const,
          }}
          initial={{ opacity: 0, x: "-50%", scale: 0.12 }}
          animate={{ opacity: 1, x: "-50%", scale: 1 }}
          transition={{ duration: 2.5, ease: [0, 0, 0.35, 1], delay: 0.4 }}
        />

        {/* ── Roots spreading — sap flowing outward through earth ── */}
        <motion.div
          className="absolute pointer-events-none"
          style={{
            bottom: "5%",
            left: "50%",
            width: "78%",
            height: "28%",
            background:
              "radial-gradient(ellipse 100% 62% at 50% 88%, rgba(210,142,28,0.44) 0%, rgba(182,108,12,0.20) 52%, transparent 80%)",
            filter: "blur(26px)",
            mixBlendMode: "screen" as const,
          }}
          initial={{ opacity: 0, x: "-50%", scaleX: 0.08, scaleY: 0.45 }}
          animate={{ opacity: 1, x: "-50%", scaleX: 1, scaleY: 1 }}
          transition={{ duration: 4.2, ease: [0, 0, 0.25, 1], delay: 1.0 }}
        />

        {/* ── Trunk — warmth climbing from root crown ── */}
        <motion.div
          className="absolute pointer-events-none"
          style={{
            bottom: "9%",
            left: "50%",
            width: "22%",
            height: "55%",
            background:
              "radial-gradient(ellipse 55% 100% at 50% 76%, rgba(200,132,24,0.30) 0%, rgba(165,102,8,0.12) 60%, transparent 82%)",
            filter: "blur(28px)",
            mixBlendMode: "screen" as const,
            transformOrigin: "50% 100%",
          }}
          initial={{ opacity: 0, x: "-50%", scaleY: 0.04 }}
          animate={{ opacity: 1, x: "-50%", scaleY: 1 }}
          transition={{ duration: 4.8, ease: [0.25, 0, 0.3, 1], delay: 2.5 }}
        />

        {/* ── Left branch fork ── */}
        <motion.div
          className="absolute pointer-events-none"
          style={{
            bottom: "35%",
            left: "14%",
            width: "38%",
            height: "32%",
            background:
              "radial-gradient(ellipse 100% 100% at 72% 55%, rgba(188,128,20,0.24) 0%, transparent 72%)",
            filter: "blur(24px)",
            mixBlendMode: "screen" as const,
          }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 3.2, ease: "easeOut", delay: 4.8 }}
        />

        {/* ── Right branch fork ── */}
        <motion.div
          className="absolute pointer-events-none"
          style={{
            bottom: "35%",
            right: "14%",
            width: "38%",
            height: "32%",
            background:
              "radial-gradient(ellipse 100% 100% at 28% 55%, rgba(188,128,20,0.24) 0%, transparent 72%)",
            filter: "blur(24px)",
            mixBlendMode: "screen" as const,
          }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 3.2, ease: "easeOut", delay: 5.1 }}
        />

        {/* ── Canopy — the leaves catch the morning warmth ── */}
        <motion.div
          className="absolute pointer-events-none"
          style={{
            top: "4%",
            left: "50%",
            width: "85%",
            height: "58%",
            background:
              "radial-gradient(ellipse 100% 78% at 50% 28%, rgba(178,142,52,0.18) 0%, rgba(152,118,28,0.08) 55%, transparent 80%)",
            filter: "blur(40px)",
            mixBlendMode: "screen" as const,
          }}
          initial={{ opacity: 0, x: "-50%" }}
          animate={{ opacity: 1, x: "-50%" }}
          transition={{ duration: 3.5, ease: "easeOut", delay: 6.2 }}
        />

        {/* ── Ground shadow — sharpens as the tree awakens ── */}
        <motion.div
          className="absolute pointer-events-none"
          style={{
            bottom: 0,
            left: "50%",
            width: "78%",
            height: "10%",
            background:
              "radial-gradient(ellipse 100% 40% at 50% 100%, rgba(3,2,6,0.68) 0%, rgba(3,2,6,0.30) 55%, transparent 82%)",
            filter: "blur(6px)",
          }}
          initial={{ opacity: 0, x: "-50%" }}
          animate={{ opacity: 1, x: "-50%" }}
          transition={{ duration: 6, ease: "easeInOut", delay: 2.5 }}
        />

        {/* ── Floating motes of golden light ── */}
        {MOTES.map((m, i) => (
          <div
            key={i}
            className="absolute pointer-events-none rounded-full"
            style={{
              left: `${m.x}%`,
              top: `${m.y}%`,
              width: `${m.sz}px`,
              height: `${m.sz}px`,
              background: "rgba(220,160,48,0.9)",
              boxShadow: `0 0 ${Math.round(m.sz * 2.5)}px rgba(218,155,44,0.38)`,
              animation: `mote-rise ${m.dur}s ease-in-out infinite ${m.dl}s`,
              "--op": m.op,
              "--dr": `${m.dr}px`,
            } as React.CSSProperties}
          />
        ))}

      </div>
    </>
  )
}
