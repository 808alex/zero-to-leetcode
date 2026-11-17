import { useEffect, useRef } from "react";
import { EditorView, keymap, lineNumbers, highlightActiveLine, drawSelection } from "@codemirror/view";
import { EditorState } from "@codemirror/state";
import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { HighlightStyle, syntaxHighlighting, indentOnInput, bracketMatching, indentUnit } from "@codemirror/language";
import { closeBrackets, closeBracketsKeymap } from "@codemirror/autocomplete";
import { tags as t } from "@lezer/highlight";

const highlight = HighlightStyle.define([
  { tag: [t.keyword, t.controlKeyword, t.operatorKeyword, t.definitionKeyword, t.moduleKeyword], color: "var(--tk-key)" },
  { tag: [t.string, t.special(t.string)], color: "var(--tk-str)" },
  { tag: [t.number, t.bool, t.null], color: "var(--tk-num)" },
  { tag: [t.comment, t.lineComment], color: "var(--tk-com)", fontStyle: "italic" },
  { tag: [t.function(t.variableName), t.function(t.propertyName), t.className], color: "var(--tk-fn)" },
  { tag: [t.definition(t.variableName)], color: "var(--ink)" },
  { tag: [t.operator, t.punctuation, t.bracket], color: "var(--muted)" },
]);

const theme = EditorView.theme({
  "&": { backgroundColor: "var(--code-bg)", color: "var(--ink)", borderRadius: "14px", fontSize: "14.5px" },
  ".cm-content": { fontFamily: "var(--font-mono)", padding: "12px 0", caretColor: "var(--primary)" },
  ".cm-gutters": { backgroundColor: "transparent", border: "none", color: "var(--muted)", opacity: "0.6" },
  ".cm-activeLine": { backgroundColor: "color-mix(in srgb, var(--primary) 7%, transparent)" },
  ".cm-activeLineGutter": { backgroundColor: "transparent", color: "var(--ink)" },
  "&.cm-focused": { outline: "none" },
  ".cm-selectionBackground, &.cm-focused .cm-selectionBackground, ::selection": { backgroundColor: "color-mix(in srgb, var(--primary) 28%, transparent) !important" },
  ".cm-cursor": { borderLeftColor: "var(--primary)", borderLeftWidth: "2px" },
  ".cm-scroller": { fontFamily: "var(--font-mono)", lineHeight: "1.6" },
});

type Props = { value: string; onChange: (v: string) => void; onRun?: () => void; ariaLabel: string };

export function CodeEditor({ value, onChange, onRun, ariaLabel }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const view = useRef<EditorView | null>(null);
  const runRef = useRef(onRun);
  runRef.current = onRun;
  const changeRef = useRef(onChange);
  changeRef.current = onChange;

  useEffect(() => {
    const state = EditorState.create({
      doc: value,
      extensions: [
        lineNumbers(), history(), drawSelection(), highlightActiveLine(), indentOnInput(), bracketMatching(), closeBrackets(),
        indentUnit.of("    "), EditorState.tabSize.of(4), python(), syntaxHighlighting(highlight), theme,
        keymap.of([
          { key: "Mod-Enter", run: () => { runRef.current?.(); return true; } },
          ...closeBracketsKeymap, ...defaultKeymap, ...historyKeymap, indentWithTab,
        ]),
        EditorView.updateListener.of((u) => { if (u.docChanged) changeRef.current(u.state.doc.toString()); }),
        EditorView.contentAttributes.of({ "aria-label": ariaLabel, spellcheck: "false", autocapitalize: "off", autocorrect: "off" }),
      ],
    });
    view.current = new EditorView({ state, parent: host.current! });
    return () => view.current?.destroy();
    // the editor owns its document after mount
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // allow the parent to reset the content (e.g. "Reset code")
  useEffect(() => {
    const v = view.current;
    if (v && v.state.doc.toString() !== value) v.dispatch({ changes: { from: 0, to: v.state.doc.length, insert: value } });
  }, [value]);

  return <div className="editor" ref={host} />;
}
