import { NextResponse } from "next/server";
import { deleteTodo } from "@/lib/queries";

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    await deleteTodo(id);
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Error deleting todo:", error);
    return NextResponse.json(
      { success: false, error: "Failed to delete todo" },
      { status: 500 },
    );
  }
}
