# Vercel NOT_FOUND Error - Complete Fix & Understanding Guide

## ⚠️ Quick Fix for "cd: frontend: No such file or directory"

**If you're seeing this error:**
```
Running "install" command: `cd frontend && npm install`...
sh: line 1: cd: frontend: No such file or directory
Error: Command "cd frontend && npm install" exited with 1
```

**This means:** You set `rootDirectory` to `frontend` in the Vercel dashboard, but your `vercel.json` still has `cd frontend` in the commands.

**The fix:** Update `vercel.json` to remove `cd frontend` from all commands:

```json
{
  "buildCommand": "npm run build",
  "installCommand": "npm install",
  "outputDirectory": ".next",
  "framework": "nextjs"
}
```

**Why:** When `rootDirectory` is set, Vercel already changes to that directory BEFORE running commands. So `cd frontend` tries to go to `frontend/frontend` which doesn't exist!

---

## 1. The Fix ✅

### Primary Solution: Set Root Directory in Vercel Dashboard (RECOMMENDED)

**This is the most reliable fix:**

1. Go to your Vercel project: https://vercel.com/dashboard
2. Select your project
3. Navigate to **Settings** → **General**
4. Scroll to **Root Directory**
5. Click **Edit** and set it to: `frontend`
6. Click **Save**
7. **IMPORTANT:** Update `vercel.json` to work WITH rootDirectory (see below)
8. **Redeploy** your project (trigger a new deployment)

**Why this works:**
- Vercel will automatically change to the `frontend/` directory **BEFORE** running any commands
- Next.js auto-detection will work perfectly
- This is the official Vercel approach for monorepos

**⚠️ CRITICAL:** When `rootDirectory` is set in the dashboard, Vercel changes to that directory FIRST. Your `vercel.json` commands should NOT include `cd frontend` because you're already in that directory!

**Correct vercel.json for Dashboard rootDirectory:**
```json
{
  "buildCommand": "npm run build",
  "installCommand": "npm install",
  "outputDirectory": ".next",
  "framework": "nextjs"
}
```

**Why paths are different:**
- `outputDirectory`: `.next` (not `frontend/.next`) because paths are relative to `rootDirectory`
- Commands: No `cd frontend` because you're already in `frontend/` directory
- Framework: Explicitly tells Vercel this is Next.js

### Alternative Solution: vercel.json WITHOUT Dashboard rootDirectory

If you prefer NOT to use the dashboard setting, use this `vercel.json`:

```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "installCommand": "cd frontend && npm install",
  "outputDirectory": "frontend/.next",
  "framework": "nextjs",
  "ignoreCommand": "git diff --quiet HEAD^ HEAD ./frontend"
}
```

**What each field does:**
- `installCommand`: Changes to frontend directory and installs dependencies
- `buildCommand`: Changes to frontend directory, installs (if needed), and builds
- `outputDirectory`: Tells Vercel where to find the built Next.js app (relative to repo root)
- `framework`: Explicitly tells Vercel this is a Next.js project
- `ignoreCommand`: Only deploys when frontend code changes (optimization)

**To use this approach:**
1. **Remove** the `rootDirectory` setting from Vercel dashboard (or leave it empty)
2. Commit the `vercel.json` with `cd frontend` commands
3. Push to trigger a new deployment
4. Vercel will use these build commands

---

## 2. Root Cause Analysis 🔍

### What Was Actually Happening vs. What Should Happen

**What was happening (the problem):**
```
1. Vercel clones your repository
2. Vercel looks for Next.js at the ROOT directory (/)
3. Vercel checks: "Is there a package.json here?" → NO
4. Vercel checks: "Is there a next.config.js here?" → NO  
5. Vercel checks: "Is there a .next build output?" → NO
6. Vercel gives up: "NOT_FOUND - I can't find anything to deploy!"
```

**What should happen (the solution):**
```
1. Vercel clones your repository
2. Vercel changes to frontend/ directory (via rootDirectory setting)
   OR
   Vercel runs: cd frontend && npm install && npm run build
3. Vercel finds package.json in frontend/
4. Vercel finds next.config.js in frontend/
5. Vercel runs the build successfully
6. Vercel finds .next/ output directory
7. Vercel deploys successfully ✅
```

### What Conditions Triggered This Error?

1. **Monorepo Structure**
   - Your repo has both `frontend/` and `backend/` directories
   - Vercel defaults to looking at the repository root
   - Without explicit configuration, it can't find your Next.js app

2. **Missing Root Directory Configuration**
   - The `rootDirectory` setting wasn't configured in Vercel dashboard
   - The `vercel.json` existed but might have had issues with path resolution

