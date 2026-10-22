"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { User } from "@/lib/types";
import { 
  loginUser, 
  registerUser, 
  fetchCurrentUser, 
  rechargeCredits 
} from "@/lib/api";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  recharge: (amount?: number) => Promise<number>;
  refreshUser: () => Promise<void>;
  deductLocalCredits: (amount: number) => void;
  isAuthModalOpen: boolean;
  authModalMode: "login" | "signup";
  openAuthModal: (mode?: "login" | "signup") => void;
  closeAuthModal: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_STORAGE_KEY = "chalkka_user_token";
const USER_STORAGE_KEY = "chalkka_user_profile";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authModalMode, setAuthModalMode] = useState<"login" | "signup">("login");

  // Load stored session on initial mount
  useEffect(() => {
    try {
      const storedToken = localStorage.getItem(TOKEN_STORAGE_KEY);
      const storedUser = localStorage.getItem(USER_STORAGE_KEY);

      if (storedToken && storedUser) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
        
        // Refresh profile in background to get latest credit balance
        fetchCurrentUser(storedToken)
          .then((res) => {
            setUser(res.user);
            localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(res.user));
          })
          .catch((err) => {
            console.warn("Session expired or unreachable:", err);
            // If invalid token, clear
            if (err?.message?.includes("expired") || err?.message?.includes("invalid")) {
              localStorage.removeItem(TOKEN_STORAGE_KEY);
              localStorage.removeItem(USER_STORAGE_KEY);
              setToken(null);
              setUser(null);
            }
          });
      }
    } catch (e) {
      console.error("Failed to load auth session from localStorage:", e);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await loginUser({ email, password });
      setToken(res.token);
      setUser(res.user);
      localStorage.setItem(TOKEN_STORAGE_KEY, res.token);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(res.user));
      setIsAuthModalOpen(false);
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (email: string, password: string, name: string) => {
    setIsLoading(true);
    try {
      const res = await registerUser({ email, password, name });
      setToken(res.token);
      setUser(res.user);
      localStorage.setItem(TOKEN_STORAGE_KEY, res.token);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(res.user));
      setIsAuthModalOpen(false);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
  };

  const recharge = async (amount: number = 25): Promise<number> => {
    if (!token) throw new Error("Must be logged in to recharge credits.");
    const res = await rechargeCredits(token, amount);
    if (user) {
      const updatedUser = { ...user, credits: res.credits };
      setUser(updatedUser);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(updatedUser));
    }
    return res.credits;
  };

  const refreshUser = async () => {
    if (!token) return;
    try {
      const res = await fetchCurrentUser(token);
      setUser(res.user);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(res.user));
    } catch (err) {
      console.warn("Failed to refresh user:", err);
    }
  };

  const deductLocalCredits = (amount: number) => {
    if (user) {
      const updatedUser = { ...user, credits: Math.max(0, user.credits - amount) };
      setUser(updatedUser);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(updatedUser));
    }
  };

  const openAuthModal = (mode: "login" | "signup" = "login") => {
    setAuthModalMode(mode);
    setIsAuthModalOpen(true);
  };

  const closeAuthModal = () => {
    setIsAuthModalOpen(false);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        signup,
        logout,
        recharge,
        refreshUser,
        deductLocalCredits,
        isAuthModalOpen,
        authModalMode,
        openAuthModal,
        closeAuthModal,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
