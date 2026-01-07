/**
 * 인증 스토어 Provider 컴포넌트
 * Next.js App Router용 클라이언트 컴포넌트
 */

'use client';

import { createContext, useRef, type ReactNode } from 'react';
import { createAuthStore, type AuthStoreApi } from './auth.store';

// ============================================
// Context
// ============================================

export const AuthStoreContext = createContext<AuthStoreApi | undefined>(undefined);

// ============================================
// Provider Props
// ============================================

export interface AuthStoreProviderProps {
  children: ReactNode;
}

// ============================================
// Provider Component
// ============================================

export function AuthStoreProvider({ children }: AuthStoreProviderProps) {
  const storeRef = useRef<AuthStoreApi | null>(null);

  if (!storeRef.current) {
    storeRef.current = createAuthStore();
  }

  return (
    <AuthStoreContext.Provider value={storeRef.current}>
      {children}
    </AuthStoreContext.Provider>
  );
}

