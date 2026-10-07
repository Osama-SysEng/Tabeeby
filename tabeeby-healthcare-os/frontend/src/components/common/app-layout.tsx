import React from 'react';
import { Sidebar } from './sidebar';
import { Header } from './header';
import { TierBadge } from './tier-badge';

interface AppLayoutProps { children: React.ReactNode; tier: number; user: any; }

export const AppLayout: React.FC<AppLayoutProps> = ({ children, tier, user }) => {
  return (
    <div className={`app-layout tier-${tier}`}>
      <Sidebar tier={tier} user={user} />
      <div className="main-area">
        <Header user={user} tier={tier} />
        <TierBadge tier={tier} />
        <main className="content">{children}</main>
      </div>
    </div>
  );
};