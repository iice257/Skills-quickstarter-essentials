import { Check, Clipboard, ClipboardList, X } from "lucide-react";
import { useState } from "react";
import type { SelectionItem } from "../types";

type MultiSelectFabProps = {
  active: boolean;
  selectedItems: SelectionItem[];
  onEnable: () => void;
  onCancel: () => void;
  onCopied: () => void;
};

export function MultiSelectFab({ active, selectedItems, onEnable, onCancel, onCopied }: MultiSelectFabProps) {
  const [copied, setCopied] = useState(false);
  const disabled = active && selectedItems.length === 0;

  function fallbackCopy(value: string) {
    const textArea = document.createElement("textarea");
    textArea.value = value;
    textArea.setAttribute("readonly", "");
    textArea.style.position = "fixed";
    textArea.style.left = "-9999px";
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);
  }

  async function copySelection() {
    const value = selectedItems.map((item) => `${item.title}\n${item.command}`).join("\n\n");

    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(value);
      } else {
        fallbackCopy(value);
      }
    } catch {
      fallbackCopy(value);
    }

    setCopied(true);
    onCopied();
    window.setTimeout(() => setCopied(false), 1800);
  }

  async function handleClick() {
    if (!active) {
      onEnable();
      return;
    }

    if (disabled) return;
    await copySelection();
  }

  return (
    <div className={`multi-select-actions ${active ? "active" : ""}`}>
      <button
        className="multi-select-fab"
        type="button"
        disabled={disabled}
        onClick={handleClick}
        aria-label={active ? "Copy selected commands" : "Enable multi-selection mode"}
        title={active ? "Copy selection" : "Multi-selection mode"}
      >
        {copied ? (
          <Check aria-hidden="true" />
        ) : active ? (
          <ClipboardList aria-hidden="true" />
        ) : (
          <Clipboard aria-hidden="true" />
        )}
        <span>{copied ? "Selection copied" : active ? "Copy selection" : "Multi-selection mode"}</span>
        {active ? <em>{selectedItems.length}</em> : null}
      </button>
      {active ? (
        <button
          className="multi-select-cancel"
          type="button"
          onClick={onCancel}
          aria-label="Cancel multi-selection mode"
          title="Cancel selection"
        >
          <X aria-hidden="true" />
        </button>
      ) : null}
    </div>
  );
}
