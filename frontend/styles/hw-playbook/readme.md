# Honeywell Style Playbook

A tiny design system for Honeywell-aligned styling in the HoneyGo application. This playbook provides reusable design tokens and component classes that ensure consistent, brand-aligned visuals across the project.

## Structure

This playbook consists of three layers:

1. **`design-tokens.css`** - Raw CSS variables (colors, typography, spacing, breakpoints)
2. **`components.css`** - Reusable component classes built on top of tokens
3. **`readme.md`** - This documentation file

## Design Tokens

### Colors

- `--hw-color-bg-dark`: Dark background color (`#000000`)
- `--hw-color-text-on-dark`: Text color for dark backgrounds (`#ffffff`)
- `--hw-color-overlay`: Overlay color (`#000000`)

**Usage:**
```css
.my-component {
  background-color: var(--hw-color-bg-dark);
  color: var(--hw-color-text-on-dark);
}
```

### Typography

#### Font Weights
- `--hw-font-weight-bold`: 700
- `--hw-font-weight-black`: 900

#### Hero Title
- Small screens: `--hw-hero-title-size-sm` (32px) / `--hw-hero-title-line-sm` (35px)
- Medium+ screens: `--hw-hero-title-size-md` (50px) / `--hw-hero-title-line-md` (54px)

#### Hero Description
- Small screens: `--hw-hero-desc-size-sm` (14px) / `--hw-hero-desc-line-sm` (16px)
- Medium+ screens: `--hw-hero-desc-size-md` (22px) / `--hw-hero-desc-line-md` (26px)

### Layout / Spacing

- `--hw-left-rail-padding-x-desktop`: 50px (desktop padding)
- `--hw-left-rail-padding-x-tablet`: 35px (tablet padding)

### Breakpoints

- `--hw-break-sm`: 480px
- `--hw-break-md`: 768px
- `--hw-break-lg`: 900px
- `--hw-break-xl`: 992px

## Component Classes

### `.hw-hero`

Hero section component with dark background and gradient overlay.

**Usage:**
```tsx
<section className="hw-hero bg-black">
  <h1 className="hw-hero-title">HoneyGo</h1>
  <p className="hw-hero-desc">AI-Powered Pricing Platform</p>
</section>
```

**Features:**
- Dark background with text-on-dark color
- Gradient overlay (270deg, transparent to black)
- Responsive min-height (576px on medium+ screens)

### `.hw-hero-title`

Hero title styling with uppercase text transformation.

**Usage:**
```tsx
<h1 className="hw-hero-title">HoneyGo</h1>
```

**Features:**
- Black font weight (900)
- Uppercase text transformation
- Responsive sizing (32px → 50px)
- Relative positioning for z-index control

### `.hw-hero-desc`

Hero description text styling.

**Usage:**
```tsx
<p className="hw-hero-desc">AI-Powered Pricing Platform</p>
```

**Features:**
- Bold font weight (700)
- Responsive sizing (14px → 22px)
- Relative positioning for z-index control

### `.hw-left-rail`

Left rail component with responsive horizontal padding.

**Usage:**
```tsx
<div className="hw-left-rail">
  {/* Content */}
</div>
```

**Features:**
- Desktop: 50px horizontal padding
- Tablet and below: 35px horizontal padding (at 992px breakpoint)

## Integration with Tailwind

The design tokens are also mapped into Tailwind's theme system, allowing you to use utilities for finer control:

```tsx
<header className="hw-hero bg-hw-dark">
  <div className="max-w-7xl mx-auto px-6 py-8">
    <h1 className="hw-hero-title">HoneyGo</h1>
    <p className="hw-hero-desc text-hw-onDark">AI-Powered Pricing</p>
  </div>
</header>
```

### Available Tailwind Utilities

- Colors: `bg-hw-dark`, `text-hw-onDark`
- Screens: `hwsm:`, `hwmd:`, `hwlg:`, `hwxl:`

## Best Practices

1. **Use component classes for common patterns**: Prefer `.hw-hero`, `.hw-hero-title`, etc. for consistent styling
2. **Use tokens for custom components**: When building new components, reference design tokens directly
3. **Mix with Tailwind utilities**: Combine HW classes with Tailwind utilities for layout and spacing
4. **Maintain consistency**: Always use HW tokens/classes when Honeywell branding is required

## Example: Complete Hero Section

```tsx
<section className="hw-hero bg-black">
  <div className="hw-left-rail max-w-7xl mx-auto py-12">
    <h1 className="hw-hero-title">HoneyGo</h1>
    <p className="hw-hero-desc">AI-Powered Pricing Platform</p>
    <p className="text-gray-400 mt-4">
      Powered by Honeywell AI
    </p>
  </div>
</section>
```

## When to Use

- **Use HW classes** when you need Honeywell-branded components (hero sections, branded headers, etc.)
- **Use HW tokens** when building custom components that need to align with Honeywell design
- **Use Tailwind utilities** for layout, spacing, and non-branded styling
- **Mix both** for maximum flexibility while maintaining brand consistency

