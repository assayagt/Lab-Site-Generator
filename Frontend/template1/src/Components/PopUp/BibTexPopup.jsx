import React, { useState } from "react";
import "./BibTexPopup.css"; // You'll need to create this CSS file

const BibTexPopup = ({ bibtex, onClose }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(bibtex);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  return (
    <div className="bibtex-modal-overlay" onClick={onClose}>
      <div
        className="bibtex-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="bibtex-modal-header">
          <h3>BibTeX Citation</h3>
          <button className="bibtex-close-button" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="bibtex-content">
          <pre>{bibtex}</pre>
        </div>
        <div className="bibtex-modal-footer">
          <button
            className={`bibtex-copy-button ${copied ? "copied" : ""}`}
            onClick={handleCopy}
          >
            {copied ? "Copied!" : "Copy to Clipboard"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default BibTexPopup;
