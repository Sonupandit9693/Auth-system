'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { User } from '@/types/auth';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [protectedData, setProtectedData] = useState<string>('');

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const userData = await api.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to load user:', error);
      router.push('/login');
    } finally {
      setLoading(false);
    }
  };

  const testProtectedRoute = async () => {
    try {
      const response = await api.authenticatedRequest('/auth/protected');
      const data = await response.json();
      setProtectedData(data.message);
    } catch (error) {
      console.error('Protected route error:', error);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto text-center">
          <div className="text-2xl">Loading...</div>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Dashboard</h1>

        <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
          <h2 className="text-2xl font-bold mb-4">Welcome, {user.username}! 🎉</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">User Information</h3>
              <div className="space-y-2">
                <p><span className="font-semibold">User ID:</span> {user.user_id}</p>
                <p><span className="font-semibold">Email:</span> {user.email}</p>
                <p><span className="font-semibold">Username:</span> {user.username}</p>
                <p>
                  <span className="font-semibold">Verified:</span>{' '}
                  <span className={user.is_verified ? 'text-green-600' : 'text-orange-600'}>
                    {user.is_verified ? '✓ Yes' : '✗ No'}
                  </span>
                </p>
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Token Information</h3>
              <div className="space-y-2">
                <p><span className="font-semibold">Access Token:</span> Stored ✓</p>
                <p><span className="font-semibold">Refresh Token:</span> Stored ✓</p>
                <p><span className="font-semibold">Expires:</span> 15 minutes</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Test Protected Route</h2>
          <p className="text-gray-600 mb-4">
            Click the button below to test accessing a protected API endpoint
          </p>
          
          <button
            onClick={testProtectedRoute}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Test Protected API
          </button>

          {protectedData && (
            <div className="mt-4 p-4 bg-green-100 border border-green-400 rounded-lg">
              <p className="text-green-800 font-semibold">✓ Success!</p>
              <p className="text-green-700">{protectedData}</p>
            </div>
          )}
        </div>

        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-bold text-blue-800 mb-2">🔒 Security Features Active</h3>
          <ul className="list-disc list-inside text-blue-700 space-y-1">
            <li>Bcrypt password hashing (12 rounds)</li>
            <li>JWT access tokens (15 min expiry)</li>
            <li>Refresh token rotation</li>
            <li>Rate limiting (5 requests/minute)</li>
            <li>Account lockout (5 failed attempts)</li>
            <li>Audit logging enabled</li>
          </ul>
        </div>
      </div>
    </div>
  );
}