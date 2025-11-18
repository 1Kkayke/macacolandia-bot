import { NextResponse } from 'next/server';
import { getUserGameHistory, getUserAchievements } from '@/lib/db';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ userId: string }> }
) {
  try {
    const { userId } = await params;
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '50');
    const type = searchParams.get('type');

    if (type === 'achievements') {
      const achievements = getUserAchievements(userId);
      return NextResponse.json(achievements);
    }

    const gameHistory = getUserGameHistory(userId, limit);
    return NextResponse.json(gameHistory);
  } catch (error) {
    console.error('Error fetching game history:', error);
    return NextResponse.json({ error: 'Failed to fetch game history' }, { status: 500 });
  }
}
