# Styles Directory

This directory contains organized CSS files following best practices for maintainability and scalability.

## Structure

### `variables.css`
Contains all CSS custom properties (variables) for Honeywell's brand colors, typography, and design tokens. These variables are used throughout the application to maintain brand consistency.

**Key Variables:**
- Honeywell brand colors (orange, blue, red, gray)
- Semantic color mappings (primary, secondary, success, info, warning, danger)
- Responsive breakpoints
- Typography font families

### `tailwind-theme.css`
Extends TailwindCSS v4's theme system with Honeywell brand colors and design tokens using CSS custom properties. This file maps CSS variables to Tailwind's theme system.

### `base.css`
Global base styles and resets that apply to the entire application, including body styles and box-sizing rules.

### `animations.css`
Reusable animation keyframes and utility classes for consistent animations throughout the application.

## Usage

All styles are imported through `app/globals.css` in the following order:
1. TailwindCSS
2. Variables
3. Tailwind Theme
4. Base Styles
5. Animations

## Honeywell Brand Colors

- **Primary Orange**: `#FF6A13` (`--honeywell-orange`)
- **Primary Blue**: `#0046ad` (`--honeywell-blue`)
- **Red**: `#E1251B` (`--honeywell-red`)
- **Gray**: `#939598` (`--honeywell-gray`)

## TailwindCSS Usage

You can use Honeywell brand colors in Tailwind classes:
- `bg-honeywell-orange` - Background with Honeywell orange
- `text-honeywell-blue` - Text with Honeywell blue
- `border-honeywell-gray` - Border with Honeywell gray

Or use semantic colors:
- `bg-primary` - Primary brand color (orange)
- `text-info` - Info color (blue)
- `bg-danger` - Danger color (red)

## Fonts

The application uses Honeywell's recommended font stack:
- Primary: System fonts (San Francisco, Segoe UI, Roboto, Helvetica Neue, Arial)
- Monospace: SFMono-Regular, Menlo, Monaco, Consolas

