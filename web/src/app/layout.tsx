import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '700']
});

export const metadata = {
  title: 'LinkSage',
  description: 'Transform bookmarks into actionable insights with AI-powered intelligence.'
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.className}>
      <body className="bg-background text-foreground flex flex-col min-h-screen">
        {children}
      </body>
    </html>
  );
}