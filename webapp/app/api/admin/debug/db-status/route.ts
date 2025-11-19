import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { getAuthDatabase } from '@/lib/auth-db';

// Debug endpoint to inspect DB file and tables. Access control:
// - Allowed when NEXTAUTH_DEBUG=true OR
// - When request header 'x-admin-debug-token' equals ADMIN_DEBUG_TOKEN env var

function isAuthorized(req: NextRequest) {
  if (process.env.NEXTAUTH_DEBUG === 'true' || process.env.NODE_ENV !== 'production') return true;
  const token = req.headers.get('x-admin-debug-token');
  if (token && process.env.ADMIN_DEBUG_TOKEN && token === process.env.ADMIN_DEBUG_TOKEN) return true;
  return false;
}

export async function GET(request: NextRequest) {
  if (!isAuthorized(request)) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  const DB_DIR = process.env.DATABASE_DIR || path.join(process.cwd(), 'data');
  const DB_PATH = path.join(DB_DIR, 'macacolandia.db');

  const result: any = { dbPath: DB_PATH, exists: false };

  try {
    result.exists = fs.existsSync(DB_PATH);
    if (result.exists) {
      const stat = fs.statSync(DB_PATH);
      result.size = stat.size;
      result.mtime = stat.mtime;
    }

    // Try opening DB via getAuthDatabase (this will initialize tables if needed)
    try {
      const db = getAuthDatabase();
      const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").all();
      result.tables = tables.map((r: any) => r.name);
    } catch (dbErr) {
      result.dbError = (dbErr instanceof Error) ? dbErr.message : String(dbErr);
    }

    return NextResponse.json(result, { status: 200 });
  } catch (err) {
    console.error('[DEBUG][DB-STATUS] Error:', err);
    return NextResponse.json({ error: 'Failed to get DB status', details: (err as any)?.message || String(err) }, { status: 500 });
  }
}
