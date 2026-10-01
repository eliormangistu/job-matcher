import { RefObject } from "react";

export interface DesktopNavProps {
  header: {
    home: string;
    jobs: string;
    cvMatcher: string;
  };
  isUserMenuOpen: boolean;
  setIsUserMenuOpen: (value: boolean) => void;
  isAuthenticated: boolean;
  authLoading: boolean;
  user: {
    email?: string | null;
  } | null;
  onLogout: () => Promise<void>;
  userMenuRef: RefObject<HTMLDivElement | null>;
}

export interface MobileNavProps {
  header: {
    home: string;
    jobs: string;
    cvMatcher: string;
  };
  isOpen: boolean;
  setIsOpen: (value: boolean) => void;
  isAuthenticated: boolean;
  authLoading: boolean;
  onLogout: () => Promise<void>;
  menuRef: RefObject<HTMLDivElement | null>;
}
