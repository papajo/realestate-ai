# Vercel NOT_FOUND Error - Complete Resolution Guide

## 1. The Fix

**IMPORTANT:** `rootDirectory` cannot be set in `vercel.json` - it's a project-level setting that must be configured in the Vercel dashboard.

### Option A: Vercel Dashboard (Recommended) ✅

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **General**
3. Find **Root Directory** section
4. Click **Edit** and set it to `frontend`
5. Click **Save**
6. Redeploy your project

This is the **recommended approach** because:
- It's the official way to handle monorepos
- Vercel will automatically change to that directory before running any commands
- No need for custom build commands
- Works seamlessly with Next.js auto-detection

### Option B: Build Commands in vercel.json

If you prefer a code-based approach, I've created a `vercel.json` file with explicit build commands:

```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "installCommand": "cd frontend && npm install",
  "outputDirectory": "frontend/.next"
}
```

**What this does:**
- Explicitly changes into the `frontend` directory before running commands
- Runs npm install and build from the correct location
- Specifies where the build output is located

**Note:** This approach works but is less elegant than using the dashboard's `rootDirectory` setting.

---

## 2. Root Cause Analysis

### What Was Happening vs. What Should Happen

**What was happening:**
- Vercel was trying to build from the repository root (`/Users/padoshi/Projects/RealEstate-AI/`)
- It couldn't find a `package.json` or Next.js configuration at the root level
- Vercel's build system couldn't identify this as a Next.js project
- Result: `NOT_FOUND` error because Vercel couldn't locate the application to deploy

**What should happen:**
- Vercel should recognize that the Next.js app is in the `frontend/` subdirectory
- It should change into that directory before running build commands
- It should detect Next.js 14 and use the appropriate build process
- The build should complete successfully and deploy

### What Triggered This Error?

1. **Monorepo Structure**: Your project has both `backend/` and `frontend/` directories, making it a monorepo
2. **Default Behavior**: Vercel assumes the root directory contains the application by default
3. **No Configuration**: Without explicit configuration, Vercel doesn't know to look in a subdirectory

### The Misconception

The oversight was assuming Vercel would automatically detect a Next.js app in a subdirectory. While Vercel has excellent auto-detection for Next.js apps, it only works when:
- The app is at the repository root, OR
- You explicitly tell Vercel where to find it

This is a common issue with monorepos where multiple applications exist in the same repository.

---

## 3. Understanding the Concept

### Why This Error Exists

The `NOT_FOUND` error is Vercel's way of saying: *"I looked for your application, but I couldn't find anything deployable at the location I expected."*

**What it's protecting you from:**
- Deploying the wrong directory (e.g., deploying backend code as a frontend)
- Wasting build minutes on failed deployments
- Confusion about what's actually being deployed

### The Mental Model

Think of Vercel's deployment process like this:

```
1. Clone Repository
   ↓
2. Look for framework (Next.js, React, etc.)
   ↓
3. Find package.json and build configuration
   ↓
4. Run install → build → deploy
```

**For monorepos, you need to tell Vercel:**
```
1. Clone Repository
   ↓
2. Change to [rootDirectory] (e.g., "frontend")
   ↓
3. Look for framework in that directory
   ↓
4. Run install → build → deploy
```

### Framework Integration

**Next.js on Vercel:**
- Vercel is the company behind Next.js, so integration is seamless
- Auto-detection works when Next.js is at the root
- For subdirectories, you need explicit configuration
- Vercel automatically handles:
  - Server-side rendering (SSR)
  - Static site generation (SSG)
  - API routes
  - Image optimization
  - Edge functions

**The `rootDirectory` setting:**
- Changes Vercel's working directory before any commands run
- All relative paths in your config are relative to this directory
- Build output is expected in this directory's `.next` folder

---

## 4. Warning Signs & Prevention

### Red Flags to Watch For

1. **Monorepo Structure**
   - Multiple apps in one repo (`frontend/`, `backend/`, `mobile/`)
   - If you see this, you'll likely need `rootDirectory` configuration

2. **Build Logs Show Wrong Directory**
   ```
   ❌ "No package.json found"
   ❌ "Could not find Next.js installation"
   ✅ Should show: "Installing dependencies from frontend/package.json"
   ```

3. **Deployment Fails Immediately**
   - If deployment fails in < 10 seconds, it's likely a configuration issue
   - Build errors usually take longer (compilation time)

4. **Multiple package.json Files**
   - Root-level `package.json` for workspace management
   - App-specific `package.json` in subdirectories
   - Vercel needs to know which one to use

### Code Smells & Patterns

**Pattern: Monorepo Without Configuration**
```json
// ❌ Missing vercel.json or rootDirectory setting
// Project structure:
// ├── frontend/
// │   ├── package.json
// │   └── next.config.js
// └── backend/
//     └── requirements.txt
```

