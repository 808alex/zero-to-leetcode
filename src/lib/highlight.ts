import Prism from "prismjs";
import "prismjs/components/prism-python";

export const escapeHtml = (s: string) =>
  s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));

export const highlightPy = (code: string) => Prism.highlight(code, Prism.languages.python, "python");

/** Highlight every <pre><code> inside an element (used for lesson HTML). */
export function highlightWithin(el: HTMLElement) {
  el.querySelectorAll("pre code").forEach((node) => {
    const c = node as HTMLElement;
    if (c.dataset.hl) return;
    c.innerHTML = highlightPy(c.textContent || "");
    c.dataset.hl = "1";
  });
}
