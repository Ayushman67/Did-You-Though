import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'DidYouThough? | Meeting Accountability',
  description: 'Turn meeting conversations into visible, trackable commitments',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
