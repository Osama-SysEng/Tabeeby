import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { TierBadge } from './TierBadge';

interface Props { children: React.ReactNode; tier: number; userName: string; }
export const AppLayout = ({ children, tier, userName }: Props) => (
  <div className={`app-layout tier-${tier}`}>
    <Sidebar tier={tier} userName={userName} />
    <div className="main-content">
      <Header userName={userName} tier={tier} />
      <TierBadge tier={tier} />
      <main className="page-content">{children}</main>
    </div>
  </div>
);
