/** Small inline SVG icon set (no icon font, no emoji). */
type P = { size?: number; className?: string };
const S = ({ size = 22, className, children }: P & { children: React.ReactNode }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden="true" fill="none"
    stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">{children}</svg>
);

export const Heart = ({ size = 26, className }: P) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden="true">
    <path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.8 4.5c2.1 0 3.6 1.2 5.2 3 1.6-1.8 3.1-3 5.2-3 3.8 0 5.9 3.9 4.4 7.3C19.5 16.4 12 21 12 21z" fill="currentColor" />
    <path d="M7 8.2c-.9.3-1.5 1.1-1.6 2" stroke="#fff" strokeOpacity=".55" strokeWidth="1.8" strokeLinecap="round" fill="none" />
  </svg>
);
export const Flame = ({ size = 24, className }: P) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden="true">
    <path d="M12 2.5c1 3.2 4.8 5.3 4.8 10.1A4.8 4.8 0 0 1 12 17.4a4.8 4.8 0 0 1-4.8-4.8c0-1.9.9-3.3 2-4.4.2 1.4.9 2.4 1.9 2.9-.4-3.1.5-6.2.9-8.6z" fill="currentColor" />
    <path d="M12 21.5a3.6 3.6 0 0 0 3.6-3.6c0-2.2-2.2-3.3-2.7-5.3-1.3 1.2-4.5 2.7-4.5 5.3a3.6 3.6 0 0 0 3.6 3.6z" fill="#ffd34d" />
  </svg>
);
export const Trophy = (p: P) => <S {...p}><path d="M8 4h8v5a4 4 0 0 1-8 0z" /><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8 21h8M9 17h6" /></S>;
export const Gear = (p: P) => <S {...p}><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" /></S>;
export const Dumbbell = (p: P) => <S {...p}><path d="M6 7v10M3 9v6M18 7v10M21 9v6M6 12h12" /></S>;
export const Close = (p: P) => <S {...p}><path d="M6 6l12 12M18 6L6 18" /></S>;
export const Bulb = (p: P) => <S {...p}><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2V16h5v-.1c0-.8.4-1.5 1-2A6 6 0 0 0 12 3z" /></S>;
export const Lifebuoy = (p: P) => <S {...p}><circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="3.5" /><path d="M5.6 5.6l4 4M14.4 14.4l4 4M18.4 5.6l-4 4M9.6 14.4l-4 4" /></S>;
export const Book = (p: P) => <S {...p}><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z" /><path d="M4 19V5M8 7h7" /></S>;
export const Check = (p: P) => <S {...p}><path d="M5 12.5l4.5 4.5L19 7.5" /></S>;
export const Lock = (p: P) => <S {...p}><rect x="5" y="10.5" width="14" height="10" rx="2.5" /><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" /></S>;
export const Star = ({ size = 22, className }: P) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden="true">
    <path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z" fill="currentColor" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round" />
  </svg>
);
export const Crown = ({ size = 26, className }: P) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden="true">
    <path d="M3 8l4.5 4L12 5l4.5 7L21 8l-2 11H5z" fill="currentColor" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round" />
    <circle cx="12" cy="15" r="1.6" fill="#fff" opacity=".8" />
  </svg>
);
export const Speaker = ({ on, ...p }: P & { on: boolean }) => <S {...p}><path d="M4 10v4h4l5 4V6L8 10z" />{on ? <path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12" /> : <path d="M17 9l5 6M22 9l-5 6" />}</S>;
export const Play = (p: P) => <S {...p}><path d="M7 5v14l11-7z" fill="currentColor" /></S>;
export const Arrow = (p: P) => <S {...p}><path d="M5 12h14M13 6l6 6-6 6" /></S>;
export const Back = (p: P) => <S {...p}><path d="M19 12H5M11 6l-6 6 6 6" /></S>;
export const Skip = (p: P) => <S {...p}><path d="M5 5l8 7-8 7M15 5v14" /></S>;

const BADGE_PATHS: Record<string, React.ReactNode> = {
  foot: <path d="M8 3c2 0 3 2 3 4.5S10 13 8 13s-3-3-3-5.5S6 3 8 3zM7 15.5h3l-.5 4.5h-2zM16 7c1.7 0 2.5 1.7 2.5 3.8S17.7 15 16 15s-2.5-2.1-2.5-4.2S14.3 7 16 7zM15 17h2.5l-.4 4h-1.7z" fill="currentColor" stroke="none" />,
  loop: <><path d="M17 3l3 3-3 3" /><path d="M4 11V9a3 3 0 0 1 3-3h13M7 21l-3-3 3-3" /><path d="M20 13v2a3 3 0 0 1-3 3H4" /></>,
  heart: <path d="M12 20s-7-4.3-9-8.6C1.6 8.2 3.6 5 7 5c2 0 3.4 1.1 5 2.8C13.6 6.1 15 5 17 5c3.4 0 5.4 3.2 4 6.4-2 4.3-9 8.6-9 8.6z" fill="currentColor" stroke="none" />,
  star: <path d="M12 3l2.7 5.6 6.1.8-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1-4.4-4.3 6.1-.8z" fill="currentColor" stroke="none" />,
  rise: <><path d="M3 17l6-6 4 4 8-8" /><path d="M15 7h6v6" /></>,
  bug: <><rect x="8" y="7" width="8" height="12" rx="4" /><path d="M12 7V4M8 11H4M8 15H4M16 11h4M16 15h4M9 4l1.5 2M15 4l-1.5 2" /></>,
  eye: <><path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z" /><circle cx="12" cy="12" r="3" /></>,
  brick: <><rect x="3" y="5" width="18" height="14" rx="1.5" /><path d="M3 12h18M9 5v7M15 12v7" /></>,
  dumbbell: <path d="M6 7v10M3 9v6M18 7v10M21 9v6M6 12h12" />,
  flame: <path d="M12 2.5c1 3.2 4.8 5.3 4.8 10.1a4.8 4.8 0 1 1-9.6 0c0-1.9.9-3.3 2-4.4.2 1.4.9 2.4 1.9 2.9-.4-3.1.5-6.2.9-8.6zM12 21a3.5 3.5 0 0 0 3.5-3.5" fill="currentColor" stroke="none" />,
  flag: <><path d="M5 21V4" /><path d="M5 4h11l-2 4 2 4H5" fill="currentColor" /></>,
  crown: <path d="M3 8l4.5 4L12 5l4.5 7L21 8l-2 11H5z" fill="currentColor" stroke="none" />,
  trophy: <><path d="M8 4h8v5a4 4 0 0 1-8 0z" fill="currentColor" /><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8 21h8M9 17h6" /></>,
};
export const Badge = ({ name, size = 30 }: { name: string; size?: number }) => <S size={size}>{BADGE_PATHS[name]}</S>;
