/**
 * "Ask Claude" for the helper. Only available when the app is opened inside Claude as an artifact
 * (window.claude provides the sample capability). On GitHub Pages this resolves to null and the
 * button never appears.
 */
type Sampler = ((input: string, opts?: any) => Promise<{ text: string }>) | null;
let samplerP: Promise<Sampler> | null = null;

export function getSampler(): Promise<Sampler> {
  if (!samplerP) {
    const claude = (window as any).claude;
    samplerP = claude && typeof claude.use === "function"
      ? claude.use("sample").catch(() => null)
      : Promise.resolve(null);
  }
  return samplerP!;
}

const COACH =
  "You are Pip, a friendly but honest Python coach inside a learning game. The learner is relearning Python to get ready for LeetCode. " +
  "Use simple language and markdown. Never give the full solution. Point at the specific mistake, then give one nudge toward fixing it. Under 120 words.";

export async function askClaude(problem: string, code: string, results: string, onText: (t: string) => void): Promise<string> {
  const sample = await getSampler();
  if (!sample) throw new Error("unavailable");
  const prompt = `${COACH}\n\nQuestion: ${problem}\n\nTheir code:\n\`\`\`python\n${code}\n\`\`\`\n\nLatest test results:\n${results || "(not run yet)"}`;
  const res = await sample(prompt, { cache: false, onText: ({ text }: { text: string }) => text && onText(text) });
  return res.text || "";
}

/** Minimal, safe markdown for Claude's replies. */
export function miniMarkdown(text: string): string {
  const esc = (s: string) => s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]!));
  return text.split(/```(?:\w+)?\n?/).map((chunk, i) => {
    if (i % 2) return `<pre><code>${esc(chunk.replace(/\n$/, ""))}</code></pre>`;
    return chunk.split(/\n{2,}/).map((para) => {
      const lines = para.split("\n").filter((l) => l.trim());
      if (!lines.length) return "";
      const inline = (s: string) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
      if (lines.every((l) => /^\s*([-*]|\d+\.)\s/.test(l))) return "<ul>" + lines.map((l) => `<li>${inline(l.replace(/^\s*([-*]|\d+\.)\s/, ""))}</li>`).join("") + "</ul>";
      return `<p>${lines.map(inline).join("<br>")}</p>`;
    }).join("");
  }).join("");
}
