# Tabeeby — Animation Implementation Plan

## Overview
This document outlines the animation strategy for Tabeeby dashboards.

## Animation Categories

### 1. **Loading Animations**
- Pulse glow effects for live data indicators
- Shimmer effects for loading states
- Slide-up animations for cards entering viewport

### 2. **Data Display Animations**
- Heartbeat animation for vital signs
- Progress bar transitions (0.5s ease)
- Count-up animations for statistics
- Shimmer gradient for vital value underlines

### 3. **AI Chat Animations**
- Slide-in-right message entrance
- Typing indicator with 3-dot blink sequence
- Message time stamps fade-in

### 4. **Interactive Animations**
- Card hover: scale(1.02) + shadow lift
- Button hover: scale(1.02) + color shift
- Emergency button: float 3s infinite animation
- Critical alerts: continuous pulse glow

### 5. **Timeline Animations**
- Timeline dots with pulse glow
- Connecting line gradient fade
- Staggered card entrance (0.1s delay per item)

### 6. **Special Effects**
- Floating particles for molecular simulation
- Glowing borders for critical items (spinning gradient)
- Success pop animation (scale bounce)
- Error shake animation

## Implementation Notes
- All animations respect `prefers-reduced-motion`
- Animation delays staggered per card index
- CSS custom properties for easy theming
- Hardware acceleration via transform/opacity only
- Fallback states defined for all animated elements

## Performance
- Animations use transform and opacity only (GPU-accelerated)
- No layout-triggering properties animated
- Animation duration: 0.2-0.5s for micro-interactions
- 1.5-3s for ambient/continuous animations
- Infinite loops: 1.5-3s for ambient, 1s for pulses
