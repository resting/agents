---
name: archive-done-tasks
description: Archive a completed task folder from /docs/tasks/ to /docs/done-features/ with sequential numeric prefixing. Use this skill whenever the user says "archive task", "mark task as done", "move task to done", "archive [task-name]", "done with [task-name]", or any variation of completing/archiving a task folder. Also trigger when the user references moving work from tasks to done-features, finishing a feature, or closing out a task.
---

# Archive Done Task

Move a completed task folder from `/docs/tasks/` into `/docs/done-features/` with an auto-incremented numeric prefix.

## Workflow

1. **Parse the task name** from the user's request. The user provides a task name (e.g., `wealth-calculations`).

2. **Verify the source exists.** Check if `/docs/tasks/{task-name}` exists.
   - If **not found**: respond with exactly: `Task not found: /docs/tasks/{task-name}`
   - If **found**: proceed.

3. **Determine the next sequence number.**
   - List all folders in `/docs/done-features/` (create the directory if it doesn't exist).
   - Each archived folder is prefixed with a 3-digit zero-padded number: `000-`, `001-`, `002-`, etc.
   - Find the highest existing numeric prefix. The new prefix is that number + 1.
   - If `/docs/done-features/` is empty, start at `000`.

4. **Move and rename.**
   - Move the entire `/docs/tasks/{task-name}` folder (including all subfolders and files) to `/docs/done-features/{NNN}-{task-name}`.
   - Use `mv` for an atomic move.

5. **Confirm** to the user with the old and new paths.

## Implementation

```bash
TASK_NAME="<user-provided-task-name>"
SOURCE="/docs/tasks/$TASK_NAME"
DEST_DIR="/docs/done-features"

# 1. Check source exists
if [ ! -d "$SOURCE" ]; then
  echo "Task not found: $SOURCE"
  exit 1
fi

# 2. Ensure destination directory exists
mkdir -p "$DEST_DIR"

# 3. Determine next sequence number
LAST_NUM=$(ls -1 "$DEST_DIR" 2>/dev/null | grep -oP '^\d{3}' | sort -n | tail -1)
if [ -z "$LAST_NUM" ]; then
  NEXT_NUM="000"
else
  NEXT_NUM=$(printf "%03d" $((10#$LAST_NUM + 1)))
fi

# 4. Move
mv "$SOURCE" "$DEST_DIR/${NEXT_NUM}-${TASK_NAME}"

echo "Archived: $SOURCE → $DEST_DIR/${NEXT_NUM}-${TASK_NAME}"
```

## Edge Cases

- If `/docs/done-features/` doesn't exist yet, create it. First archive gets prefix `000`.
- If non-conforming folders exist in `/docs/done-features/` (no numeric prefix), ignore them when calculating the next number.
- Preserve the original folder name after the prefix (e.g., `wealth-calculations` stays as-is, just prefixed).
