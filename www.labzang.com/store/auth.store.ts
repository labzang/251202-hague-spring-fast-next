/**
 * 인증 상태 관리 스토어 (Zustand + Ducks 패턴)
 * Access Token은 메모리에만 저장
 * Refresh Token은 httpOnly 쿠키에 저장되므로 이 스토어에서는 관리하지 않음
 */

'use client';

import { useContext } from 'react';
import { createStore, useStore as useZustandStore } from 'zustand';
import { AuthStoreContext } from './auth.provider';

// ============================================
// Types (Ducks 패턴: 타입 정의)
// ============================================

interface AuthState {
    accessToken: string | null;
}

interface AuthActions {
    setAccessToken: (token: string | null) => void;
    getAccessToken: () => string | null;
    clearAccessToken: () => void;
    isAuthenticated: () => boolean;
}

export type AuthStore = AuthState & AuthActions;

// ============================================
// Store Creator (Ducks 패턴: 스토어 생성 함수)
// ============================================

export const createAuthStore = () => {
    return createStore<AuthStore>((set, get) => ({
        // State
        accessToken: null,

        // Actions
        setAccessToken: (token) => {
            set({ accessToken: token });
        },

        getAccessToken: () => {
            return get().accessToken;
        },

        clearAccessToken: () => {
            set({ accessToken: null });
        },

        isAuthenticated: () => {
            return get().accessToken !== null;
        },
    }));
};

// ============================================
// Store API Type (Provider에서 사용)
// ============================================

export type AuthStoreApi = ReturnType<typeof createAuthStore>;

// ============================================
// Custom Hook (Ducks 패턴: 셀렉터 훅)
// ============================================

export function useAuthStore<T>(selector: (state: AuthStore) => T): T {
    const store = useContext(AuthStoreContext);

    if (!store) {
        throw new Error('useAuthStore must be used within AuthStoreProvider');
    }

    return useZustandStore(store, selector);
}

// ============================================
// Selectors (Ducks 패턴: 자주 사용하는 셀렉터)
// ============================================

export const selectAccessToken = (state: AuthStore) => state.accessToken;
export const selectIsAuthenticated = (state: AuthStore) => state.isAuthenticated();
export const selectSetAccessToken = (state: AuthStore) => state.setAccessToken;
export const selectClearAccessToken = (state: AuthStore) => state.clearAccessToken;

