"""
Quick Guide: How to Access Post-Diagnosis Page
===============================================

STEP 1: RESTART STREAMLIT
--------------------------
The app needs to be restarted to load the new page!

Current app has been running for 24+ minutes.
It started BEFORE we added the post-diagnosis page.

TO RESTART:
1. In terminal, press: Ctrl+C (stop current app)
2. Then run: streamlit run app.py
3. Wait for "You can now view your Streamlit app in your browser"

STEP 2: FIND THE PAGE
----------------------
After restart, look in the LEFT SIDEBAR for:

    Post-Diagnosis   <-- NEW! This is the page

It should appear in the navigation list between:
   -  Search (above)
   -  Analytics (below)

STEP 3: USE IT
--------------
1. Click " Post-Diagnosis"
2. Select a patient
3. Use the 5 tabs:
   -  Diagnosis Info
   -  Medical Images
   -  Tumor Markers
   -  Treatment Plan
   -  Progress Timeline

TROUBLESHOOTING:
----------------
If you still don't see it after restart:
- Check the terminal for any errors
- Verify app.py was saved (it was!)
- Try: streamlit run app.py --server.port 8502
  (uses different port in case of cache issues)

The page EXISTS and is integrated!
You just need to RESTART Streamlit to see it.
"""

print(__doc__)
