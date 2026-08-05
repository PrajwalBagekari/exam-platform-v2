from langgraph.graph import StateGraph

from state import ExamState

from nodes import (
    pdf_node,
    image_node,
    ocr_node,
    question_node,
    rag_node,
    exam_node
)

builder = StateGraph(
    ExamState
)

# Nodes
builder.add_node(
    "pdf",
    pdf_node
)

builder.add_node(
    "image",
    image_node
)

builder.add_node(
    "ocr",
    ocr_node
)

builder.add_node(
    "question",
    question_node
)

builder.add_node(
    "rag",
    rag_node
)

builder.add_node(
    "exam",
    exam_node
)

# Entry Point
builder.set_entry_point(
    "pdf"
)

# Workflow
builder.add_edge(
    "pdf",
    "image"
)

builder.add_edge(
    "image",
    "question"
)

builder.add_edge(
    "question",
    "rag"
)

builder.add_edge(
    "rag",
    "exam"
)

# Final Node
builder.set_finish_point(
    "exam"
)

graph = builder.compile()