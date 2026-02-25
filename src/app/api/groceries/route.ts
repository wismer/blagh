import { NextResponse } from "next/server";
import { getGroceries, createGrocery, deleteGrocery } from "@/lib/queries";

export async function GET() {
  try {
    const groceries = await getGroceries();
    return NextResponse.json({ success: true, groceries });
  } catch (error) {
    console.error("Error fetching groceries:", error);
    return NextResponse.json(
      { success: false, error: "Failed to fetch groceries" },
      { status: 500 },
    );
  }
}

export async function POST(request: Request) {
  try {
    const { item_name, quantity = 1 } = await request.json();

    if (!item_name) {
      return NextResponse.json(
        { success: false, error: "Item name is required" },
        { status: 400 },
      );
    }

    const grocery = await createGrocery(item_name, quantity);
    return NextResponse.json({ success: true, grocery }, { status: 201 });
  } catch (error) {
    console.error("Error creating grocery:", error);
    return NextResponse.json(
      { success: false, error: "Failed to create grocery item" },
      { status: 500 },
    );
  }
}
