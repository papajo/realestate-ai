# Frontend - AI Real Estate Investing

Next.js 14 frontend application with React, TypeScript, and Tailwind CSS.

## Features

- ✅ User authentication (login/register)
- ✅ Dashboard with metrics and charts
- ✅ Lead pipeline management
- ✅ List stacking search
- ✅ AI Chatbot interface
- ✅ Property analysis with image upload
- ✅ Cash buyer management
- ✅ No-code tool builder with Monaco Editor
- ✅ Real-time notifications via WebSocket

## Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Development

```bash
npm run dev
```

Visit http://localhost:3000

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/              # Next.js app directory
│   ├── layout.tsx    # Root layout
│   ├── page.tsx      # Home page
│   └── globals.css   # Global styles
├── components/        # React components
│   ├── Dashboard.tsx
│   ├── Login.tsx
│   ├── LeadPipeline.tsx
│   ├── ListStacking.tsx
│   ├── Chatbot.tsx
│   ├── PropertyAnalysis.tsx
│   ├── CashBuyers.tsx
│   ├── NoCodeBuilder.tsx
│   ├── Metrics.tsx
│   └── NotificationPanel.tsx
├── hooks/            # Custom React hooks
│   ├── useAuth.tsx
│   └── useWebSocket.tsx
├── lib/              # Utilities
│   └── api.ts        # API client
└── public/           # Static assets
```

## Key Technologies

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first styling
- **Chart.js**: Data visualization
- **Monaco Editor**: Code editor component
- **Axios**: HTTP client
- **React Hot Toast**: Notifications
- **WebSocket**: Real-time updates

## API Integration

The frontend uses a centralized API client (`lib/api.ts`) that:
- Automatically adds authentication tokens
- Handles token refresh on 401 errors
- Provides consistent error handling

## Components

### Dashboard
Main application interface with tabbed navigation.

### LeadPipeline
View and manage leads with status updates.

### ListStacking
Search properties using public records.

### Chatbot
AI-powered conversation interface for lead qualification.

### PropertyAnalysis
Upload images for AI-powered property issue detection.

### CashBuyers
Browse and search cash buyer database.

### NoCodeBuilder
Generate tools from natural language descriptions.

## Development Notes

- All API calls require authentication (JWT token)
- WebSocket connection established on login
- Real-time notifications appear in notification panel
- Charts update based on lead data

## Troubleshooting

### "Cannot connect to API"
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`

### "WebSocket connection failed"
- Check `NEXT_PUBLIC_WS_URL` in `.env.local`
- Ensure backend WebSocket endpoint is accessible

### Build errors
- Clear `.next` directory: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`