**Pattern: Build Commands in Wrong Directory**
```json
// ❌ This won't work - commands run from root
{
  "buildCommand": "cd frontend && npm run build"
}
// ✅ Better - let rootDirectory handle it
{
  "rootDirectory": "frontend",
  "buildCommand": "npm run build"
}
```

### Similar Mistakes to Avoid

1. **Forgetting to Set Root Directory in Team Settings**
   - Each team member's local setup might work
   - But Vercel deployment fails
   - Solution: Always commit `vercel.json` or document the setting

2. **Assuming Auto-Detection Works Everywhere**
   - Works great for single-app repos
   - Fails silently for monorepos
   - Always verify in first deployment

3. **Mixing Build Tools**
   - Using `npm` in one place, `yarn` in another
   - Inconsistent lock files
   - Solution: Standardize on one package manager

---

## 5. Alternative Approaches & Trade-offs

### Approach 1: Vercel Dashboard rootDirectory (Recommended) ✅

**How to set:**
- Settings → General → Root Directory → Set to `frontend`

**Pros:**
- Official Vercel approach for monorepos
- Clean and simple - no custom build commands needed
- Next.js auto-detection works perfectly
- No vercel.json needed

**Cons:**
- Not version-controlled (dashboard setting)
- Requires manual configuration per project
- Can be forgotten when creating new projects

**Best for:** Most use cases, especially when you want Vercel to handle everything automatically

### Approach 2: vercel.json with Build Commands

**Pros:**
- Version-controlled configuration
- Consistent across all deployments
- Works with Git-based deployments
- No manual dashboard configuration needed

**Cons:**
- More complex build commands
- Requires maintaining vercel.json
- Less elegant than dashboard approach

**Best for:** Teams that want everything in code, or when dashboard access is limited

### Approach 2: Vercel Dashboard Settings

**Pros:**
- No code changes needed
- Easy to update without commits
- Can be different per environment (preview vs. production)

**Cons:**
- Not version-controlled
- Easy to forget when onboarding new team members
- Can drift from codebase structure

**Best for:** Quick fixes, personal projects, experimental setups

### Approach 3: Separate Vercel Projects

**Structure:**
- One Vercel project for `frontend/`
- Another for `backend/` (if deploying separately)
- Each project points to the same repo but different directories

**Pros:**
- Complete isolation
- Independent scaling and settings
- Clear separation of concerns

**Cons:**
- More complex setup
- Multiple deployments to manage
- Higher cost (if on paid plans)

**Best for:** Large teams, microservices architecture, independent scaling needs

### Approach 4: Monorepo Tools (Turborepo, Nx)

**Structure:**
- Use monorepo build tools at root
- Single build command that handles all apps
- Vercel builds from root but uses tool's output

**Pros:**
- Optimized builds (caching, parallelization)
- Better for complex monorepos
- Industry-standard approach

**Cons:**
- Additional tooling complexity
- Learning curve
- Overkill for simple two-app repos

**Best for:** Large monorepos, multiple apps, complex build dependencies

### Recommendation

For your current setup (frontend + backend), **Approach 1 (Dashboard rootDirectory)** is ideal because:
- Official Vercel method - most reliable
- Clean and simple - no custom build commands
- Next.js auto-detection works perfectly
- No configuration files needed

**If you prefer code-based configuration**, use Approach 2 (vercel.json) which is version-controlled and works well for teams.

---

## Next Steps

### If using Dashboard method (Recommended):
1. Go to Vercel dashboard → Settings → General → Root Directory
2. Set to `frontend` and save
3. Redeploy your project
4. Verify the deployment works

### If using vercel.json method:
1. **Commit the `vercel.json` file** to your repository
2. **Redeploy on Vercel** - the build should now succeed
3. **Verify the deployment** by checking:
   - Build logs show correct directory
   - Application loads correctly
   - All routes work (especially `/profile`)

## Testing the Fix

After deploying, verify:
- ✅ Home page loads (`/`)
- ✅ Profile page loads (`/profile`)
- ✅ API calls work (check browser console)
- ✅ No 404 errors in Vercel logs

## Additional Resources

- [Vercel Monorepo Guide](https://vercel.com/docs/monorepos)
- [Vercel Configuration Reference](https://vercel.com/docs/build-step)
- [Next.js Deployment on Vercel](https://nextjs.org/docs/deployment)

---

**Summary:** The error occurred because Vercel couldn't find your Next.js app at the repository root. 

**The fix:** Set `Root Directory` to `frontend` in your Vercel project settings (Settings → General → Root Directory). This tells Vercel where your Next.js app is located, resolving the NOT_FOUND error.

**Alternative:** Use the provided `vercel.json` with explicit build commands that change into the frontend directory, though the dashboard method is preferred.

