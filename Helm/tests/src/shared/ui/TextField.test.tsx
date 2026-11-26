import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

import { TextField } from "@/shared/ui"

describe("TextField", () => {
  it("keeps its label as the input's accessible name while a message shows", () => {
    render(<TextField label="Name" error="Name the search." />)

    expect(screen.getByLabelText("Name", { exact: true })).toBeInTheDocument()
  })

  it("announces the message as the input's description", () => {
    render(<TextField label="Name" error="Name the search." />)

    expect(screen.getByRole("textbox", { name: "Name" })).toHaveAccessibleDescription("Name the search.")
  })

  it("marks the input invalid only while a message shows", () => {
    const { rerender } = render(<TextField label="Name" error="Name the search." />)
    expect(screen.getByRole("textbox", { name: "Name" })).toHaveAttribute("aria-invalid", "true")

    rerender(<TextField label="Name" />)

    expect(screen.getByRole("textbox", { name: "Name" })).not.toHaveAttribute("aria-invalid")
  })

  it("ties its label to the id a caller gives the input", () => {
    render(<TextField id="vessel-name" label="Vessel name" />)

    expect(screen.getByLabelText("Vessel name")).toHaveAttribute("id", "vessel-name")
  })
})
