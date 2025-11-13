# Backend Development Guidelines

## Overview

This skill provides best practices, patterns, and guidelines for backend development in this project. Use it when working with APIs, services, databases, or server-side logic.

**When to use**: Creating endpoints, implementing business logic, database operations, authentication, middleware, error handling.

## Core Principles

### 1. Architecture Layers
- **Routes**: HTTP endpoint definitions, minimal logic
- **Controllers**: Request/response handling, validation
- **Services**: Business logic, orchestration
- **Repositories**: Database access, data mapping
- **Models**: Data structures and validation

**Flow**: Route → Controller → Service → Repository → Database

### 2. Error Handling
- **Try-catch all async**: Every async function wrapped in try-catch
- **Centralized errors**: Use error handler middleware
- **Typed errors**: Create error classes for different types
- **Log everything**: All errors logged with context
- **Don't expose internals**: Safe error messages to clients

### 3. Security
- **Validate input**: All user input validated
- **Sanitize data**: Prevent injection attacks
- **Authenticate**: Verify identity on protected routes
- **Authorize**: Check permissions before operations
- **Rate limit**: Prevent abuse

### 4. Performance
- **Database indexes**: Index frequently queried fields
- **N+1 prevention**: Use joins or batching
- **Caching**: Cache expensive operations
- **Async operations**: Don't block the event loop
- **Connection pooling**: Reuse database connections

## Quick Patterns

### Route Definition
```typescript
import { Router } from 'express';
import { UserController } from './user.controller';
import { authMiddleware } from '@/middleware/auth';

const router = Router();
const controller = new UserController();

// Public route
router.post('/users/register', controller.register);

// Protected route
router.get('/users/me', authMiddleware, controller.getCurrentUser);

export { router as userRoutes };
```

### Controller Pattern
```typescript
import { Request, Response, NextFunction } from 'express';
import { UserService } from './user.service';

export class UserController extends BaseController {
  private userService: UserService;

  constructor() {
    super();
    this.userService = new UserService();
  }

  register = async (req: Request, res: Response, next: NextFunction) => {
    try {
      // 1. Validate input
      const dto = RegisterDto.parse(req.body);

      // 2. Call service
      const result = await this.userService.register(dto);

      // 3. Return response
      return this.ok(res, result);
    } catch (error) {
      // 4. Pass to error handler
      next(error);
    }
  };
}
```

### Service Pattern
```typescript
import { UserRepository } from './user.repository';
import { hashPassword } from '@/utils/crypto';
import { ServiceResponse } from '@/types';

export class UserService {
  private userRepo: UserRepository;

  constructor() {
    this.userRepo = new UserRepository();
  }

  async register(dto: RegisterDto): Promise<ServiceResponse<User>> {
    // 1. Business logic validation
    const exists = await this.userRepo.findByEmail(dto.email);
    if (exists) {
      throw new ConflictError('Email already registered');
    }

    // 2. Data transformation
    const hashedPassword = await hashPassword(dto.password);

    // 3. Repository call
    const user = await this.userRepo.create({
      ...dto,
      password: hashedPassword,
    });

    // 4. Return success response
    return {
      success: true,
      data: user,
    };
  }
}
```

### Repository Pattern
```typescript
import { PrismaClient } from '@prisma/client';

export class UserRepository {
  private prisma: PrismaClient;

  constructor() {
    this.prisma = new PrismaClient();
  }

  async create(data: CreateUserDto): Promise<User> {
    try {
      return await this.prisma.user.create({
        data,
      });
    } catch (error) {
      throw new DatabaseError('Failed to create user', error);
    }
  }

  async findByEmail(email: string): Promise<User | null> {
    return await this.prisma.user.findUnique({
      where: { email },
    });
  }
}
```

## Error Handling Pattern

### Custom Error Classes
```typescript
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400);
  }
}

export class NotFoundError extends AppError {
  constructor(message: string) {
    super(message, 404);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(message, 401);
  }
}
```

