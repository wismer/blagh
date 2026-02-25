import { NextResponse } from "next/server";
import { scanAndSyncPosts } from "@/lib/blog";

export async function POST() {
  try {
    const count = await scanAndSyncPosts();
    return NextResponse.json({
      success: true,
      message: `Synced ${count} posts`,
      count,
    });
  } catch (error) {
    console.error("Error syncing posts:", error);
    return NextResponse.json(
      { success: false, error: "Failed to sync posts" },
      { status: 500 },
    );
  }
}
