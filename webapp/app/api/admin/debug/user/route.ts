import { NextRequest, NextResponse } from 'next/server';
import path from 'path';
import { getAuthDatabase } from '@/lib/auth-db';

// Protected debug endpoint: returns auth_users row for given email.
// Access allowed when NEXTAUTH_DEBUG=true OR when header x-admin-debug-token matches ADMIN_DEBUG_TOKEN.

function isAuthorized(req: NextRequest) {
  if (process.env.NEXTAUTH_DEBUG === 'true' || process.env.NODE_ENV !== 'production') return true;
  const token = req.headers.get('x-admin-debug-token');
  if (token && process.env.ADMIN_DEBUG_TOKEN && token === process.env.ADMIN_DEBUG_TOKEN) return true;
  return false;
}

export async function GET(req: NextRequest) {
  if (!isAuthorized(req)) return NextResponse.json({ error: 'Forbidden' }, { status: 403 });

  const url = new URL(req.url);
  const email = url.searchParams.get('email');
  if (!email) return NextResponse.json({ error: 'Missing email parameter' }, { status: 400 });

  try {
    const db = getAuthDatabase();
    const row = db.prepare('SELECT * FROM auth_users WHERE email = ?').get(email);
    if (!row) return NextResponse.json({ error: 'User not found' }, { status: 404 });

    return NextResponse.json({ user: row }, { status: 200 });
  } catch (err) {
    console.error('[DEBUG][USER] Error:', err);
    return NextResponse.json({ error: 'Failed to query user', details: (err as any)?.message || String(err) }, { status: 500 });
  }
}
