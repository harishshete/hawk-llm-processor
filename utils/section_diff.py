import difflib


def compare_sections(old_sections, new_sections):
    changes = []

    all_sections = set(old_sections.keys()) | set(new_sections.keys())

    for section in all_sections:

        old_content = old_sections.get(section, "")
        new_content = new_sections.get(section, "")

        # New section
        if not old_content and new_content:
            changes.append(
                f"""
SECTION: {section}

ADDED SECTION:
{new_content}
"""
            )
            continue

        # Removed section
        if old_content and not new_content:
            changes.append(
                f"""
SECTION: {section}

REMOVED SECTION:
{old_content}
"""
            )
            continue

        # Same content
        if old_content == new_content:
            continue

        # Generate line diff
        diff = difflib.ndiff(
            old_content.splitlines(),
            new_content.splitlines()
        )

        section_changes = []

        old_line = None

        for line in diff:

            if line.startswith("- "):
                old_line = line[2:]

            elif line.startswith("+ ") and old_line:
                section_changes.append(
                    f"""
OLD: {old_line}
NEW: {line[2:]}
"""
                )
                old_line = None

            elif line.startswith("+ ") and not old_line:
                section_changes.append(
                    f"ADDED: {line[2:]}"
                )

            elif line.startswith("- ") and not old_line:
                section_changes.append(
                    f"REMOVED: {line[2:]}"
                )

        if section_changes:
            formatted = "\n".join(section_changes)

            changes.append(
                f"""
SECTION: {section}

CHANGES:
{formatted}
"""
            )

    return "\n\n".join(changes)