### Error Handler Middleware
```typescript
export const errorHandler = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // Log error (with Sentry, etc.)
  logger.error(error);

  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        message: error.message,
        code: error.statusCode,
      },
    });
  }

  // Unknown error - don't expose details
  return res.status(500).json({
    success: false,
    error: {
      message: 'Internal server error',
      code: 500,
    },
  });
};
```

## Database Best Practices

### Always Use Transactions for Multiple Operations
```typescript
async transferFunds(from: string, to: string, amount: number) {
  return await this.prisma.$transaction(async (tx) => {
    // Deduct from sender
    await tx.account.update({
      where: { id: from },
      data: { balance: { decrement: amount } },
    });

    // Add to receiver
    await tx.account.update({
      where: { id: to },
      data: { balance: { increment: amount } },
    });

    // Log transfer
    await tx.transfer.create({
      data: { from, to, amount },
    });
  });
}
```

### Prevent N+1 Queries
```typescript
// ❌ Bad: N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({
    where: { userId: user.id },
  });
}

// ✅ Good: Single query with include
const users = await prisma.user.findMany({
  include: { posts: true },
});
```

### Use Indexes
```prisma
model User {
  id    String @id @default(uuid())
  email String @unique // Automatic index
  name  String

  @@index([name]) // Explicit index if you query by name often
}
```

## Authentication Pattern

### JWT Middleware
```typescript
export const authMiddleware = async (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    // 1. Extract token
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) {
      throw new UnauthorizedError('No token provided');
    }

    // 2. Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);

    // 3. Attach user to request
    req.user = decoded;

    next();
  } catch (error) {
    next(new UnauthorizedError('Invalid token'));
  }
};
```

## Validation Pattern

### Using Zod
```typescript
import { z } from 'zod';

const RegisterSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
});

type RegisterDto = z.infer<typeof RegisterSchema>;

// In controller
const dto = RegisterSchema.parse(req.body); // Throws if invalid
```

## API Response Format

### Consistent Response Structure
```typescript
// Success
{
  "success": true,
  "data": { /* response data */ },
  "meta": { /* pagination, etc. */ }
}

// Error
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { /* optional */ }
  }
}
```

### BaseController Helper
```typescript
export class BaseController {
  protected ok<T>(res: Response, data: T) {
    return res.status(200).json({
      success: true,
      data,
    });
  }

  protected created<T>(res: Response, data: T) {
    return res.status(201).json({
      success: true,
      data,
    });
  }

  protected noContent(res: Response) {
    return res.status(204).send();
  }
}
```

## Testing Guidelines

### Unit Test Services
```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepo = {
      findByEmail: jest.fn(),
      create: jest.fn(),
    } as any;

    service = new UserService();
    (service as any).userRepo = mockRepo;
  });

  it('should throw if email already exists', async () => {
    mockRepo.findByEmail.mockResolvedValue({ id: '1' } as any);

    await expect(
      service.register({ email: 'test@test.com', password: 'pass' })
    ).rejects.toThrow('Email already registered');
  });
});
```

### Integration Test Endpoints
```typescript
describe('POST /users/register', () => {
  it('should create user with valid data', async () => {
    const response = await request(app)
      .post('/users/register')
      .send({
        email: 'test@test.com',
        password: 'Password123',
        name: 'Test User',
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.email).toBe('test@test.com');
  });
});
```

## Resources

For deeper dives:
- `resources/database-patterns.md` - Advanced database patterns
- `resources/authentication.md` - Auth strategies
- `resources/api-design.md` - RESTful API design
- `resources/performance.md` - Backend optimization
- `resources/security.md` - Security best practices

## When NOT to Use This Skill

This skill is for **backend/API development**. For other domains:
- **Frontend/UI**: Use `frontend-dev-guidelines` skill
- **Database design**: Use `database-specialist` skill
- **DevOps**: Use infrastructure skills

## Quick Reference

**Layers**: Route → Controller → Service → Repository
**Errors**: Try-catch all, centralized handler, typed errors
**Security**: Validate, sanitize, auth, authorize, rate limit
**Database**: Transactions, prevent N+1, use indexes
**Testing**: Unit services, integration endpoints

---

*This skill follows Anthropic's progressive disclosure: <500 lines main file, detailed resources available.*
