"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import { getCurrentUser } from "@/api/user";
import { User } from "@/types/user";
import { logout as logoutApi } from "@/api/auth";
import { AuthContextValue, AuthProviderProps } from "@/types/auth";
import { googleLogout } from "@react-oauth/google";

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const response = await getCurrentUser();
        setUser(response.data.user);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  const refreshUser = async () => {
    try {
      const response = await getCurrentUser();
      setUser(response.data.user);
    } catch {
      setUser(null);
    }
  };

  const logout = async () => {
    try {
      await logoutApi();
    } finally {
      googleLogout();

      localStorage.clear();
      sessionStorage.clear();

      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: user !== null,
        loading,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
}
