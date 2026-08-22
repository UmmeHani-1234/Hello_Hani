export default function Mascot({ size = 96, thinking = false }) {
  return (
    <div
      className={`relative ${thinking ? "animate-breathe" : ""}`}
      style={{ width: size, height: size }}
    >
      <svg viewBox="0 0 120 120" width={size} height={size}>
        <defs>
          <radialGradient id="orbFill" cx="35%" cy="30%" r="80%">
            <stop offset="0%" stopColor="#EFE4F6" />
            <stop offset="55%" stopColor="#C9B7E6" />
            <stop offset="100%" stopColor="#8D82C4" />
          </radialGradient>
          <linearGradient id="orbRim" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#544B82" stopOpacity="0.15" />
          </linearGradient>
        </defs>

        <circle cx="60" cy="62" r="46" fill="url(#orbFill)" />
        <circle cx="60" cy="62" r="46" fill="none" stroke="url(#orbRim)" strokeWidth="2" />

        {/* soft highlight */}
        <ellipse cx="42" cy="42" rx="14" ry="9" fill="#FFFFFF" opacity="0.35" />

        {/* face */}
        <g className="animate-blink" style={{ transformOrigin: "60px 60px" }}>
          <ellipse cx="47" cy="60" rx="3.5" ry="4.5" fill="#211C30" />
          <ellipse cx="73" cy="60" rx="3.5" ry="4.5" fill="#211C30" />
        </g>
        <path
          d="M50 74 Q60 81 70 74"
          stroke="#211C30"
          strokeWidth="3"
          fill="none"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
}
