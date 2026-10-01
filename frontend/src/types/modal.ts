import { ReactNode } from "react";

export interface ModalProps {
  isOpen: boolean;
  title: string;
  message?: string;
  children?: ReactNode;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm?: () => void | Promise<void>;
  onCancel: () => void;
}
