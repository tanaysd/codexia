import React, { createContext, useContext, useState } from 'react';

interface Toast {
  id: number;
  message: string;
}

const ToastContext = createContext<(msg: string) => void>(() => {});

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  function push(message: string) {
    setToasts((t) => [...t, { id: Date.now(), message }]);
    setTimeout(() => setToasts((t) => t.slice(1)), 3000);
  }

  return (
    <ToastContext.Provider value={push}>
      {children}
      <div className="fixed bottom-2 right-2 space-y-2">
        {toasts.map((t) => (
          <div key={t.id} className="bg-black text-white p-2 rounded">
            {t.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  return useContext(ToastContext);
}
