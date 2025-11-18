import { NextResponse } from 'next/server';
import { addCoinsToUser, getUser } from '@/lib/db';

export async function POST(
  request: Request,
  { params }: { params: Promise<{ userId: string }> }
) {
  try {
    const { userId } = await params;
    const body = await request.json();
    const { amount, description } = body;

    if (typeof amount !== 'number') {
      return NextResponse.json({ error: 'Invalid amount' }, { status: 400 });
    }

    // Verify user exists
    const user = getUser(userId);
    if (!user) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 });
    }

    const success = addCoinsToUser(userId, amount, description);
    
    if (!success) {
      return NextResponse.json({ error: 'Failed to update coins' }, { status: 500 });
    }

    // Return updated user
    const updatedUser = getUser(userId);
    return NextResponse.json(updatedUser);
  } catch (error) {
    console.error('Error updating user coins:', error);
    return NextResponse.json({ error: 'Failed to update coins' }, { status: 500 });
  }
}
