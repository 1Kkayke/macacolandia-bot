import { NextResponse } from 'next/server';
import { getServers } from '@/lib/db';

export async function GET() {
  try {
    const servers = getServers();
    return NextResponse.json(servers);
  } catch (error) {
    console.error('Error fetching servers:', error);
    return NextResponse.json({ error: 'Failed to fetch servers' }, { status: 500 });
  }
}
