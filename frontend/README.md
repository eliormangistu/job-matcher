# Job Matcher — Frontend

AI-powered job matching application built with **Next.js, React, and TypeScript**.

The frontend allows users to browse job opportunities, authenticate with Google, upload a CV, and receive job matches based on their profile.

## Tech Stack

* Next.js 16
* React 19
* TypeScript
* Sass
* pnpm
* Google OAuth
* REST API
* ESLint

## Features

* Job listing and pagination
* Job details view
* Google authentication
* CV upload
* CV validation
* AI-powered job matching
* Match results
* Loading states
* Error handling and dedicated error page
* Responsive retro-inspired UI

## Project Structure

```text
frontend/
├── src/
│   ├── api/              # API client and endpoint functions
│   ├── app/              # Next.js routes and application layout
│   ├── components/       # Reusable React components
│   ├── config/           # Environment-specific configuration
│   ├── env/              # Environment variables
│   ├── lib/              # Shared utilities and error handling
│   ├── mocks/            # Mock data
│   ├── routes/           # Application routes
│   ├── styles/           # Global and component styles
│   ├── types/            # TypeScript types
│   └── validations/      # Client-side validation
├── public/
├── package.json
├── next.config.ts
└── tsconfig.json
```

## Getting Started

### Prerequisites

Make sure the following are installed:

* Node.js
* pnpm

### Install dependencies

```bash
pnpm install
```

### Environment Variables

Create a `.env.local` file in the frontend root:

```env
NEXT_PUBLIC_JOB_MATCHER_BACKEND_API_URL=http://127.0.0.1:8000
```

### Run the development server

```bash
pnpm dev
```

The application will be available at:

```text
http://localhost:3000
```

## Available Scripts

```bash
pnpm dev
```

Start the development server.

```bash
pnpm build
```

Create a production build.

```bash
pnpm start
```

Start the production server.

```bash
pnpm lint
```

Run ESLint.

## Backend

The frontend communicates with the Job Matcher FastAPI backend.

By default, the development environment expects the backend at:

```text
http://127.0.0.1:8000
```

Make sure the backend is running before using features such as:

* Job loading
* CV upload
* AI matching

## Application Routes

| Route      | Description            |
| ---------- | ---------------------- |
| `/`        | Home page              |
| `/jobs`    | Browse available jobs  |
| `/cv`      | CV upload and matching |
| `/error`   | Shared error page      |

## Development

The project uses a component-based architecture with shared:

* API functions
* TypeScript types
* Configuration
* Validation
* Error handling
* Styling

Application routes are centralized in:

```text
src/routes/routes.ts
```

This helps avoid hard-coded route strings throughout the application.

## License

This project is currently developed as a personal portfolio project.
