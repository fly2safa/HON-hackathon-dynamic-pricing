# Frontend - Next.js Application

**Owner:** Role 1 (Jason - Frontend Developer)

## Purpose
Next.js 14+ web application with modern UI for the HoneyGo pricing interface.

## Setup Instructions

### 1. Initialize Next.js Project
```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
Create `.env.local` with:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Run Development Server
```bash
npm run dev
```

Frontend runs on: http://localhost:3000

## Folder Structure to Create

```
frontend/
├── package.json               # Node dependencies
├── next.config.js             # Next.js configuration
├── tsconfig.json              # TypeScript configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── .env.local                 # Environment variables
├── app/                       # Next.js 14+ app router
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home page
│   ├── pricing/              # Pricing page
│   │   └── page.tsx
│   └── globals.css           # Global styles
├── components/                # React components
│   ├── PricingForm.tsx       # Pricing input form
│   ├── PricingResult.tsx     # Pricing display
│   ├── ReasoningExplainer.tsx # Agent reasoning display
│   ├── VoiceInput.tsx        # Voice input (E1 - Extra)
│   └── VoiceOutput.tsx       # Voice output (E2 - Extra)
├── lib/                       # Utilities
│   ├── api.ts                # API client
│   └── types.ts              # TypeScript types
└── public/                    # Static assets
    └── logo.png              # HoneyGo logo (copy from /images)
```

## Timeline
- **Dec 1 AM:** Set up Next.js project and folder structure
- **Dec 1 PM:** Build UI components with mock data
- **Dec 2:** Continue UI development
- **Dec 3 Eve:** Integrate with backend API
- **Dec 3-4:** Add voice features (E1, E2) if time permits
- **Dec 4:** Testing and polish

## Dependencies
- API contract from Dari (Role 3) - Dec 1 AM
- Backend API running for integration - Dec 3 Eve

## Extra Features (If Time Permits)
- **E1:** Voice Input (🎤 Mic Icon) - 2-3 hours
- **E2:** Voice Output (🔊 Speaker Icon) - 1-2 hours

## Reference
See `docs/project-structure-guide.md` for detailed setup instructions and sample code.

