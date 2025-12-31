import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import NavBar from '../components/NavBar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Urban Evolution AI',
  description: 'AI-Powered Urban Evolution Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <NavBar />
        <main className="min-h-screen bg-background text-foreground">
          {children}
        </main>
      </body>
    </html>
  )
}
