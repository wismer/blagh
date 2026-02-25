import { NextResponse } from "next/server";
import { completeTodo } from "@/lib/queries";

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const todo = await completeTodo(id);
    return NextResponse.json({ success: true, todo });
  } catch (error) {
    console.error("Error completing todo:", error);
    return NextResponse.json(
      { success: false, error: "Failed to complete todo" },
      { status: 500 },
    );
  }
}
