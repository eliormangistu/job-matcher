export function getFocusableElements(container: HTMLElement): HTMLElement[] {
  return Array.from(
    container.querySelectorAll<HTMLElement>(
      'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
    ),
  );
}

export function trapFocus(event: KeyboardEvent, container: HTMLElement): void {
  if (event.key !== "Tab") {
    return;
  }

  const focusableElements = getFocusableElements(container);

  if (focusableElements.length === 0) {
    event.preventDefault();
    return;
  }

  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  if (event.shiftKey && document.activeElement === firstElement) {
    event.preventDefault();
    lastElement.focus();
    return;
  }

  if (!event.shiftKey && document.activeElement === lastElement) {
    event.preventDefault();
    firstElement.focus();
  }
}

export function handleEscape(event: KeyboardEvent, onClose: () => void): void {
  if (event.key === "Escape") {
    event.preventDefault();
    onClose();
  }
}

export function handleDialogKeyDown(
  event: KeyboardEvent,
  container: HTMLElement,
  onClose: () => void,
): void {
  handleEscape(event, onClose);
  trapFocus(event, container);
}
