import './globals.css'
import { Inter } from 'next/font/google'
import { Toaster } from 'react-hot-toast'
import { Providers } from "@/components/providers";

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'AI Real Estate Investing',
  description: 'Scaling Success with Automation',
  other: {
    'cache-control': 'no-cache, no-store, must-revalidate',
    'pragma': 'no-cache',
    'expires': '0',
    'version': Date.now().toString(), // Force cache invalidation
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          {children}
          <Toaster position="top-right" />
        </Providers>
      </body>
    </html>
  )
}
