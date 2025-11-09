import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen">

      <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-slate-900/80 border-b border-slate-800/50 shadow-lg shadow-black/10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex justify-between items-center h-20">

            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 via-purple-600 to-cyan-600 flex items-center justify-center shadow-lg shadow-blue-600/30">
                <span className="text-white font-black text-2xl">N</span>
              </div>
              <div>
                <h1 className="text-2xl font-extrabold bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                  Nexus Data Hub
                </h1>
                <p className="text-xs text-slate-400 font-medium">
                  Plataforma de Integração de APIs
                </p>
              </div>
            </div>
            

            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-full bg-green-500/10 border border-green-500/30">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
                </span>
                <span className="text-green-400 text-sm font-semibold">Online</span>
              </div>
              
              <span className="hidden md:block text-slate-500 text-sm font-medium">
                6 APIs Ativas
              </span>
            </div>
          </div>
        </div>
      </header>
      

      <main className="pt-20">
        {children}
      </main>
    </div>
  );
};

export default Layout;
