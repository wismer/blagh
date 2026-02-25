import { NextResponse } from "next/server";
import { getTodos, createTodo, completeTodo, deleteTodo } from "@/lib/queries";

export async function GET() {
  try {
    const todos = await getTodos();
    return NextResponse.json({ success: true, todos });
  } catch (error) {
    console.error("Error fetching todos:", error);
    return NextResponse.json(
      { success: false, error: "Failed to fetch todos" },
      { status: 500 },
    );
  }
}

export async function POST(request: Request) {
  try {
    const { text, priority = 0 } = await request.json();

    if (!text) {
      return NextResponse.json(
        { success: false, error: "Text is required" },
        { status: 400 },
      );
    }

    const todo = await createTodo(text, priority);
    return NextResponse.json({ success: true, todo }, { status: 201 });
  } catch (error) {
    console.error("Error creating todo:", error);
    return NextResponse.json(
      { success: false, error: "Failed to create todo" },
      { status: 500 },
    );
  }
}
