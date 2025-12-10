'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const isAuthenticated = typeof window !== 'undefined' && api.isAuthenticated();

  const handleLogout = async () => {
    await api.logout();
    router.push('/login');
  };

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            🔐 Auth System
          </Link>

          <div className="flex gap-4 items-center">
            {!isAuthenticated ? (
              <>
                <Link
                  href="/login"
                  className={`px-4 py-2 rounded ${
                    pathname === '/login' ? 'bg-blue-700' : 'hover:bg-blue-700'
                  }`}
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className={`px-4 py-2 rounded ${
                    pathname === '/register' ? 'bg-blue-700' : 'hover:bg-blue-700'
                  }`}
                >
                  Register
                </Link>
              </>
            ) : (
              <>
                <Link
                  href="/dashboard"
                  className={`px-4 py-2 rounded ${
                    pathname === '/dashboard' ? 'bg-blue-700' : 'hover:bg-blue-700'
                  }`}
                >
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 rounded bg-red-500 hover:bg-red-600"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}