3. **Build Output Path Confusion**
   - When build commands use `cd frontend`, the output is created in `frontend/.next`
   - But Vercel needs to know where to look for it relative to the repo root
   - The `outputDirectory` must be `frontend/.next` (not just `.next`)
   - **NEW ISSUE:** When `rootDirectory` is set, paths are relative to that directory, so `outputDirectory` should be `.next` (not `frontend/.next`)
   - **NEW ISSUE:** When `rootDirectory` is set, commands should NOT include `cd frontend` because Vercel already changes to that directory first

### The Misconception/Oversight

**Common misconception:** "Vercel will automatically detect my Next.js app wherever it is"

**Reality:**
- Vercel's auto-detection is excellent, but it only works at the repository root
- For subdirectories, you MUST explicitly tell Vercel where to look
- This is by design to prevent accidentally deploying the wrong part of a monorepo

**The oversight:** Assuming that having a `vercel.json` with build commands would be enough, without ensuring:
1. The paths are correct relative to repo root
2. The framework is explicitly specified
3. OR the dashboard rootDirectory is set

**⚠️ CRITICAL NEW ISSUE DISCOVERED:**
When you set `rootDirectory` in the dashboard, Vercel changes to that directory **BEFORE** running commands from `vercel.json`. This means:
- ❌ **WRONG:** `"buildCommand": "cd frontend && npm run build"` → Tries to go to `frontend/frontend` (doesn't exist!)
- ✅ **CORRECT:** `"buildCommand": "npm run build"` → Already in `frontend/`, just run the command
- ❌ **WRONG:** `"outputDirectory": "frontend/.next"` → Looks for `frontend/frontend/.next` (doesn't exist!)
- ✅ **CORRECT:** `"outputDirectory": ".next"` → Looks for `.next` in the current directory (`frontend/.next`)

---

## 3. Understanding the Concept 🎓

### Why This Error Exists

The `NOT_FOUND` error is Vercel's safety mechanism. It means:

> "I searched for a deployable application using my detection logic, but I couldn't find one. Rather than guessing or deploying something wrong, I'm stopping and asking you to clarify."

**What it's protecting you from:**
- **Accidental deployments**: Deploying backend Python code as a frontend app
- **Wrong directory deployments**: Deploying a test/staging app instead of production
- **Broken deployments**: Deploying incomplete or misconfigured builds
- **Wasted resources**: Running builds that will definitely fail

### The Correct Mental Model

Think of Vercel's deployment process as a **smart but cautious assistant**:

```
┌─────────────────────────────────────┐
│ 1. Clone Repository                 │
│    "I have your code"                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Framework Detection              │
│    "What am I deploying?"           │
│    - Look for package.json          │
│    - Look for framework files       │
│    - Check rootDirectory setting    │
└──────────────┬──────────────────────┘
               │
         ┌─────┴─────┐
         │           │
    Found?        Not Found?
         │           │
         ▼           ▼
    Continue    NOT_FOUND Error
         │      (Stop here)
         │
         ▼
┌─────────────────────────────────────┐
│ 3. Install Dependencies             │
│    "Getting everything ready"        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Build Application                 │
│    "Creating production version"    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 5. Deploy                            │
│    "Making it live"                  │
└─────────────────────────────────────┘
```

**For monorepos, you need to intervene at step 2:**

**Option A (Dashboard):**
```
Step 2: Framework Detection
  → Check rootDirectory setting: "frontend"
  → Change working directory to frontend/
  → Now look for package.json (found!)
  → Continue...
```

**Option B (vercel.json):**
```
Step 2: Framework Detection
  → Check vercel.json for buildCommand
  → See: "cd frontend && npm install && npm run build"
  → Execute build command (which changes directory)
  → Look for output in frontend/.next
  → Continue...
```

### How This Fits Into Vercel's Design

**Vercel's Philosophy:**
1. **Zero Configuration**: Should work out of the box for standard setups
2. **Explicit Over Implicit**: For non-standard setups, require explicit configuration
3. **Safety First**: Fail fast rather than deploy incorrectly

**Why rootDirectory is dashboard-only:**
- It's a **project-level setting**, not a code-level setting
- Different environments (preview, production) might need different root directories
- It affects the entire deployment pipeline, not just build commands
- It's part of the project's infrastructure configuration

**Why vercel.json build commands work:**
- They're **code-level configuration** (version controlled)
- They're executed during the build phase
- They're more flexible but require more explicit setup

---

## 4. Warning Signs & Prevention 🚨

### Red Flags to Watch For

#### 1. **Monorepo Structure Without Configuration**
```
Your repo structure:
├── frontend/          ← Your Next.js app
│   ├── package.json
│   └── next.config.js
├── backend/           ← Your Python API
│   └── requirements.txt
└── vercel.json        ← Might be missing or incorrect
```

**Action:** Immediately check if `rootDirectory` is set or `vercel.json` is configured.

#### 2. **Build Logs Show Wrong Directory**
Look for these in Vercel build logs:

**❌ Bad signs:**
```
> Installing dependencies...
> No package.json found
> Could not find Next.js installation
> Error: NOT_FOUND
```

**✅ Good signs:**
```
> Installing dependencies from frontend/package.json
> Detected Next.js version 14.2.35
> Building Next.js application
> Build completed successfully
```

#### 3. **Deployment Fails Immediately**
- **Configuration errors**: Fail in < 10 seconds
- **Build errors**: Fail after compilation starts (usually 30+ seconds)
- **NOT_FOUND**: Usually fails in 5-15 seconds

#### 4. **Multiple package.json Files**
```
├── package.json          ← Workspace root (if using workspaces)
├── frontend/
│   └── package.json      ← Next.js app
└── backend/
    └── (no package.json, uses requirements.txt)
```

**Issue:** Vercel might find the root `package.json` first and try to deploy that instead.

**Solution:** Use `rootDirectory` or ensure build commands target the correct directory.

### Code Smells & Patterns

#### Pattern 1: Missing Root Directory Configuration
```json
// ❌ BAD: No configuration
// (No vercel.json, no rootDirectory in dashboard)
// Result: NOT_FOUND error

// ✅ GOOD: Dashboard rootDirectory set to "frontend"
// OR vercel.json with proper build commands
```

#### Pattern 2: Incorrect Output Directory
```json
// ❌ BAD: Wrong path
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": ".next"  // Wrong! This is relative to repo root
}

// ✅ GOOD: Correct path relative to repo root
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/.next"  // Correct!
}
```

#### Pattern 3: Build Command Doesn't Change Directory
```json
// ❌ BAD: Assumes we're already in frontend/
{
  "buildCommand": "npm run build"  // Will fail - no package.json at root
}

// ✅ GOOD: Explicitly changes directory
{
  "buildCommand": "cd frontend && npm run build"
}
```

### Similar Mistakes to Avoid

#### 1. **Forgetting Root Directory in Team Settings**
- **Problem**: Works on your machine, fails for teammates
- **Solution**: Document the setting or use `vercel.json` (version controlled)

#### 2. **Assuming Auto-Detection Works Everywhere**
- **Problem**: Works for single-app repos, fails for monorepos
- **Solution**: Always verify configuration on first deployment

#### 3. **Mixing Configuration Methods**
- **Problem**: Setting both dashboard `rootDirectory` AND custom build commands
- **Solution**: Choose one approach and stick with it

#### 4. **Incorrect Path Assumptions**
- **Problem**: Using relative paths that assume a different working directory
- **Solution**: Always use paths relative to repository root in `vercel.json`

#### 5. **Missing Framework Declaration**
- **Problem**: Relying solely on auto-detection
- **Solution**: Explicitly set `"framework": "nextjs"` in `vercel.json`

---

## 5. Alternative Approaches & Trade-offs 🔄

### Approach 1: Vercel Dashboard rootDirectory ⭐ (RECOMMENDED)

**How it works:**
- Set in Vercel dashboard: Settings → General → Root Directory → `frontend`
- Vercel automatically changes to that directory before any commands
- No `vercel.json` needed (or minimal one)

**Pros:**
- ✅ Official Vercel method - most reliable
- ✅ Clean and simple - no custom build commands
- ✅ Next.js auto-detection works perfectly
- ✅ Can be different per environment (preview vs. production)
- ✅ No code changes needed

**Cons:**
- ❌ Not version-controlled (dashboard setting)
- ❌ Requires manual configuration per project
- ❌ Can be forgotten when creating new projects
- ❌ Team members might not know about it

**Best for:** Most use cases, especially when you want Vercel to handle everything automatically

**Trade-off:** Configuration lives outside code, but it's the most reliable method.

---

### Approach 2: vercel.json with Build Commands (Current Setup)

**How it works:**
- Use `vercel.json` with explicit `buildCommand` and `installCommand`
- Commands change directory before running
- Specify `outputDirectory` and `framework`

**Pros:**
- ✅ Version-controlled configuration
- ✅ Consistent across all deployments
- ✅ Works with Git-based deployments
- ✅ No manual dashboard configuration needed
- ✅ Team members can see the configuration in code

**Cons:**
- ❌ More complex build commands
- ❌ Requires maintaining `vercel.json`
- ❌ Less elegant than dashboard approach
- ❌ Path resolution can be tricky

**Best for:** Teams that want everything in code, or when dashboard access is limited

**Trade-off:** More explicit but requires careful path management.

---

### Approach 3: Separate Vercel Projects

**How it works:**
- Create separate Vercel projects:
  - Project 1: Points to repo, rootDirectory = `frontend`
  - Project 2: Points to repo, rootDirectory = `backend` (if deploying backend)

**Pros:**
- ✅ Complete isolation between frontend and backend
- ✅ Independent scaling and settings
- ✅ Clear separation of concerns
- ✅ Can deploy independently

**Cons:**
- ❌ More complex setup
- ❌ Multiple deployments to manage
- ❌ Higher cost (if on paid plans with multiple projects)
- ❌ More dashboard configuration

**Best for:** Large teams, microservices architecture, when frontend and backend need independent scaling

**Trade-off:** More management overhead but better isolation.

---

### Approach 4: Monorepo Tools (Turborepo, Nx)

**How it works:**
- Use monorepo build tools at repository root
- Single build command that handles all apps
- Vercel builds from root but uses tool's output

**Structure:**
```
├── package.json          ← Workspace root with Turborepo
├── turbo.json           ← Turborepo configuration
├── apps/
│   ├── frontend/        ← Next.js app
│   └── backend/         ← API
└── packages/            ← Shared packages
```

**Pros:**
- ✅ Optimized builds (caching, parallelization)
- ✅ Better for complex monorepos
- ✅ Industry-standard approach
- ✅ Handles dependencies between apps
- ✅ Single build command for everything

**Cons:**
- ❌ Additional tooling complexity
- ❌ Learning curve
- ❌ Overkill for simple two-app repos
- ❌ More setup time

**Best for:** Large monorepos, multiple apps, complex build dependencies, teams already using monorepo tools

**Trade-off:** More complexity but better for large-scale projects.

---

### Approach 5: Move Frontend to Repository Root

**How it works:**
- Restructure repository so Next.js app is at root
- Move backend to a subdirectory
- Vercel auto-detection works immediately

**Structure:**
```
├── package.json          ← Next.js app (at root)
├── next.config.js
├── app/
├── components/
└── backend/              ← Moved here
    └── ...
```

**Pros:**
- ✅ Simplest configuration (no changes needed)
- ✅ Vercel auto-detection works perfectly
- ✅ Standard Next.js project structure

**Cons:**
- ❌ Requires restructuring existing codebase
- ❌ Might break existing workflows
- ❌ Less clear separation
- ❌ Not ideal if backend is the primary app

**Best for:** When frontend is the primary application and backend is secondary

**Trade-off:** Requires code restructuring but simplest long-term.

---

### Recommendation for Your Project

**For your current setup (frontend + backend monorepo):**

**Primary recommendation:** **Approach 1 (Dashboard rootDirectory)**
- Set `rootDirectory` to `frontend` in Vercel dashboard
- This is the official, most reliable method
- Minimal configuration, maximum reliability

**If you prefer code-based configuration:** **Approach 2 (Current vercel.json)**
- Your current `vercel.json` is now properly configured
- Commit it and redeploy
- This works well for teams that want version-controlled config

**Don't use:** Approach 5 (restructuring) unless you're doing a major refactor anyway.

---

## Next Steps 🚀

### Immediate Action (Choose One)

#### Option A: Dashboard Method (Recommended)
1. Go to https://vercel.com/dashboard
2. Select your project
3. Settings → General → Root Directory
4. Set to `frontend` and save
5. Trigger a new deployment
6. Verify it works

#### Option B: vercel.json Method
1. The `vercel.json` is already updated
2. Commit and push the changes:
   ```bash
   git add vercel.json
   git commit -m "Fix Vercel NOT_FOUND: Configure monorepo build"
   git push
   ```
3. Vercel will automatically redeploy
4. Verify it works

### Verification Checklist

After deploying, verify:
- ✅ Build logs show: "Installing dependencies from frontend/package.json"
- ✅ Build completes successfully
- ✅ Home page loads (`/`)
- ✅ Profile page loads (`/profile`)
- ✅ No 404 errors in Vercel function logs
- ✅ API calls work (check browser console)

### If It Still Fails

1. **Check build logs** for specific error messages
2. **Verify paths** in `vercel.json` are correct
3. **Ensure** `frontend/package.json` exists and is valid
4. **Check** that `frontend/next.config.js` exists
5. **Verify** Node.js version compatibility (Next.js 14 requires Node 18+)

---

## Summary

**The Error:** Vercel couldn't find your Next.js app because it was looking at the repository root, but your app is in the `frontend/` subdirectory.

**The Fix:** Tell Vercel where to find your app by either:
1. Setting `Root Directory` to `frontend` in Vercel dashboard (recommended)
2. Using the updated `vercel.json` with proper build commands

**The Lesson:** For monorepos, always explicitly configure where Vercel should look for your application. Auto-detection only works at the repository root.

**Prevention:** When creating a monorepo, immediately configure the root directory or `vercel.json` before the first deployment.

