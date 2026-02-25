import { NextResponse } from "next/server";
import { deleteGrocery } from "@/lib/queries";

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    await deleteGrocery(id);
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Error deleting grocery:", error);
    return NextResponse.json(
      { success: false, error: "Failed to delete grocery item" },
      { status: 500 },
    );
  }
}
