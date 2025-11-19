import { NextResponse } from 'next/server';
import { getGlobalStats, getGameStats } from '@/lib/db';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const gameType = searchParams.get('gameType');
    const guildId = searchParams.get('guildId');

    const globalStats = getGlobalStats(guildId || undefined);
    const gameStats = getGameStats(gameType || undefined, guildId || undefined);

    return NextResponse.json({
      global: globalStats,
      games: gameStats,
    });
  } catch (error) {
    console.error('Error fetching stats:', error);
    return NextResponse.json({ error: 'Failed to fetch stats' }, { status: 500 });
  }
}
