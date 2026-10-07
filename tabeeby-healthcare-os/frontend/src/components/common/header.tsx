import React from 'react';
import { Logout } from '../icons';
export const Header = ({ userName, tier }: { userName: string; tier: number }) => (
  <header className="app-header">
    <div className="header-left"><h1>Tabeeby AI Healthcare OS</h1><span className="tier-badge">Tier {tier}</span></div>
    <div className="header-right"><span className="user-name">{userName}</span><Logout /></div>
  </header>
);
