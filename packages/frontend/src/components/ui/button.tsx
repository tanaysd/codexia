import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost';
  size?: 'default' | 'sm' | 'lg';
  children: React.ReactNode;
}

export function Button({ 
  variant = 'default', 
  size = 'default', 
  className = '', 
  children, 
  ...props 
}: ButtonProps) {
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50';
  
  const variants = {
    default: 'bg-slate-900 text-white hover:bg-slate-800 focus-visible:ring-slate-950',
    outline: 'border border-slate-200 bg-white hover:bg-slate-50 hover:text-slate-900 focus-visible:ring-slate-950',
    ghost: 'hover:bg-slate-100 hover:text-slate-900 focus-visible:ring-slate-950'
  };
  
  const sizes = {
    default: 'h-10 px-4 py-2',
    sm: 'h-8 rounded-md px-3 text-sm',
    lg: 'h-11 rounded-md px-8'
  };
  
  return (
    <button
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}