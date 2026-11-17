/** Pip, an original snake mascot drawn in SVG. Moods change the face and the animation. */
export type Mood = "idle" | "happy" | "sad" | "think" | "cheer";

export function Pip({ mood = "idle", size = 96, say }: { mood?: Mood; size?: number; say?: string }) {
  const pupil = mood === "think" ? { dx: 2, dy: -3 } : mood === "sad" ? { dx: 0, dy: 2 } : { dx: 1, dy: 0 };
  const mouth =
    mood === "sad" ? "M50 53 Q58 47 66 53" :
    mood === "think" ? "M52 51 Q58 50 64 52" :
    mood === "cheer" ? "M48 47 Q58 60 68 47 Z" :
    "M50 48 Q58 56 66 48";
  return (
    <div className={`pip pip-${mood}`} style={{ width: size }}>
      {say && <div className="pip-say" role="status">{say}</div>}
      <svg viewBox="0 0 120 120" width={size} height={size} aria-hidden="true">
        <ellipse cx="60" cy="108" rx="38" ry="6" className="pip-shadow" />
        <g className="pip-body">
          <path d="M22 98 Q60 78 98 98 Q60 116 22 98" className="pip-fill-dark" />
          <path d="M24 97 Q60 80 96 97" className="pip-stroke" strokeWidth="18" />
          <path d="M28 97 Q60 84 92 97" className="pip-belly" strokeWidth="5" strokeDasharray="5 6" />
          <path d="M36 82 Q60 66 84 82" className="pip-stroke" strokeWidth="16" />
          <path d="M40 82 Q60 70 80 82" className="pip-belly" strokeWidth="4" strokeDasharray="5 6" />
          <path d="M80 80 C 92 64, 78 54, 66 48" className="pip-stroke" strokeWidth="15" />
          <g className="pip-head">
            <ellipse cx="58" cy="38" rx="27" ry="23" className="pip-fill" />
            <ellipse cx="50" cy="20" rx="9" ry="4" className="pip-shine" />
            <circle cx="41" cy="45" r="4" className="pip-cheek" />
            <circle cx="75" cy="45" r="4" className="pip-cheek" />
            <g className="pip-eyes">
              <circle cx="48" cy="34" r="8.5" fill="#fff" />
              <circle cx="68" cy="34" r="8.5" fill="#fff" />
              <circle cx={48 + pupil.dx} cy={34 + pupil.dy} r="4.3" className="pip-pupil" />
              <circle cx={68 + pupil.dx} cy={34 + pupil.dy} r="4.3" className="pip-pupil" />
              <circle cx={49.5 + pupil.dx} cy={32.5 + pupil.dy} r="1.4" fill="#fff" />
              <circle cx={69.5 + pupil.dx} cy={32.5 + pupil.dy} r="1.4" fill="#fff" />
            </g>
            {mood === "sad" && <path d="M40 24 L54 27 M76 24 L62 27" className="pip-brow" />}
            <path d={mouth} className={mood === "cheer" ? "pip-mouth-open" : "pip-mouth"} />
            {(mood === "happy" || mood === "cheer") && <path d="M58 57 v6 l-3 3 M58 63 l3 3" className="pip-tongue" />}
          </g>
        </g>
      </svg>
    </div>
  );
}
