# Git Push Guide - Excluding Description Folder

## Step-by-Step Instructions

### Step 1: Add Description folder to .gitignore
✅ **DONE** - Description/ has been added to .gitignore

### Step 2: Check Git Status
```bash
git status
```
This shows what files have changed.

### Step 3: Un-track Description folder (if already tracked)
If Description files are already in Git, remove them:
```bash
git rm -r --cached Description/
```
**Note:** This removes them from Git but keeps them on your local machine.

### Step 4: Stage Your Changes
```bash
# Add specific files
git add core/
git add frontend/
git add .gitignore
git add *.md
git add *.py

# OR add all except ignored
git add .
```

### Step 5: Commit Your Changes
```bash
git commit -m "Fixed ML prediction bug and removed emojis

- Fixed risk level mapping (0/1/2 -> Low/Medium/High)
- Removed all emojis from code
- Fixed SQLAlchemy mapper error permanently
- Updated .gitignore to exclude Description folder"
```

### Step 6: Push to Repository
```bash
# Push to current branch
git push

# OR specify branch
git push origin saif-2.0
```

## Quick Command Sequence

```bash
# 1. Remove Description from Git tracking (if needed)
git rm -r --cached Description/

# 2. Add all changes except ignored files
git add .

# 3. Commit
git commit -m "Your commit message"

# 4. Push
git push origin saif-2.0
```

## Verify Description is Excluded

After adding to .gitignore, check:
```bash
git status
```

You should NOT see Description/ files listed.

## What Will Be Pushed

✅ **Included:**
- All code files (.py)
- Configuration files
- Frontend files
- Backend services
- ML service fixes
- .gitignore updates

❌ **Excluded:**
- Description/ folder (all .md documentation files)
- .pkl model files
- .csv data files
- __pycache__ folders

## Important Notes

1. **.gitignore only affects untracked files**
   - If Description/ is already in Git, use `git rm -r --cached Description/`

2. **Local files stay safe**
   - `git rm --cached` removes from Git but keeps local files

3. **Check before pushing**
   - Always run `git status` to verify what will be pushed

## Common Issues

### If Description files still show up:
```bash
# Force remove from tracking
git rm -r --cached Description/

# Add .gitignore change
git add .gitignore

# Commit the removal
git commit -m "Remove Description folder from tracking"
```

### If you want to push to a new branch:
```bash
git checkout -b new-branch-name
git push origin new-branch-name
```

## Your Current Branch

You're on: **saif-2.0**

Push with:
```bash
git push origin saif-2.0
```
