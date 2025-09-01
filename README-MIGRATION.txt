MIGRATION CHECKLIST

1) Run migration:
   powershell -File scripts\migrate_from_archive.ps1
   (Paste your old folder path when prompted)

2) Sanity tests:
   powershell -File scripts\run_tests.ps1

3) If anything breaks:
   powershell -File scripts\restore_stubs.ps1

4) When stable:
   python scripts\make_checksums.py
   python verify_checksums.py
   git add .
   git commit -m "migrate core modules from archive"
   git push
