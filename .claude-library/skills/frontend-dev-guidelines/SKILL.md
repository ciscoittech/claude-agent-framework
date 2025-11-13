# Frontend Development Guidelines

## Overview

This skill provides best practices, patterns, and guidelines for frontend development in this project. Use it when working with UI components, state management, styling, or user interactions.

**When to use**: Building components, implementing UI features, working with state, styling interfaces, handling user interactions.

## Core Principles

### 1. Component Structure
- **Functional components**: Always use function components, not classes
- **Single responsibility**: One component, one purpose
- **Composition over inheritance**: Build complex UIs from simple components
- **Props typing**: Every prop must be typed (TypeScript)

### 2. State Management
- **Local first**: Use `useState` for component-local state
- **Context for shared**: Use Context API for cross-component state
- **External for global**: Use external state library (Redux, Zustand) for global app state
- **No prop drilling**: If passing props >2 levels, use Context or external state

### 3. Performance
- **Memoization**: Use `React.memo()` for expensive components
- **Callbacks**: Use `useCallback()` for functions passed as props
- **Values**: Use `useMemo()` for expensive computations
- **Keys**: Always provide stable keys in lists

### 4. Error Handling
- **Error boundaries**: Wrap features in error boundaries
- **Try-catch**: Wrap async operations in try-catch
- **Loading states**: Always show loading UI during async operations
- **Error states**: Always show error UI when operations fail

## Quick Patterns

### Component Template
```typescript
import { FC } from 'react';

interface ComponentNameProps {
  prop1: string;
  prop2?: number;
}

export const ComponentName: FC<ComponentNameProps> = ({ prop1, prop2 = 0 }) => {
  // Hooks at top
  // Event handlers
  // Render logic

  return (
    <div>
      {/* JSX */}
    </div>
  );
};
```

### Custom Hook Template
```typescript
import { useState, useEffect } from 'react';

export function useCustomHook(param: string) {
  const [state, setState] = useState<Type>(initialValue);

  useEffect(() => {
    // Side effect
    return () => {
      // Cleanup
    };
  }, [dependencies]);

  return { state, helper functions };
}
```

### Async Data Fetching
```typescript
const [data, setData] = useState<Type | null>(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<Error | null>(null);

useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await api.getData();
      setData(response);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  fetchData();
}, [dependencies]);

if (loading) return <LoadingSpinner />;
if (error) return <ErrorMessage error={error} />;
if (!data) return null;

return <DataDisplay data={data} />;
```

## Project-Specific Patterns

### File Structure
```
src/
├── components/
│   ├── ui/           # Reusable UI components
│   ├── features/     # Feature-specific components
│   └── layouts/      # Layout components
├── hooks/            # Custom hooks
├── contexts/         # React contexts
├── utils/            # Utility functions
├── types/            # TypeScript types
└── styles/           # Global styles
```

### Naming Conventions
- **Components**: PascalCase (`UserProfile.tsx`)
- **Hooks**: camelCase with `use` prefix (`useUserData.ts`)
- **Utils**: camelCase (`formatDate.ts`)
- **Constants**: SCREAMING_SNAKE_CASE (`API_BASE_URL`)
- **Props interfaces**: ComponentName + `Props` (`UserProfileProps`)

### Import Order
```typescript
// 1. External libraries
import { FC, useState } from 'react';
import { Link } from 'react-router-dom';

// 2. Internal utilities
import { formatDate } from '@/utils/date';
import { useAuth } from '@/hooks/useAuth';

// 3. Components
import { Button } from '@/components/ui/Button';

// 4. Types
import { User } from '@/types/user';

// 5. Styles
import './styles.css';
```

## Common Anti-Patterns

### ❌ DON'T: Mutate state directly
```typescript
// Wrong
user.name = 'New Name';
setUser(user);
```

### ✅ DO: Create new objects
```typescript
// Right
setUser({ ...user, name: 'New Name' });
```

### ❌ DON'T: Forget cleanup
```typescript
// Wrong
useEffect(() => {
  const interval = setInterval(() => {}, 1000);
}, []);
```

### ✅ DO: Clean up side effects
```typescript
// Right
useEffect(() => {
  const interval = setInterval(() => {}, 1000);
  return () => clearInterval(interval);
}, []);
```

### ❌ DON'T: Use indexes as keys
```typescript
// Wrong
{items.map((item, index) => (
  <div key={index}>{item.name}</div>
))}
```

### ✅ DO: Use stable unique identifiers
```typescript
// Right
{items.map((item) => (
  <div key={item.id}>{item.name}</div>
))}
```

## Testing Guidelines

### Component Tests
- Test user interactions, not implementation
- Use `@testing-library/react`
- Query by accessible roles and labels
- Mock external dependencies

### Example Test
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Button', () => {
  it('calls onClick when clicked', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    await userEvent.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## Accessibility

### Required Practices
- **Semantic HTML**: Use `<button>`, `<nav>`, `<article>`, etc.
- **Alt text**: All images must have alt attributes
- **ARIA labels**: Add labels for icon-only buttons
- **Keyboard navigation**: All interactive elements accessible via keyboard
- **Focus management**: Visible focus indicators, logical focus order

### Example
```typescript
// Good accessibility
<button aria-label="Close dialog" onClick={onClose}>
  <CloseIcon />
</button>

<img src={src} alt="User profile photo" />

<nav aria-label="Main navigation">
  {/* Navigation items */}
</nav>
```

## Performance Optimization

### When to Optimize
- Component renders >10 times per second
- List has >100 items
- Computation takes >50ms
- User experiences lag

### How to Optimize
1. **Profile first**: Use React DevTools Profiler
2. **Identify bottleneck**: Find slow component
3. **Apply technique**:
   - `React.memo()` for pure components
   - `useCallback()` for stable function identity
   - `useMemo()` for expensive calculations
   - Virtualization for long lists
4. **Measure impact**: Verify improvement

## Resources

For deeper dives into specific topics, see:
- `resources/react-patterns.md` - Advanced React patterns
- `resources/state-management.md` - State management strategies
- `resources/performance.md` - Performance optimization guide
- `resources/styling.md` - Styling approaches and conventions
- `resources/testing.md` - Comprehensive testing guide

## When NOT to Use This Skill

This skill is for **frontend/UI development**. For other domains:
- **Backend/API**: Use `backend-dev-guidelines` skill
- **Database**: Use `database-specialist` skill
- **Testing**: Use `testing-specialist` skill
- **DevOps**: Use appropriate infrastructure skill

## Quick Reference

**Component**: Functional, typed props, hooks at top
**State**: Local → Context → Global store
**Performance**: Profile first, optimize bottlenecks
**Errors**: Boundaries, try-catch, loading/error states
**Accessibility**: Semantic HTML, ARIA, keyboard nav
**Testing**: User interactions, accessible queries

---

*This skill follows Anthropic's progressive disclosure best practices: <500 lines main file, detailed resources linked.*
