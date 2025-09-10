import math

# -------------------------------
# Helper functions
# -------------------------------

def parse_input(expr: str) -> float:
    """Evaluate simple math expressions safely."""
    try:
        return eval(expr, {"__builtins__": {}})
    except:
        raise ValueError("Invalid input.")

def parse_multiplier_input(expr: str) -> float:
    """
    Parse multiplier input in format like '2D', '4D' and return numeric value.
    Example: '4D' -> 4.0
    """
    expr = expr.strip().upper().replace(" ", "")
    if expr.endswith("D"):
        return float(expr[:-1])
    else:
        raise ValueError("Multiplier must be entered in the format '2D', '4D', etc.")

def nearest_rivet_size(D_target):
    """Round D_target to nearest standard rivet size (in inches)."""
    standard_rivets = [1/16, 3/32, 1/8, 5/32, 3/16, 7/32, 1/4]
    return min(standard_rivets, key=lambda x: abs(x - D_target))

# -------------------------------
# Rivet Layout Calculation
# -------------------------------

def rivet_layout(length, width, thickness, spacing_mult, edge_mult):
    """
    Compute rivet layout with even spacing along edges.
    Corner rivets counted only once.
    Returns all relevant info for output.
    """
    D_target = 3 * thickness
    D = nearest_rivet_size(D_target)
    
    edge_distance = edge_mult * D
    nominal_spacing = spacing_mult * D

    effective_length = length - 2 * edge_distance
    effective_width = width - 2 * edge_distance

    n_length = max(1, math.floor(effective_length / nominal_spacing) + 1)
    n_width = max(1, math.floor(effective_width / nominal_spacing) + 1)

    actual_spacing_length = effective_length / (n_length - 1) if n_length > 1 else 0
    actual_spacing_width = effective_width / (n_width - 1) if n_width > 1 else 0

    total_rivets = 2 * n_length + 2 * n_width - 4  # corners counted once

    recommended_length = thickness + 1/16

    return {
        "thickness": thickness,
        "target_diameter": D_target,
        "chosen_diameter": D,
        "edge_distance": edge_distance,
        "spacing_multiplier": spacing_mult,
        "nominal_spacing": nominal_spacing,
        "actual_spacing_length": actual_spacing_length,
        "actual_spacing_width": actual_spacing_width,
        "rivets_along_length": n_length,
        "rivets_along_width": n_width,
        "total_rivets": total_rivets,
        "recommended_length": recommended_length
    }

# -------------------------------
# Explanation
# -------------------------------

def explain(details, question):
    q = question.lower()
    if any(word in q for word in ["diameter", "rivet size", "how big", "rivet width"]):
        return f"Target rivet diameter = 3 × thickness = {details['target_diameter']:.4f}, rounded to nearest standard size = {details['chosen_diameter']:.4f}"
    elif any(word in q for word in ["edge", "margin", "distance from edge"]):
        return f"Edge distance = chosen multiplier × rivet diameter = {details['edge_distance']:.4f}"
    elif any(word in q for word in ["spacing", "gap", "between rivets"]):
        return (f"Nominal spacing = {details['spacing_multiplier']} × rivet diameter = {details['nominal_spacing']:.4f}\n"
                f"Actual even spacing along length = {details['actual_spacing_length']:.4f}, width = {details['actual_spacing_width']:.4f}")
    elif any(word in q for word in ["how many rivets", "number of rivets", "total rivets"]):
        return f"Total rivets = {details['total_rivets']}"
    elif any(word in q for word in ["length rivets", "along length"]):
        return f"Rivets along length = {details['rivets_along_length']}"
    elif any(word in q for word in ["width rivets", "along width"]):
        return f"Rivets along width = {details['rivets_along_width']}"
    elif any(word in q for word in ["rivet length", "shank"]):
        return f"Recommended rivet length (shank) = {details['recommended_length']:.4f}"
    elif any(word in q for word in ["how", "why", "calculated", "formula"]):
        return ("Calculations:\n"
                "- Rivet diameter = 3 × sheet thickness, rounded to nearest standard size\n"
                "- Edge distance = user-defined multiplier × chosen diameter\n"
                "- Spacing = user-defined multiplier × chosen diameter\n"
                "- Number of rivets along a dimension = floor((dimension - 2*edge_distance)/spacing) + 1\n"
                "- Actual spacing evenly distributed along effective dimension\n"
                "- Corner rivets are counted once")
    else:
        return "Sorry, I don't understand that question. Try asking about diameter, edge distance, spacing, rivet length, or total rivets."

# -------------------------------
# Main Program
# -------------------------------

def main():
    print("=== Rivet Layout Calculator ===")
    unit_choice = input("Select units: inches or mm (type 'inches' or 'mm'): ").strip().lower()
    units_factor = 1.0 if unit_choice == "inches" else 25.4  # convert mm to inches

    all_layouts = []

    while True:
        thickness = parse_input(input(f"\nEnter sheet thickness ({unit_choice}): ")) / units_factor
        print("Suggested minimum edge multiplier: 2D")
        print("Suggested minimum spacing multiplier: 4D")

        edge_mult = parse_multiplier_input(input("Enter edge distance multiplier (e.g., 2D): "))
        spacing_mult = parse_multiplier_input(input("Enter spacing multiplier (e.g., 4D): "))

        length = parse_input(input(f"Enter sheet length ({unit_choice}): ")) / units_factor
        width = parse_input(input(f"Enter sheet width ({unit_choice}): ")) / units_factor

        layout_details = rivet_layout(length, width, thickness, spacing_mult, edge_mult)
        all_layouts.append(layout_details)

        print(f"\nTotal rivets for this layout: {layout_details['total_rivets']}")
        cont = input("Do you want to calculate another sheet? (y/n): ").strip().lower()
        if cont != 'y':
            break

    print("\n--- All Calculated Layouts ---")
    for idx, layout in enumerate(all_layouts, 1):
        print(f"Layout {idx}: Total rivets = {layout['total_rivets']} (Length {layout['rivets_along_length']} x Width {layout['rivets_along_width']})")

    # Interactive Q&A
    print("\nYou can now ask questions about the calculations. Type 'exit' to quit.")
    while True:
        q = input("Ask: ")
        if q.lower() in ["exit", "quit"]:
            break
        # For multi-layout, ask for layout number
        if len(all_layouts) > 1:
            layout_num = input(f"Which layout (1-{len(all_layouts)})? ").strip()
            if layout_num.isdigit() and 1 <= int(layout_num) <= len(all_layouts):
                layout_details = all_layouts[int(layout_num)-1]
            else:
                print("Invalid layout number. Using the first layout by default.")
                layout_details = all_layouts[0]
        else:
            layout_details = all_layouts[0]
        print(explain(layout_details, q))

if __name__ == "__main__":
    main()
