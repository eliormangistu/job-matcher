"use client";

import { useEffect } from "react";

import { handleEscape } from "@/utils/accessibility";

import { ModalProps } from "@/types/modal";

import "@/styles/components/ui/_modal.scss";

export default function Modal({
  isOpen,
  title,
  message,
  children,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  onConfirm,
  onCancel,
}: ModalProps) {
  useEffect(() => {
    if (!isOpen) {
      return;
    }

    function handleKeyDown(event: KeyboardEvent) {
      handleEscape(event, onCancel);
    }

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, onCancel]);

  if (!isOpen) {
    return null;
  }

  return (
    <div
      className="modal-overlay"
      role="presentation"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) {
          onCancel();
        }
      }}
    >
      <section
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <h2 id="modal-title">{title}</h2>

        {message && <p>{message}</p>}

        {children}

        <div className="modal-actions">
          <button
            type="button"
            className="modal-cancel-button"
            onClick={onCancel}
          >
            {cancelLabel}
          </button>

          {onConfirm && (
            <button
              type="button"
              className="modal-confirm-button"
              onClick={onConfirm}
            >
              {confirmLabel}
            </button>
          )}
        </div>
      </section>
    </div>
  );
}
