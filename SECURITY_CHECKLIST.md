# 🔒 Pre-Commit Security Checklist

## Before publishing to GitHub, verify:

### ✅ Files to Include (Safe)
- [ ] `test_case_generator.py` - Core functionality
- [ ] `streamlit_app.py` - Web interface
- [ ] `requirements.txt` - Dependencies
- [ ] `examples.py` - Sample usage
- [ ] `README.md` - Documentation
- [ ] `SETUP_GUIDE.md` - Installation guide
- [ ] `AWS_DEPLOYMENT.md` - Deployment guide
- [ ] `SECURITY.md` - Security information
- [ ] `Dockerfile` - Container configuration
- [ ] `deploy.sh` - Deployment script
- [ ] `.env.example` - Configuration template
- [ ] `.gitignore` - Git exclusions
- [ ] `.dockerignore` - Docker exclusions

### ❌ Files to Exclude (Private)
- [ ] `.env` - Contains API keys (NEVER commit)
- [ ] `*.xlsx` - Generated test files
- [ ] `*.log` - Log files
- [ ] `__pycache__/` - Python cache
- [ ] `venv/` - Virtual environment
- [ ] Any personal data files

### 🔍 Code Review
- [ ] No hardcoded API keys in any file
- [ ] No personal information in examples
- [ ] No company-specific data
- [ ] Environment variables used properly
- [ ] Error messages don't expose sensitive info

### 📝 Documentation
- [ ] Clear setup instructions
- [ ] Security warnings included
- [ ] Multiple AI provider options documented
- [ ] Local deployment option emphasized

### 🛡️ Security Features
- [ ] Input validation implemented
- [ ] Error handling without info disclosure
- [ ] User warnings about sensitive data
- [ ] Privacy-focused options available

## ✅ Final Check Commands

```bash
# Check for potential secrets
grep -r "api_key\|secret\|password\|token" --exclude-dir=.git --exclude="*.md" .

# Verify .gitignore works
git status

# Check what would be committed
git add --dry-run .

# Scan for sensitive patterns
git secrets --scan
```

## 🚨 Emergency Procedures

If sensitive data was accidentally committed:
1. **Immediately revoke** any exposed API keys
2. **Remove from history**: `git filter-branch` or BFG Repo-Cleaner
3. **Force push** cleaned history
4. **Generate new keys**
5. **Update documentation**

## 🎯 Ready to Publish!

Once all items are checked, the repository is safe for public GitHub publication.
