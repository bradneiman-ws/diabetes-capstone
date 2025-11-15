# Git Safety Protocol v1  
_For the Diabetes Capstone Project_

This guide prevents 45-minute Git emergencies, protects your work, and keeps your development workflow smooth and predictable.

---

# 1. Purpose

This repository includes:
- notebooks  
- Python packages (`src/`, `ds_viz/`)  
- auto-generated reports/figures  
- path utilities  
- experimental branches  

This complexity can cause:
- failed rebases  
- local changes blocking pulls  
- `.gitignore` conflicts  
- messy notebook diffs  
- duplicated or regenerated files  

This protocol prevents those issues.

---

# 2. Start-of-Session Checklist (Run Before You Code)

### **A. Check repo health**
git sanity

## What to look for when running 'git sanity'
- Uncommitted changes
- Untracked files
- Pending conflicts
- Unpushed commits

### **B. If clean, sync with origin***
git pull --rebase
git status

### **C. If NOT clean**
If you want to KEEP changes:
git add -A
git commit -m "WIP: <short summary>"
git push
git pull --rebase

If you want to DISCARD changes:
git reset --hard HEAD
git clean -fd
git pull --rebase

# 3. During-Work Rules
* Never start a rebase or merge with uncommitted changes.
* Avoid editing .gitignore casually. Treat it as a config file.
* Don't commit auto-generated outputs (e.g., figures, reports, temp files).
* Keep commits small and frequent.
* Checkpoint frequently when experimenting:
  git wip

# 4. End-of-Session Checklist
Before stopping:

## A. Save your work
git add -A
git commit -m "WIP: end of session"
git push

## B. Or use the shortcut
git wip

This prevents stale code and surprise conflicts tomorrow.

# 5. Panic Guide (When Git Freaks Out)
## Step A -- Don't run random commands
Take your hands off the keyboard. This prevents deeper problems.

## Step B -- Diagnose
Run:
git status
git sanity

Identify:
* Am I in the middle of a rebase?
* Are there conflicts?
* Do I have unstaged changes?
* Are there unpushed commits?

## Step C -- If stuck in a rebase
You have 3 safe options:

### i. Abort completely
git rebase --abort
git reset --hard HEAD
git pull --rebase

### ii. Save changes, then retry
git rebase --abort
git add -A
git commit -m "WIP: before rebase"
git push
git pull --rebase

### iii. Continue the rebase (after fixing conflicts)
git add <files>
git rebase --continue

## Step D -- If not in a rebase, but everything is messy
### Keep everything
git add -A
git commit -m "WIP: messy state"
git push

### Throw everything away
(Only if you're *absolutely* sure)
git reset --hard HEAD
git clean -fd